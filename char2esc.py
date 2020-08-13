
esc = "\x1b["
def c2e(char, bg, fg):
    out = ""
    out += f"{esc}48;2;{bg[0]};{bg[1]};{bg[2]}m"
    out += f"{esc}38;2;{fg[0]};{fg[1]};{fg[2]}m"
    return out + char
