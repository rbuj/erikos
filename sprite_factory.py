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
import os.path

from sprites import *

#
# class for defining individual cards
#
class Sprite:
    def __init__(self, tw, name, x, y, w, h, name_label=False):
        # create sprite from svg file
        self.spr = sprNew(tw, x, y,
                          self.load_image(tw.path,name,w*tw.scale,h*tw.scale))
        if name_label is True:
            self.spr.label = name
        else:
            self.spr.label = ""

    def draw_sprite(self, layer=1000):
        setlayer(self.spr, layer)
        draw(self.spr)

    def load_image(self, file, name, w, h):
        return gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(file + 
                                                                 name + 
                                                                 '.svg'),
                                                    w, h)

