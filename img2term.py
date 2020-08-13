
import argparse
import converter
parser = argparse.ArgumentParser()

parser.add_argument("image", help="the image to be converted")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
parser.add_argument("-c", "--charset",  help="the character set used in conversion",
                        choices=["full", "full_blocks", "half_blocks", "quarter_blocks"])
parser.add_argument("-s", "--size", nargs=2, metavar=("width", "height"), help="output image dimensions",
                    default=[0, 0], type=int)

args = parser.parse_args()

img = converter.convert(args.image, args.size[0], args.size[1], charset=args.charset)
for row in img:
    print("".join(c for c in row) + "\x1b[0m")
