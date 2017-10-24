#! /usr/bin/python
# coding: utf-8

"""
X-Wing font to image converter

:author: KalHamaar
:date: 24/10/2017

Used to convert font from geordanr into png images

:seealso: https://github.com/geordanr/xwing-miniatures-font


"""
import argparse

import sys

from font_converter import FontConverter
from logger import get_logger

parser = argparse.ArgumentParser(description='X-Wing font to image converter by KalHamaar')

# optional arguments
parser.add_argument('-c', '--color', dest='COLOR', default='black', action='store',
                    choices=['black', 'white'],
                    help='Color of font to use (default: %(default)s)')
parser.add_argument('-p', '--pointsize', dest='PS', default=50, action='store',
                    help='Size of font to use (default: %(default)s)')
parser.add_argument('-s', '--size', dest='SIZE', default=64, action='store',
                    help='Size of generated image as x*x (default: %(default)sx%(default)s)')

required = parser.add_argument_group('required arguments')

required.add_argument('-m', '--map', dest='MAP', help='Mapping file to use (.scss)')
required.add_argument('-t', '--ttf', dest='TTF', help='TrueType Font file to use (.ttf)')
required.add_argument('-o', '--output', dest='OUT', help='Output folder (will created if not exist)')


if __name__ == '__main__':

    logger = get_logger()
    args = parser.parse_args()

    if any(l is None for l in [args.MAP, args.TTF, args.OUT]):
        parser.print_help()
        sys.exit(-1)

    logger.info('Starting conversion')

    fc = FontConverter(map_file_path=args.MAP,
                       ttf_file_path=args.TTF,
                       output_folder=args.OUT)

    fc.get_elements_from_map()
    fc.convert_2_images(color=args.COLOR, point_size=args.PS, size=args.SIZE)

    logger.info("Files available in: {}".format(args.OUT))
