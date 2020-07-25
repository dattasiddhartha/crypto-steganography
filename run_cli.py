# cli tool for backend / oneclick usage
from stenographic_mask_generator import RunStenography, RestoreVideo
import argparse

parser = argparse.ArgumentParser(description='crypto+steganography')

parser.add_argument('--function', type=str,
                    help='Options: "store" or "restore" (without quotations)')

parser.add_argument('--filename', type=str,
                    help='name of file stored in /data/')

parser.add_argument('--style_index', type=int, default=1,
                    help='Pass integer of index of style -- 0:apple2orange, 1:horse2zebra, 2:style_monet, 3:style_vangogh, 4:summer2winter_yosemite')

parser.add_argument('--mode', type=str, default="cyclegan",
                    help='Mode of steganography; options: "cyclegan"')

parser.add_argument('--fps', type=int, default=25,
                    help='framerate')

parser.add_argument('--display', type=bool, default=False,
                    help='Displaying img; True, or False')

args = parser.parse_args()

if args.function == "store":
    RunStenography(args.filename, args.style_index, args.mode, args.fps, args.display)

if args.function == "restore":
    RestoreVideo(args.filename, args.style_index, args.mode, args.fps, args.display)

