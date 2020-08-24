import argparse
from converter.converter import convert
parser = argparse.ArgumentParser()

parser.add_argument("image", help="the image to be converted")
# parser.add_argument("-v", "--verbose", help="increase output verbosity",
#                         action="store_true")
parser.add_argument("-c", "--charset",  help="the character set used in conversion",
                        choices=["full", "full_blocks", "half_blocks", "quarter_blocks"])
parser.add_argument("-s", "--size", nargs=2, metavar=("width", "height"), help="output image dimensions",
                    default=[0, 0], type=int)
# parser.add_argument("-r", "--raw", help="return raw text", action="store_true")
args = parser.parse_args()

img = convert(args.image, args.size[0], args.size[1], charset=args.charset)
img_printable = img.printable()
print(img.printable())
