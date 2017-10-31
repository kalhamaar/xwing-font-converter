# coding=utf-8
import locale
import os
import re
import subprocess

import time

from logger import get_logger

AVAILABLE_COLORS = ['black', 'white', 'red', 'green']
AVAILABLE_FILE_FORMATS = ['gif', 'png']


class FontConverter(object):
    """
    Class implementing main conversion mechanism
    """

    def __init__(self, map_file_path, ttf_file_path, output_folder):
        super(FontConverter, self).__init__()

        self._map_file_path = map_file_path
        self._ttf_file_path = ttf_file_path
        self._output_folder = output_folder

        self._element_map = {}
        self._log = get_logger()

    def init_font_converter(self):
        """
        Check if given files are correct and create output file if necessary

        :return: Whether initialisation was ok or not
        :rtype: bool
        """
        init_ok = True

        init_ok = init_ok and self.__check_file_integrity(self._map_file_path, 'scss')
        init_ok = init_ok and self.__check_file_integrity(self._ttf_file_path, 'ttf')

        if not os.path.exists(self._output_folder):
            os.makedirs(self._output_folder)
            time.sleep(0.25)  # to left system sync

        return init_ok

    @property
    def element_map(self):
        return self._element_map

    def __check_file_integrity(self, file_path, exp_file_format):
        """
        Check if given file is valid or not

        :param file_path: Path to file to check
        :type file_path: str

        :param exp_file_format: Expected file format (usually scss and tff)
        :type exp_file_format: str

        :return: whether given file is valid or not
        :rtype: bool
        """
        status = os.path.exists(file_path) and exp_file_format in os.path.splitext(file_path)[1]
        if not status:
            self._log.error("Given '{}' file ({}) does not exist or invalid !".format(exp_file_format, file_path))
        return status

    def get_elements_from_map(self):
        """
        Use regular expression on map file to extract elements names and key codes

        :return: None
        """
        # open it
        with open(self._map_file_path, 'rb') as map_file:
            test_str = map_file.read()

        regex = r"s*(.*)\:\s\"(.*)\",.*"
        matches = re.finditer(regex, test_str)
        # then parse it to get key code
        for match in matches:
            element_name = match.group(1).lstrip()
            element_code = match.group(2).lstrip()

            # because icons are in css code (eg: \011E mean Ğ)
            if element_code.startswith('\\'):
                # replace \ by \u to convert to unicode str
                element_code = element_code.replace('\\', '\u').decode('unicode-escape')

            # for better quote enclosing insert quoting here
            if element_code == "'":
                # if element code is single-quote, surround with double-quotes
                element_code = "\"" + element_code + "\""
            else:
                element_code = "'" + element_code + "'"

            self._element_map[element_name] = element_code

    def convert_2_images(self, color='black', point_size=50, size=72, file_format='gif'):
        """
        Convert all elements in map into images according given options

        :param file_format: Image file format (in 'gif', 'png')
        :type file_format: str

        :param color: Color to use (in 'black', 'white', 'red', 'green')
        :type color: str

        :param point_size: Size of font (default 50)
        :type point_size: int

        :param size: Size of the resulting image in pixel (default 72)
        :type size: int

        :raise AttributeError in case of wrong color or format
        :raise subprocess.CalledProcessError is error occurs during conversion

        :rtype: None
        """
        if color not in AVAILABLE_COLORS:
            raise AttributeError("Color should be in {colors} (got: {color})".format(colors=','.join(AVAILABLE_COLORS),
                                                                                     color=color))

        if file_format not in AVAILABLE_FILE_FORMATS:
            raise AttributeError("File format should be in {formats} (got: {format})"
                                 .format(formats=','.join(AVAILABLE_FILE_FORMATS), format=file_format))

        # if ok convert TTF to images
        for element in sorted(self._element_map):
            self._log.info(u"Processing '{element}' (keycode: {keycode}) ...".
                           format(element=element, keycode=self._element_map[element]))

            output_file = os.path.join(self._output_folder, "{ship}-{color}.{format}"
                                       .format(ship=element, color=color, format=file_format))
            convert_cmd = u"convert -font {ttf_file} -background none -fill {color} -gravity center " \
                          u"-pointsize {pointsize} -size {size}x{size} caption:{keycode} {output}". \
                format(ttf_file=self._ttf_file_path,
                       color=color,
                       pointsize=point_size,
                       size=size,
                       keycode=self._element_map[element],
                       output=output_file)

            self._log.debug(convert_cmd)
            # need to set locale encoding because non-ascii characters (eg: Ğ)
            args = convert_cmd.encode(locale.getpreferredencoding())

            try:
                # p = subprocess.Popen(args, shell=True)
                # p.communicate()
                subprocess.check_call(args, shell=True)
            except subprocess.CalledProcessError as err:
                self._log.error(err)
                raise err
