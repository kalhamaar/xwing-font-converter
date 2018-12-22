# X-Wing Font to Images converter

Vector font by [Hinny](https://github.com/Hinny), [armoredgear7](https://github.com/armoredgear7), and [ScottKarch](https://github.com/ScottKarch).

X-Wing miniature font by [geordanr](https://github.com/geordanr)

[List of symbols on xwing-miniatures-font](https://geordanr.github.io/xwing-miniatures-font/)

## Idea

The idea of this script is to convert each elements of a font to separated images.
For a later use on forum and so on.
It needed the JQON (*.json*) file to know what ship/icons correspond to what character.
And the TrueTypeFont (*.ttf*) file to extract image from

eg:
[_ships-map.scss](https://github.com/geordanr/xwing-miniatures-font/blob/master/src/sass/_ships-map.scss)
and
[xwing-miniatures-ships.ttf](https://github.com/geordanr/xwing-miniatures-font/blob/master/src/fonts/xwing-miniatures-ships.ttf)


## Installation

1. Download zip from GitHub page
2. Install:

    ```
    $ unzip xwing-font-converter-master.zip
    $ cd xwing-font-converter-master/
    $ python setup.py install
    ```



## Usage

    usage: xwing_font_converter.py [-h]
                                   [-c {black,white,blue,red,grey,violet,green,yellow,steelblue1}]
                                   [-p PS] [-s SIZE] [--trim] [--width]
                                   [-f {gif,png}] [-v {DEBUG,INFO,WARNING,ERROR}]
                                   [-m MAP] [-t TTF] [-o OUT]
    
    X-Wing font to image converter by KalHamaar
    
    optional arguments:
      -h, --help            show this help message and exit
      -c {black,white,blue,red,grey,violet,green,yellow,steelblue1}, --color {black,white,blue,red,grey,violet,green,yellow,steelblue1}
                            color of font to use (default: black)
      -p PS, --pointsize PS
                            size of font to use (default: 50)
      -s SIZE, --size SIZE  size of generated image as x*x (default: 72x72)
      --trim                Trim images (remove transparent border) (default:
                            False)
      --width               Resize with width as reference (default: False)
      -f {gif,png}, --format {gif,png}
                            output file format (default: gif)
      -v {DEBUG,INFO,WARNING,ERROR}, --verbosity {DEBUG,INFO,WARNING,ERROR}
                            log level to use (default: INFO)
    
    required arguments:
      -m MAP, --map MAP     mapping file to use (.json)
      -t TTF, --ttf TTF     TrueType Font file to use (.ttf)
      -o OUT, --output OUT  output folder (will created if not exist)



### Example:

    $ ./xwing-font-converter -m resources/ships-map.json -t resources/xwing-miniatures-ships.ttf -o output/test -c white

