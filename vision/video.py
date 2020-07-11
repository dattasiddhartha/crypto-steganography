import cv2
import os, glob
import numpy as np


def FrameGeneration(filename):

    """
    Parses mp4 videos into frames, stores frames into subdirectory in /data with same name as filename
    """
    
    # Load video, parse each video into frames

    if not os.path.exists("data/"+str(filename)):
        os.makedirs("data/"+str(filename))

    vc = cv2.VideoCapture("data/"+str(filename)+".mp4")

    if vc.isOpened():
        rval , frame = vc.read()
    else:
        rval = False

    c=1
    while rval:
        rval, frame = vc.read()
        try: 
            cv2.imwrite("data/"+str(filename)+"/"+str(c)+'.jpg',frame)
        except:
            continue
        c = c + 1
        cv2.waitKey(1)
    vc.release()
    
def VideoGeneration(filename, frame_ref, mode, style, fps):
    # choose codec according to format needed
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    WIDTH, HEIGHT = cv2.cvtColor(cv2.imread(frame_ref), cv2.COLOR_BGR2RGB).shape[1], cv2.cvtColor(cv2.imread(frame_ref), cv2.COLOR_BGR2RGB).shape[0]
    video=cv2.VideoWriter("data/"+str(filename)+"_cgan.mp4", fourcc, fps,(WIDTH, HEIGHT))

    filenames = []
    for f in glob.iglob("data/"+str(filename) + "/*"):
        filenames.append(f)

    if mode == 'cyclegan':
        for i in range(0,int(len(filenames))):
            img = cv2.imread('./vision/cycle_gan/results/'+str(style)+'/test_latest/images/'+str(i+1)+'_fake.png')
            video.write(img)

    cv2.destroyAllWindows()
    video.release()

