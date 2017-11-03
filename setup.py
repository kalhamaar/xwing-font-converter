#!/usr/bin/env python

from setuptools import setup, find_packages

from xwing_font_converter import xwing_font_converter

setup(name=xwing_font_converter.__prog_name__,
      version=xwing_font_converter.__version__,
      description=xwing_font_converter.__description__,
      author=xwing_font_converter.__author__,
      author_email='kalhamaar@hotmail.fr',
      url=xwing_font_converter.__url__,
      classifiers=[
          "Programming Language :: Python",
          "Development Status :: 1 - Planning",
          "License :: Apache 2.0",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Topic :: Font",
      ],
      packages=find_packages(),
      # include_package_data=True,
      entry_points={
          'console_scripts': [
              'xwing-font-converter = xwing_font_converter.xwing_font_converter:main',
              'xwing-font-converter-gui = xwing_font_converter.xwing_font_converter_gui:main',
          ],
      },
      )
