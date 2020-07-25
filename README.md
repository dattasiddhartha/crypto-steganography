## !PiedPiper
###### Empower users to upload their videos in the public domain while upholding privacy. 
<img src="https://i.imgur.com/Jtx0R11.png"></img>

###### <i>Collaborators</i>: [Kaustav Halder](https://github.com/kaustavha), [Yash Sinha](https://github.com/ysinha1), [Siddhartha Datta](https://github.com/dattasiddhartha)

#### Steganography

<img src="data/original.png" height="150px"></img>
<img src="data/encrypted.png" height="150px"></img>
<img src="data/mask.png" height="150px"></img>
<img src="data/restored.png" height="150px"></img>

Accepts the user's original video, obfuscates the video with a stenographic mask, allows user to store mask array, then allows user to retrieve mask array to decrpyt the video each time they wish to view it.

Install dependencies with `pip install -r requirements.txt`. Run stenographic mask generator `stenographic_mask_generator.py` to return mask arrays (refer to `example_stenography.ipynb` for example demonstration).

Download weights from
[here](https://drive.google.com/drive/folders/1ANqflh1dxSfgdFwvH1mZqZ8_vPS6WipB?usp=sharing).
* `cycle_gan/checkpoints` placed in `vision/`

Stenography functionality currently supported:
* CycleGAN ( `"apple2orange", "horse2zebra", "style_monet", "style_vangogh", "summer2winter_yosemite"`)

#### CLI tool

Run `python run_cli.py -h` for help / argument options. Parameters include
```
'--function': help='Options: "store" or "restore" (without quotations)')

'--filename', help='name of file stored in /data/')

'--style_index', help='Pass integer of index of style -- 0:apple2orange, 1:horse2zebra, 2:style_monet, 3:style_vangogh, 4:summer2winter_yosemite')

'--mode', help='Mode of steganography; options: "cyclegan"')

'--fps', help='framerate')

'--display', help='Displaying img; True, or False')
```

Run this in command line to generate and store masks:
```python
python run_cli.py --function store --filename cyclegan_test --style_index 1
```

Run this in command line to restore masks onto original image:
```python
python run_cli.py --function restore --filename cyclegan_test --style_index 1
```

