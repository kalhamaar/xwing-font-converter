#!/usr/bin/env python

from setuptools import setup, find_packages

import xwing_font_converter

setup(name='X-Wing Font Converter',
      version=xwing_font_converter.__version__,
      description='Convert geordanr\'s font into images',
      author='KalHamaar',
      author_email='kalhamaar@hotmail.fr',
      url='https://github.com/kalhamaar/xwing_font_converter',
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'xwing-font-converter = xwing_font_converter.xwing_font_converter:main',
          ],
      },
      )
