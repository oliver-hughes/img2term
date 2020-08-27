<!-- ![Lenna](examples/Lenna.png) ![Lenna Converted](examples/lenna_letters.png) -->
<p align="center">
  <img src="examples/gatsby.gif" />
</p>




---
# img2term
Render images in your terminal using unicode characters and ANSI color codes



---
## Getting Started

### Prerequisites
Python3 & PIL

`
python3 -m pip install pillow
`

---
## Usage
```
usage: img2term.py [-h] [-v]
                   [-c {full,full_blocks,half_blocks,quarter_blocks}]
                   [-s width height]
                   image

positional arguments:
  image                 the image to be converted

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -c {full,full_blocks,half_blocks,quarter_blocks}, --charset {full,full_blocks,half_blocks,quarter_blocks}
                        the character set used in conversion
  -s width height, --size width height
                        output image dimensions
```

### Arguments
#### size
Use `-s {} {}` or `--size {} {}` to set the size of the output image.

Since the height of each character is twice the width, you will need to take account of this when setting the size, for example:

An image that was `600x400 (width, height)`, would become `60x20` to maintain the same aspect ratio

#### charset
Choosing a different set of characters changes the possible unicode characters that will be used to display the image:

`full_blocks` consists of just `█`. Each character will be 1 colour.


`half_blocks` consists of `█` and `▄` . Each character could be split into two vertically, providing double the pixel density.


`quarter_blocks` consists of: `▎`,`▌`,`▊`,`▁`,`▂`,`▃`,`▄`,`▅`,`▆`,`▇`,`█`,`▘`,`▝`,`▖`,`▗`
allowing much finer subdivisions of each character


`full`, the default value, consists of all of the above, along with:`▚`,`▒`,`━`,`┃`,`╱`,`╲`,`◢`,`◣`,`◤`,`◥`. Making even finer details possible with the inclusion of angles.


## Examples
<p align="center">
  <img src="examples/Lenna.png" />
  <img src="examples/lenna_letters.png" />
</p>
