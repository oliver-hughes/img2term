import argparse
from converter.converter import convert
from time import sleep
parser = argparse.ArgumentParser()

parser.add_argument("image", help="the image to be converted")
# parser.add_argument("-v", "--verbose", help="increase output verbosity",
#                         action="store_true")
parser.add_argument("-c", "--charset",  help="the character set used in conversion",
                        choices=["full", "full_blocks", "half_blocks", "quarter_blocks"])
parser.add_argument("-s", "--size", nargs=2, metavar=("width", "height"), help="output image dimensions",
                    default=[0, 0], type=int)
# parser.add_argument("-r", "--raw", help="return raw text", action="store_true")
parser.add_argument("-a", "--animated", help="display animated image, optional value for framerate", nargs="?",
                    default=-1, const=0, type=int)
args = parser.parse_args()

if args.animated >= 0:

    img, frame_time = convert(args.image, args.size[0], args.size[1], charset=args.charset, animated=True)
    # if image is actually animated
    if frame_time > 0:
        if args.animated > 0:
            frame_time = 1 / args.animated
        print("\x1b[2J")
        try:
            while True:
                for frame in img:
                    print("\x1b[0;0f".format(frame.height, frame.width))
                    print(frame.printable())
                    print("ctrl-c to stop")
                    sleep(frame_time)
        except KeyboardInterrupt:
            print("\x1b[0;0f \x1b[0m \x1b[J ".format(frame.height, frame.width))
            pass
    # image isn't animated
    else:
        print(img[0].printable())
else:
    img = convert(args.image, args.size[0], args.size[1], charset=args.charset)
    img_printable = img.printable()
    print(img_printable)
