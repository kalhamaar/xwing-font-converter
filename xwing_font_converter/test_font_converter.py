"""
Unit testing of FontConverter class
"""
import logging
import os
import shutil
import time
import unittest

from font_converter import FontConverter


class TestFontConverter(unittest.TestCase):

    def setUp(self):
        super(TestFontConverter, self).setUp()

        # disable log during tests
        logging.disable(logging.CRITICAL)

        map_file = os.path.join('resources', 'ships-map.json')
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
        self.fc.convert_2_images(color='black', point_size=50, file_format='gif')
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

    def test_trim_images(self):
        self.fc.init_font_converter()
        self.fc.get_elements_from_map()
        self.fc.convert_2_images(color='black', point_size=50, file_format='gif')
        files_list = os.listdir(self._output_folder)
        old_date = {}
        for f_name in files_list:
            f_stat = os.stat(os.path.join(self._output_folder, f_name))
            old_date[f_name] = f_stat.st_atime
        self.fc.trim_images()
        time.sleep(1)
        new_date = {}
        for f_name in files_list:
            f_stat = os.stat(os.path.join(self._output_folder, f_name))
            new_date[f_name] = f_stat.st_atime
        diff = set(old_date.values()).intersection(new_date.values())
        self.assertEqual(len(diff), 0, "No updated date found, mean image not updated")

    def resize_images(self):
        self.fc.init_font_converter()
        self.fc.get_elements_from_map()
        self.fc.convert_2_images(color='black', point_size=50, file_format='gif')
        files_list = os.listdir(self._output_folder)
        old_date = {}
        for f_name in files_list:
            f_stat = os.stat(os.path.join(self._output_folder, f_name))
            old_date[f_name] = f_stat.st_atime
        self.fc.resize_images(20)
        time.sleep(1)
        new_date = {}
        for f_name in files_list:
            f_stat = os.stat(os.path.join(self._output_folder, f_name))
            new_date[f_name] = f_stat.st_atime
        diff = set(old_date.values()).intersection(new_date.values())
        self.assertEqual(len(diff), 0, "No updated date found, mean image not updated")

    def tearDown(self):
        shutil.rmtree(self._output_folder)


if __name__ == '__main__':
    unittest.main()
