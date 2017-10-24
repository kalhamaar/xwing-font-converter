import re
import os

from logger import get_logger


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
        self.init_font_converter()

    def init_font_converter(self):
        """
        Check if given files are correct and create output file if necessary

        :return: None
        """

        if not os.path.exists(self._map_file_path):
            self._log.error('MISSING MAP FILE (.scss)')

        if not os.path.exists(self._ttf_file_path):
            self._log.error('MISSING TTF FILE (.ttf) !')

        if not os.path.exists(self._output_folder):
            os.mkdir(self._output_folder)

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
        # then parse it to get keycode

        for match in matches:
            element_name = match.group(1).lstrip()
            element_code = match.group(2).lstrip()

            # because icons are in ascii hexa
            if str(element_code).startswith('\\00'):
                element_code = element_code.replace('\\', '').decode('hex')[1:]

            elif str(element_code).startswith('\\01'):
                # skip obstacles for now
                continue

            # for better quote enclosing insert quoting here
            if element_code == "'":
                element_code = "\"" + element_code + "\""
            else:
                element_code = "'" + element_code + "'"

            self._element_map[element_name] = element_code

    def convert_2_images(self, color='black', point_size=50, size=72):
        """
        Convert all elements in map into images according given options

        :param color:
        :param point_size:
        :param size:
        :return:
        """
        # now convert TTF to images
        for element in self._element_map:
            self._log.debug("Processing '{element}' (keycode: {keycode}) ...".
                            format(element=element, keycode=self._element_map[element]))

            output_file = os.path.join(self._output_folder, "{ship}.png".format(ship=element))
            convert_cmd = "convert -font {ttf_file} -background none -fill {color} -gravity center " \
                          "-pointsize {pointsize} -size {size}x{size} caption:{keycode} {output}". \
                format(ttf_file=self._ttf_file_path,
                       color=color,
                       pointsize=point_size,
                       size=size,
                       keycode=self._element_map[element],
                       output=output_file)

            os.system(convert_cmd)
