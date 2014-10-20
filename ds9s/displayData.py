import gtk
import sys
import os
import threading

from matplotlib.figure import Figure as MPLFigure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NaviToolbar


class ThreadFigure(threading.Thread):
    def __init__(self, figure, count):
        threading.Thread.__init__(self)
        self.figure =   figure
        self.count  =   count
    def run(self):
        window  =   gtk.Window()
        # window.connect('destroy', gtk.main_quit)

        window.set_default_size(640, 480)
        window.set_icon_from_file(...)  # provide an icon if you care about the looks

        window.set_title('MPL Figure #{}'.format(self.count))
        window.set_wmclass('MPL Figure', 'MPL Figure')

        vbox    =   gtk.VBox()
        window.add(vbox)

        canvas  =   FigureCanvas(self.figure)
        vbox.pack_start(canvas)

        toolbar =   NaviToolbar(canvas, window)
        vbox.pack_start(toolbar, expand = False, fill = False)

        window.show_all()
        # gtk.main() ... should not be called, otherwise BLOCKING


class Figure(MPLFigure):
    display_count = 0
    def show(self):
        Figure.display_count += 1 
        thrfig = ThreadFigure(self, Figure.display_count)
        thrfig.start()