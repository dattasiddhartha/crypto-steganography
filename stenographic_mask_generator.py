# imports
import cv2
import os, glob, shutil
from PIL import Image
import matplotlib, random
import torch, torchvision
import torchvision.transforms as T
import matplotlib.pyplot as plt
import numpy as np
from vision.cyclegan import CYCLEGAN
from vision.video import FrameGeneration, VideoGeneration


# options
styles = ["apple2orange", "horse2zebra", "style_monet", "style_vangogh", "summer2winter_yosemite"]
modes = ['cyclegan', 'foregroundremoval']

# Mask generation
def MaskGenerator(fakeimg_path, realimg_path, display):
    # processing original images
    transform = T.Compose([T.ToTensor()])

    img_fake = cv2.cvtColor(cv2.imread(fakeimg_path), cv2.COLOR_BGR2RGB)
    img_rgb_fake = transform(img_fake)
    img_array_floating_fake = np.array(img_rgb_fake[:,:,:])

    img_real = cv2.cvtColor(cv2.imread(realimg_path), cv2.COLOR_BGR2RGB)
    img_rgb_real = transform(img_real)
    img_array_floating_real = np.array(img_rgb_real[:,:,:])

    # generating stenographic mask
    masked_img = []
    for j in range(img_rgb_real.shape[2]): # for each pixel along width
        sub_masked_img = []
        for i in range(img_rgb_real.shape[1]): # for each pixel along height
            tmp=[]
            for h in range(img_rgb_fake.shape[0]): # for each image channel
                tmp.append(img_array_floating_fake[h][i][j]-img_array_floating_real[h][i][j])
            sub_masked_img.append(tmp)
        masked_img.append(sub_masked_img) 

    masked_img_array = np.array(masked_img)

    if display == True:
        print("Ground truth image")
        plt.imshow(img_real)
        plt.show()
        print("Encrypted image")
        plt.imshow(img_fake)
        plt.show()
        print("Stenographic mask image")
        plt.imshow(masked_img_array[:,:,:])
        plt.show()
        print("Stenographic mask array")
        print(masked_img_array)
        
    return masked_img_array

# Video Restoration
def Restoration(masked_img_array, fakeimg_path, store_path, display):
    
    transform = T.Compose([T.ToTensor()])

    img_fake = cv2.cvtColor(cv2.imread(fakeimg_path), cv2.COLOR_BGR2RGB)
    img_rgb_fake = transform(img_fake)
    img_array_floating_fake = np.array(img_rgb_fake[:,:,:])

    # masked_img_array

    # restoring original from (fake, mask)
    restored_img = []
    for j in range(img_rgb_fake.shape[2]): # for each pixel along width
        sub_masked_img = []
        for i in range(img_rgb_fake.shape[1]): # for each pixel along height
            tmp=[]
            for h in range(img_rgb_fake.shape[0]): # for each image channel
                tmp.append(img_array_floating_fake[h][j][i]-masked_img_array[i][j][h])
            sub_masked_img.append(tmp)
        restored_img.append(sub_masked_img) 

    restored_img_array = np.array(restored_img)

    if display == True:
        print("Restored image")
        plt.imshow(restored_img_array)
        plt.show()
        

    # reshape array for video export
    restored_img = []
    for j in range(restored_img_array.shape[2]): # channel
        sub_masked_img = []
        for h in range(restored_img_array.shape[0]): # width
            tmp=[]
            for i in range(restored_img_array.shape[1]): # height
                tmp.append(restored_img_array[h][i][j])
            sub_masked_img.append(tmp)
        restored_img.append(sub_masked_img) 
    restored_img = np.array(restored_img)
    

    matplotlib.image.imsave(store_path, restored_img_array)
    
    return restored_img_array

def RunStenography(filename, style_index, mode, fps, display):
    
    # parse video into frames
    FrameGeneration(filename)
    
    # Load frames
    filenames = []
    for f in glob.iglob("data/"+str(filename) + "/*"):
        filenames.append(f)
    
    # perform style transfer via CycleGAN
    if mode == 'cyclegan':
        CYCLEGAN(
                destination_style = styles[style_index], 
                source_image = "data/"+str(filename),
                num = int(len(filenames)*2),
                )
        
    # Video generation
    VideoGeneration(
        filename = filename,
        frame_ref = './vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(1)+'_fake.png', 
        mode = mode, 
        style = styles[style_index], 
        fps = fps,
    ) 
    print("Video generated, filename: ", str(filename)+"_cgan.mp4")
    
    # Generate stenographic masks
    if mode == 'cyclegan':
        stenographic_masks_stored = []
        for i in range(0,int(len(filenames))):
            masked_img_array = MaskGenerator(
                                fakeimg_path = './vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(i+1)+'_fake.png',
                                realimg_path = './vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(i+1)+'_real.png',
                                display = False
                                )
            stenographic_masks_stored.append(masked_img_array)

    return stenographic_masks_stored
    
    
def RestoreVideo(stenographic_masks_stored, filename, style_index, mode, fps, display):
    
    # Count frames -- can parse frames from the encrypted video
    filenames = []
    for f in glob.iglob("data/"+str(filename) + "/*"):
        filenames.append(f)
    
    # Apply stenographic mask onto encrpted video to restore original video for display
    if mode == 'cyclegan':

        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        WIDTH, HEIGHT = cv2.cvtColor(cv2.imread('./vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(1)+'_fake.png'), cv2.COLOR_BGR2RGB).shape[1], cv2.cvtColor(cv2.imread('./vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(1)+'_fake.png'), cv2.COLOR_BGR2RGB).shape[0]
        video=cv2.VideoWriter("data/"+str(filename)+"_restored.mp4", fourcc, fps,(WIDTH, HEIGHT))

        for i in range(0,int(len(filenames))):
            restored_img_array = Restoration(
                                        masked_img_array = stenographic_masks_stored[i], 
                                        fakeimg_path = './vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(i+1)+'_fake.png',  
                                        store_path = './vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(i+1)+'_restored.png',
                                        display = False,
                                    )

            video.write(cv2.imread('./vision/cycle_gan/results/'+str(styles[style_index])+'/test_latest/images/'+str(i+1)+'_restored.png'))


        cv2.destroyAllWindows()
        video.release()

    print("Video generated, filename: ", str(filename)+"_restored.mp4")
    
    
def DeleteProcessingFiles(style_index):
    # delete folder in cyclegan directory with style folder name, delete visions folder inside visions folder
    shutil.rmtree("./vision/vision", ignore_errors=True)
    shutil.rmtree('./vision/cycle_gan/results/'+str(styles[style_index]), ignore_errors=True)