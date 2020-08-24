from PIL import Image
import numpy as np
from .char2esc import c2e
from .charimage import CharImage, CharPixel
full_blocks = {
    u"█": 0xffffffff,# FULL BLOCK
}
half_blocks = {
    u"▄": 0x0000ffff,# half block lower
}
quarter_blocks = {
    u"▎": 0x88888888,#hblk 1q
    u"▌": 0xcccccccc,#hblk 2q
    u"▊": 0xeeeeeeee,#hblk 3q
    u"▁": 0x0000000f,
    u"▂": 0x000000ff,
    u"▃": 0x00000fff,
    # u"▄": 0x0000ffff,# half block lower
    u"▅": 0x000fffff,
    u"▆": 0x00ffffff,
    u"▇": 0x0fffffff,
    # u"█": 0xffffffff,# full block
    u'▘': 0xcccc0000,
    u'▝': 0x33330000,
    u'▖': 0x0000cccc,
    u'▗': 0x00003333
}

non_blocks = {
    u'▚': 0xcccc3333,
    u'▒': 0xa5a5a5a5,
    u'━': 0x000ff000,
    u'┃': 0x66666666,

    u'╱': 0x11224488,
    u'╲': 0x88442211,
    u'◢': 0x113377ff,#brt
    u'◣': 0x88cceeff,#blt
    u'◤': 0xffeecc88,#ult
    u'◥': 0xff773311 #urt
}

def differentbits(hex1, hex2):
    total = 0

    for i in range(32):
        if (((hex1 >> i) & 1) != ((hex2 >> i) & 1)):
            total += 1
    return total

def convert(image, width=0, height=0, charset="full", verbose=False):

    # build dictionary of characters for output
    img_chars = full_blocks
    if charset != "full_blocks":
        img_chars = {**img_chars, **half_blocks}
        if charset != "half_blocks":
            img_chars = {**img_chars, **quarter_blocks}
            if charset != "quarter_blocks":
                img_chars = {**img_chars, **non_blocks}

    # load image
    im = Image.open(image)

    # set output width and height if not given
    if width == 0 and height == 0:
        width, height = im.size
        width = int(width/4)
        height = int(height/8)

    # resize image to match output size *= 4
    im = im.resize((width*4, height*8))

    # out = CharImage(width, height)
    # out_image = []
    # out = [["" for w in range(width)] for h in range(height)]
    out = []
    for cy in range(int(height)):
        out_row = []
        for cx in range(int(width)):
            # offset pixel x,y from char x,y
            px = cx * 4
            py = cy * 8

            minvals = [256, 256, 256]
            maxvals = [0, 0, 0]

            # determine which colour has the largest range in the area
            for y in range(8):
                for x in range(4):
                    r, g, b = im.getpixel((px+x, py+y))
                    minvals = [min(minvals[0], r), min(minvals[1], g), min(minvals[2], b)]
                    maxvals = [max(maxvals[0], r), max(maxvals[1], g), max(maxvals[2], b)]
            delta = [maxvals[0] - minvals[0], maxvals[1] - minvals[1], maxvals[2] - minvals[2]]
            delta_channel = delta.index(max(delta))
            # median value of the largest shifting colour channel
            median = minvals[delta_channel] + int( delta[delta_channel] / 2 )

            # determine pattern of pixels by if above/below median
            char_pattern = 0x0
            for y in range(8):
                rowc = 0x0
                for x in range(4):
                    if im.getpixel((px+x, py+y))[delta_channel] > median:
                        rowc += 1 << (3-x)
                char_pattern += rowc << 4*(7-y)

            # find closest matching character to actual pixel pattern
            invert = False
            output_char = u" "
            output_pattern = 0x0
            min_difference = 32
            for char, pattern in img_chars.items():
                diff = differentbits(pattern, char_pattern)
                diffinverse = differentbits(pattern ^ 0xFFFFFFFF, char_pattern)
                if ( diff < min_difference):
                    output_char = char
                    min_difference = diff
                    output_pattern = pattern
                    invert = False
                if (diffinverse < min_difference):
                    output_char = char
                    min_difference = diffinverse
                    output_pattern = pattern ^ 0xFFFFFFFF
                    invert = True


            colours = [[0,0,0],[0,0,0]]
            totals = [0,0]
            for y in range(8):
                for x in range(4):
                    r,g,b = im.getpixel((px+3-x, py+7-y))
                    i = 1 << (x) + (y*4)
                    # match = (output_pattern & i) >> (x) + (y*4)
                    # testing against real pattern not shape of char
                    # - reduces halo/glow efct.
                    match = (char_pattern & i) >> (x) + (y*4)
                    colours[match][0] += r
                    colours[match][1] += g
                    colours[match][2] += b
                    totals[match] += 1

            for t in range(2):
                if totals[t]:
                    for h in range(3):
                        colours[t][h] = int(colours[t][h] / totals[t])

            if invert:
                temp = colours[0]
                colours[0] = colours[1]
                colours[1] = temp

            # out[cy][cx] = c2e(output_char, colours[0], colours[1])
            # out.set(cx, cy, CharPixel(output_char, colours[1], colours[0]))
            out_row.append(CharPixel(output_char, colours[1], colours[0]))
        out.append(out_row)

    return CharImage(out)
