X-Wing Font to Images converter
===============================

Vector font by [Hinny](https://github.com/Hinny), [armoredgear7](https://github.com/armoredgear7), and [ScottKarch](https://github.com/ScottKarch).

[List of symbols on xwing-miniatures-font](https://geordanr.github.io/xwing-miniatures-font/)

## Idea
The idea of this script is to convert each elements of a font to separated images.
For a later use on forum and so on.
It needed the *scss* file to know what ship/icons correspond to what character.

## Installation
No specific need, except _python_, which is commonly installed on most of linux distribution

## Usage
    usage: xwing-font-converter.py [-h] [-c {black,white}] [-p PS] [-s SIZE]
                                   [-m MAP] [-t TTF] [-o OUT]

    X-Wing font to image converter by KalHamaar

    optional arguments:
      -h, --help            show this help message and exit
      -c {black,white}, --color {black,white}
                            Color of font to use (default: black)
      -p PS, --pointsize PS
                            Size of font to use (default: 50)
      -s SIZE, --size SIZE  Size of generated image as x*x (default: 64x64)

    required arguments:
      -m MAP, --map MAP     Mapping file to use (.scss)
      -t TTF, --ttf TTF     TrueType Font file to use (.ttf)
      -o OUT, --output OUT  Output folder (will created if not exist)

### Example:

    $ ./xwing-font-converter.py -m resources/_ships-map.scss -t resources/xwing-miniatures-ships.ttf -o output/test -c white

