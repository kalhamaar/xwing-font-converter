"""
Unit testing of FontConverter class
"""
import logging
import os
import shutil
import unittest

from font_converter import FontConverter


class TestFontConverter(unittest.TestCase):

    def setUp(self):
        super(TestFontConverter, self).setUp()

        # disable log during tests
        logging.disable(logging.CRITICAL)

        map_file = os.path.join('resources', '_ships-map.scss')
        ttf_file = os.path.join('resources', 'xwing-miniatures-ships.ttf')
        self._output_folder = os.path.join('output', 'unittest')
        self.fc = FontConverter(map_file_path=map_file,
                                ttf_file_path=ttf_file,
                                output_folder=self._output_folder)

    def test_init(self):
        self.assertTrue(self.fc.init_font_converter(), 'Unable to init font converter')
        self.assertTrue(os.path.exists(self._output_folder), 'Unable to create output folder')

    def test_get_element_on_map(self):
        self.fc.init_font_converter()
        self.fc.get_elements_from_map()
        self.assertNotEqual(len(self.fc.element_map), 0, 'Element map should not be empty')

    def test_convert_2_images(self):
        self.fc.init_font_converter()
        self.fc.get_elements_from_map()
        self.fc.convert_2_images(color='black', point_size=50, size=72, file_format='gif')
        self.assertNotEqual(len(os.listdir(self._output_folder)), 0, 'Output folder should not be empty')

    def test_convert_2_images_wrong_color(self):
        self.fc.init_font_converter()
        self.fc.get_elements_from_map()
        with self.assertRaises(AttributeError) as context:
            self.fc.convert_2_images(color='WRONG_COLOR')
        self.assertIn("WRONG_COLOR", context.exception.message, "Should display error message")

    def test_convert_2_images_wrong_format(self):
        self.fc.init_font_converter()
        self.fc.get_elements_from_map()
        with self.assertRaises(AttributeError) as context:
            self.fc.convert_2_images(file_format='jpg')
        self.assertIn("jpg", context.exception.message, "Should display error message")

    def tearDown(self):
        shutil.rmtree(self._output_folder)


if __name__ == '__main__':
    unittest.main()
