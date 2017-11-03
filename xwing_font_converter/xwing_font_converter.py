#!/usr/bin/env python
# coding: utf-8

"""
X-Wing font to image converter

:author: KalHamaar
:date: 24/10/2017

Used to convert xwing geordanr's font into png images.

:seealso: https://github.com/geordanr/xwing-miniatures-font
"""
import argparse
from sys import exit

from os.path import basename

from font_converter import FontConverter
from logger import get_logger

# __all__ = ['main']

__prog_name__ = 'X-Wing Font Converter'
__version__ = '0.1'
__author__ = 'KalHamaar'
__description__ = 'Convert geordanr\'s font into images'
__url__ = 'https://github.com/kalhamaar/xwing_font_converter'


parser = argparse.ArgumentParser(description='X-Wing font to image converter by KalHamaar')

# optional arguments
parser.add_argument('-c', '--color', dest='COLOR', default='black', action='store',
                    choices=['black', 'white', 'red', 'green'],
                    help='color of font to use (default: %(default)s)')

parser.add_argument('-p', '--pointsize', dest='PS', default=50, action='store',
                    help='size of font to use (default: %(default)s)')

parser.add_argument('-s', '--size', dest='SIZE', default=72, action='store',
                    help='size of generated image as x*x (default: %(default)sx%(default)s)')

parser.add_argument('-f', '--format', dest='FORMAT', default='gif', action='store',
                    choices=['gif', 'png'],
                    help='output file format (default: %(default)s)')

parser.add_argument('-v', '--verbosity', dest='VERBOSITY', default='INFO', action='store',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                    help='log level to use (default: %(default)s)')

required = parser.add_argument_group('required arguments')

required.add_argument('-m', '--map', dest='MAP', help='mapping file to use (.scss)')
required.add_argument('-t', '--ttf', dest='TTF', help='TrueType Font file to use (.ttf)')
required.add_argument('-o', '--output', dest='OUT', help='output folder (will created if not exist)')


def main():
    """
    Main entry point for font converter

    :return:
    """
    args = parser.parse_args()

    logger = get_logger(loglevel=args.VERBOSITY)

    if any(l is None for l in [args.MAP, args.TTF, args.OUT]):
        parser.print_help()
        exit(-1)

    logger.info('Starting extraction of {}'.format(basename(args.TTF)))

    logger.debug("Map file: {map_file_path} TTF File: {ttf_file_path} Output folder: {output_folder}"
                 .format(map_file_path=args.MAP,
                         ttf_file_path=args.TTF,
                         output_folder=args.OUT))

    fc = FontConverter(map_file_path=args.MAP,
                       ttf_file_path=args.TTF,
                       output_folder=args.OUT)

    if not fc.init_font_converter():
        exit(-1)

    fc.get_elements_from_map()

    logger.debug("Converting {point_size} point size font to {color} {size}x{size} {file_format} images"
                 .format(point_size=args.PS,
                         color=args.COLOR,
                         size=args.SIZE,
                         file_format=args.FORMAT))

    fc.convert_2_images(color=args.COLOR, point_size=args.PS, size=args.SIZE, file_format=args.FORMAT)

    logger.info("Extraction done, files available in: {}".format(args.OUT))


if __name__ == '__main__':
    main()
