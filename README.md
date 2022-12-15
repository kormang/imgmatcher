# imgmatcher

Simple script that compares images from two directories and finds equal of very similar ones.

## Original purpose

Task was to replace about 200 images for a web site, with a better quality ones. New images had different names, directory stracture was different, sometimes format was different, dimensions could differ, and so could colour. Also some images didn't have their true match, as two images in the destination were sometimes represented as one image in the source directory.

## How to run it

### Prerequisites

Program has only been ran on Ubuntu 20.04 using Python 3.8.

It is recommended to create virtual env with `python3 -m venv .venv && source .venv/bin/active`

Install deps `pip install opencv-python scikit-image`

### Running it

`python3 main.py -s <source-dir> -d <destination-dir> [-t <ssim-threshold>]`

Run `python3 main.py --help` for more info, or just look at the source.

It will output list of matches in format:
`source-img.jpg -> dest-img.png (0.99)`

After that list of source images without a match are listed.

Lists can then be processed by another tool/script.

## How it works

It traverses all files in source directory, tries to load them as image, and if succeedes, traverses all files in destination directory to try to find matching image. So it is O(S * D), where S is the number of source images, and D is the number of destination images, not very optimal, but it did save time and filled it's purpose.

To compare images, [structural similarity index](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html) is used. Default threshold is 0.9, but it can be changed via `-t` command line argument.

### Can it be better

It it sensitive to threshold value, and also not very optimal as mentioned previously. Using methods based on Locality-sensitive hashing could prove to be much faster, and provide more flexibility, but to find matches for about 200 images, wasting time on such optimisation isn't rational.


