from .char2esc import c2e
class CharPixel:
    def __init__(self, char, fg_rgb, bg_rgb):
        self.char = char
        self.fg = fg_rgb
        self.bg = bg_rgb

    def printable(self):
        return c2e(self.char, self.bg, self.fg)

class CharImage:
    def __init__(self, char_array):
        self.image = char_array

    def set(self, x, y, charpix):
        self.image[x][y] = charpix

    def printable(self):
        out = ""
        for row in self.image:
            out += "".join(c.printable() for c in row) + "\x1b[0m" + "\n"
        return out
