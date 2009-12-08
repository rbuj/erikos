# -*- coding: utf-8 -*-
#Copyright (c) 2009, Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import sugar
from sugar.activity import activity
try: # 0.86+ toolbar widgets
    from sugar.bundle.activitybundle import ActivityBundle
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton
    from sugar.graphics.toolbarbox import ToolbarBox
    from sugar.graphics.toolbarbox import ToolbarButton
except ImportError:
    pass
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar.datastore import datastore

from gettext import gettext as _
import locale
import os.path

import logging
_logger = logging.getLogger("erikos-activity")

from sprites import *
import window

#
# Sugar activity
#
class ErikosActivity(activity.Activity):

    def __init__(self, handle):
        super(ErikosActivity,self).__init__(handle)

        try:
            # Use 0.86 toolbar design
            toolbar_box = ToolbarBox()

            # Buttons added to the Activity toolbar
            activity_button = ActivityToolbarButton(self)
            toolbar_box.toolbar.insert(activity_button, 0)
            activity_button.show()

            # Play Button
            self.play = ToolButton( "media-playback-start" )
            self.play.set_tooltip(_('Play'))
            self.play.props.sensitive = True
            self.play.connect('clicked', self._play_cb)
            toolbar_box.toolbar.insert(self.play, -1)
            self.play.show()

            separator = gtk.SeparatorToolItem()
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)

            # Label for showing level
            self.level_label = gtk.Label("%s %d" % (_("Level"),1))
            self.level_label.show()
            level_toolitem = gtk.ToolItem()
            level_toolitem.add(self.level_label)
            toolbar_box.toolbar.insert(level_toolitem,-1)

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)

            # The ever-present Stop Button
            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>Q'
            toolbar_box.toolbar.insert(stop_button, -1)
            stop_button.show()

            self.set_toolbar_box(toolbar_box)
            toolbar_box.show()

        except NameError:
            # Use pre-0.86 toolbar design
            self.toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(self.toolbox)

            self.projectToolbar = ProjectToolbar(self)
            self.toolbox.add_toolbar( _('Project'), self.projectToolbar )

            self.toolbox.show()

        # Create a canvas
        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width(), \
                                gtk.gdk.screen_height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        # Initialize the canvas
        self.tw = window.new_window(canvas, \
                                    os.path.join(activity.get_bundle_path(), \
                                                 'images/'), \
                                    self)
        self.tw.activity = self

        # Read the level from the Journal
        try:
            tw,level = int(self.metadata['level'])
        except:
            pass

    def _play_cb(self, button):
        window.play_the_game(self.tw)
        return True

    """
    Write the slider positions to the Journal
    """
    def write_file(self, file_path):
        _logger.debug("Write level: " + str(self.tw.level))
        self.metadata['level'] = self.tw.level

#
# Project toolbar for pre-0.86 toolbars
#
class ProjectToolbar(gtk.Toolbar):

    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # Play button
        self.activity.play = ToolButton( "media-playback-start" )
        self.activity.play.set_tooltip(_('Play'))
        self.activity.play.props.sensitive = True
        self.activity.play.connect('clicked', self.activity._play_cb)
        self.insert(self.activity.play, -1)
        self.activity.play.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # Label for showing play status
        self.activity.level_label = gtk.Label("%s %d" % (_("Level"),1))
        self.activity.level_label.show()
        self.activity.level_toolitem = gtk.ToolItem()
        self.activity.level_toolitem.add(self.activity.level_label)
        self.insert(self.activity.level_toolitem, -1)
        self.activity.level_toolitem.show()
