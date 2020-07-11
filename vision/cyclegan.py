import subprocess

def CYCLEGAN(destination_style, source_image, num):
    """
    destination_style can be from ["apple2orange", "horse2zebra", "style_monet", "style_vangogh", "summer2winter_yosemite"]
    """
    if destination_style == "apple2orange":
        subprocess.run("python ./vision/cycle_gan/test.py --dataroot "+str(source_image)+" --name apple2orange --model test --no_dropout")
        
    if destination_style == "horse2zebra":
        subprocess.run("python ./vision/cycle_gan/test.py --dataroot "+str(source_image)+" --name horse2zebra --model test --no_dropout --num_test "+str(num))
        
    if destination_style == "style_monet":
        subprocess.run("python ./vision/cycle_gan/test.py --dataroot "+str(source_image)+" --name style_monet --model test --no_dropout")
        
    if destination_style == "style_vangogh":
        subprocess.run("python ./vision/cycle_gan/test.py --dataroot "+str(source_image)+" --name style_vangogh --model test --no_dropout")
        
    if destination_style == "summer2winter":
        subprocess.run("python ./vision/cycle_gan/test.py --dataroot "+str(source_image)+" --name summer2winter --model test --no_dropout")
        