#!/usr/bin/env python
# coding: utf-8
"""
X-Wing font to image converter GUI

:author: KalHamaar
:date: 03/11/2017

Used to convert xwing geordanr's font into png images.

:seealso: https://github.com/geordanr/xwing-miniatures-font
"""
import gtk
from os.path import basename, join, exists

import xwing_font_converter
from font_converter import AVAILABLE_COLORS, AVAILABLE_FILE_FORMATS, FontConverter, DEFAULT_SIZE, DEFAULT_POINTSIZE
from logger import get_logger

__all__ = ['main']


class XWingFontConvertGui(gtk.Window):

    def __init__(self):
        super(XWingFontConvertGui, self).__init__()

        # to reduce init redundancy
        self.__entry_types = {'map': self.on_open_map_file_clicked,
                              'font': self.on_open_font_file_clicked,
                              'output': self.on_select_output_folder_clicked}

        # set default params
        self._color = AVAILABLE_COLORS[0]
        self._point_size = DEFAULT_POINTSIZE
        self._size = DEFAULT_SIZE
        self._resize_width = False
        self._trim = False
        self._file_format = AVAILABLE_FILE_FORMATS[0]

        self._map_entry = None
        self._font_entry = None
        self._output_entry = None

        self.logger = get_logger(loglevel='DEBUG')

        # create a new window
        self.set_resizable(False)
        self.set_title("XWing Font Converter")

        self.set_icon_from_file(self.get_logo())

        self.set_position(gtk.WIN_POS_CENTER)

        main_vbox = gtk.VBox(False, 0)  # main vertical alignment box
        valign = gtk.Alignment(0, 1, 0, 0)
        main_vbox.pack_start(valign)

        # ---------- Menu bar ----------
        mb = gtk.MenuBar()
        filemenu = gtk.Menu()
        filem = gtk.MenuItem("File")
        filem.set_submenu(filemenu)

        about = gtk.MenuItem("About")
        about.connect("activate", self.on_about_clicked)
        filemenu.append(about)

        exit_m = gtk.MenuItem("Exit")
        exit_m.connect("activate", gtk.main_quit)
        filemenu.append(exit_m)
        mb.append(filem)
        main_vbox.pack_start(mb, False, False, 0)

        # ---------- Couples entry + button ----------

        main_vbox.pack_start(self.init_file_selection('map'), False, False, 3)
        main_vbox.pack_start(self.init_file_selection('font'), False, False, 3)
        main_vbox.pack_start(self.init_file_selection('output'), False, False, 3)

        self.statusbar = gtk.Statusbar()  # Need to declare status bar here to avoid AttributeError on boxes init

        # ---------- Combo boxes ----------

        c_hbox = gtk.HBox(False, 5)  # horizontal alignment box for combo boxes

        # trim
        trim_check = gtk.CheckButton("Trim images")
        trim_check.connect("toggled", self.on_trim_checked)
        c_hbox.add(trim_check)

        # resize
        resize_width = gtk.CheckButton("Resize on Width")
        resize_width.connect("toggled", self.on_resize_width_checked)
        c_hbox.add(resize_width)

        # colors
        color_box = gtk.combo_box_new_text()
        color_box.connect("changed", self.on_color_changed)
        for color in AVAILABLE_COLORS:
            color_box.append_text(color)
        color_box.set_active(0)
        c_hbox.add(color_box)

        # pointsize
        pointsize_box = gtk.combo_box_new_text()
        pointsize_box.connect("changed", self.on_pointsize_changed)
        for ps in range(36, 98, 2):
            pointsize_box.append_text(str(ps))
        pointsize_box.set_active(7)
        c_hbox.add(pointsize_box)

        # size
        size_entry = gtk.Entry(20)
        size_entry.set_max_length(3)
        size_entry.set_width_chars(3)
        size_entry.connect("key-release-event", self.on_size_changed)
        size_entry.set_text(str(DEFAULT_SIZE))

        c_hbox.add(size_entry)

        # format
        format_box = gtk.combo_box_new_text()
        format_box.connect("changed", self.on_format_changed)
        for fmt in AVAILABLE_FILE_FORMATS:
            format_box.append_text(fmt)
        format_box.set_active(0)
        c_hbox.add(format_box)

        c_halign = gtk.Alignment(1, 0, 0, 0)
        c_halign.add(c_hbox)
        main_vbox.pack_start(c_halign, False, False, 0)

        # ---------- add RUN and Close button ----------

        buttons_hbox = gtk.HBox(False, 5)
        run_button = gtk.Button(stock=gtk.STOCK_EXECUTE)
        run_button.set_size_request(70, 30)
        run_button.connect("clicked", self.on_run_clicked)

        close_button = gtk.Button(stock=gtk.STOCK_CLOSE)
        close_button.connect("clicked", gtk.main_quit)

        buttons_hbox.add(run_button)
        buttons_hbox.add(close_button)

        b_halign = gtk.Alignment(1, 0, 0, 0)
        b_halign.add(buttons_hbox)
        main_vbox.pack_start(b_halign, False, False, 3)

        # ----- status bar ---
        self.statusbar.push(0, "Ready")
        main_vbox.pack_start(self.statusbar, False, False, 0)

        self.add(main_vbox)
        self.connect("destroy", gtk.main_quit)
        self.show_all()

    def init_file_selection(self, entry_type):

        # map file selection
        hbox = gtk.HBox(False, 5)
        hbox.add(gtk.Label(entry_type))

        entry = gtk.Entry()
        entry.set_width_chars(80)
        entry.set_editable(False)
        entry.set_name(entry_type)

        # ugly but to reduce redundancy ....
        setattr(self, "_{}_entry".format(entry_type), entry)
        hbox.add(entry)

        button = gtk.Button(stock=gtk.STOCK_OPEN)
        button.connect("clicked", self.__entry_types[entry_type])
        button.set_name(entry_type)
        hbox.add(button)

        halign = gtk.Alignment(1, 0, 0, 0)
        halign.add(hbox)
        return halign

    def on_open_map_file_clicked(self, widget):
        self._map_entry.set_text(self.on_open_file_clicked(widget))

    def on_open_font_file_clicked(self, widget):
        self._font_entry.set_text(self.on_open_file_clicked(widget))

    def on_select_output_folder_clicked(self, widget):
        self._output_entry.set_text(self.on_select_folder_clicked(widget))

    def on_trim_checked(self, widget):
        self._trim = widget.get_active()
        text = "Trim status changed to: {}".format(self._trim)
        self.logger.debug(text)
        self.statusbar.push(0, text)

    def on_resize_width_checked(self, widget):
        self._resize_width = widget.get_active()
        text = "Resize on Width status changed to: {}".format(self._trim)
        self.logger.debug(text)
        self.statusbar.push(0, text)

    def on_color_changed(self, widget):
        self._color = widget.get_active_text()
        text = "Color {} chosen".format(self._color)
        self.logger.debug(text)
        self.statusbar.push(0, text)

    def on_pointsize_changed(self, widget):
        self._point_size = widget.get_active_text()
        self.logger.debug("point size changed to {}".format(self._point_size))
        self.statusbar.push(0, "point size changed to {}".format(self._point_size))

    def on_size_changed(self, widget, event):
        try:
            val = int(widget.get_text())
            self._size = val
            widget.set_text(str(val))
            self.logger.debug("image size changed to {ps}x{ps}px".format(ps=self._size))
            self.statusbar.push(0, "image size changed to {ps}x{ps}px".format(ps=self._size))
        except ValueError:
            widget.set_text('')
            self.logger.warning("Wrong size, please enter integer format")
            self.statusbar.push(0, "Wrong size, please enter integer format")

    def on_format_changed(self, widget):
        self._file_format = widget.get_active_text()
        self.logger.debug("{} file format chosen".format(self._file_format))
        self.statusbar.push(0, "{} file format chosen".format(self._file_format))

    def on_run_clicked(self, widget):

        widget.set_sensitive(False)  # disable button temporary
        for entry_name in self.__entry_types:
            # ugly but to reduce copy/paste ....
            entry = getattr(self, "_{}_entry".format(entry_name))
            if entry.get_text() is "":
                self.raise_error_message_dialog("Error loading {} file".format(entry_name))
                widget.set_sensitive(True)  # re-enable button
                return

        self.logger.info('Starting extraction of {}'.format(basename(self._font_entry.get_text())))

        self.logger.debug("Map file: {map_file_path} TTF File: {ttf_file_path} Output folder: {output_folder}"
                          .format(map_file_path=self._map_entry.get_text(),
                                  ttf_file_path=self._font_entry.get_text(),
                                  output_folder=self._output_entry.get_text()))

        fc = FontConverter(map_file_path=self._map_entry.get_text(),
                           ttf_file_path=self._font_entry.get_text(),
                           output_folder=self._output_entry.get_text())

        if not fc.init_font_converter():
            self.raise_error_message_dialog("Unable to initialize font converter properly")
            widget.set_sensitive(True)  # re-enable button
            return

        fc.get_elements_from_map()
        self.logger.debug("Converting {point_size} point size font to {color} {size}x{size} {file_format} images"
                          .format(point_size=self._point_size,
                                  color=self._color,
                                  size=self._size,
                                  file_format=self._file_format))

        fc.convert_2_images(point_size=self._point_size,
                            color=self._color,
                            file_format=self._file_format)

        if self._trim:
            fc.trim_images()

        if self._size != DEFAULT_SIZE:
            fc.resize_images(self._size)

        self.logger.info("Extraction done, files available in: {}".format(self._output_entry.get_text()))
        widget.set_sensitive(True)  # re-enable button

    def on_about_clicked(self, widget):

        about = gtk.AboutDialog()
        about.set_program_name(xwing_font_converter.__prog_name__)
        about.set_version(xwing_font_converter.__version__)
        about.set_copyright("(c) {}".format(xwing_font_converter.__author__))
        about.set_comments(xwing_font_converter.__description__)
        about.set_website(xwing_font_converter.__url__)
        about.set_logo(gtk.gdk.pixbuf_new_from_file(self.get_logo()))
        about.run()
        about.destroy()

    def raise_error_message_dialog(self, message):
        md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                               gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()

    def on_open_file_clicked(self, widget):
        widget.set_sensitive(False)  # disable button temporary
        filename = ''
        dialog = gtk.FileChooserDialog("Select file ...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        f_filter = gtk.FileFilter()
        f_filter.set_name("All files")
        f_filter.add_pattern("*")
        dialog.add_filter(f_filter)

        if widget.name == "font":
            f_filter = gtk.FileFilter()
            f_filter.set_name("Font")
            f_filter.add_mime_type("application/x-font-ttf")
            f_filter.add_pattern("*.ttf")
            dialog.add_filter(f_filter)
            dialog.set_filter(f_filter)

        elif widget.name == "map":
            j_filter = gtk.FileFilter()
            j_filter.set_name("Json")
            j_filter.add_mime_type("text/plain")
            j_filter.add_pattern("*.json")
            dialog.add_filter(j_filter)
            dialog.set_filter(j_filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            self.logger.debug("{} selected".format(filename))
            self.statusbar.push(0, "{} selected".format(basename(filename)))

        elif response == gtk.RESPONSE_CANCEL:
            self.logger.warning('Closed, no file selected')
            self.statusbar.push(1, 'Closed, no file selected')

        dialog.destroy()
        widget.set_sensitive(True)  # re-enable button
        return filename

    def on_select_folder_clicked(self, widget):
        widget.set_sensitive(False)  # disable button temporary
        folder_name = ''
        dialog = gtk.FileChooserDialog("Select folder ...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            folder_name = dialog.get_filename()
            self.logger.debug("'{}' selected".format(folder_name))
            self.statusbar.push(1, "'{}' folder selected".format(basename(folder_name)))

        elif response == gtk.RESPONSE_CANCEL:
            self.logger.warning('Closed, no folder selected')
            self.statusbar.push(1, 'Closed, no folder selected')

        dialog.destroy()
        widget.set_sensitive(True)  # re-enable button
        return folder_name

    @staticmethod
    def get_logo():

        logo_path = join('resources', 'index.gif')
        import pkg_resources
        if exists(logo_path):
            # we are in source exec
            return logo_path
        elif pkg_resources.resource_exists(__name__, logo_path):
            return pkg_resources.resource_filename(__name__, logo_path)
        else:
            print("Unable to find logo resource, exiting ...")
            exit(-1)


def main():
    XWingFontConvertGui()
    gtk.main()
    return 0


if __name__ == "__main__":
    main()
