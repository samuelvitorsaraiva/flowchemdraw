from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT

from matplotlib.figure import Figure

from flowchemdraw.utils.drawclass import drawobject

from flowchemdraw.utils.constantes import *

import numpy as np

#plt.style.use('dark_background')

class mplwidget_set(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        self.Main_Window = None

        self.axes.set_xlim(0, SPACE_GRID_FIG)
        self.axes.set_ylim(0, SPACE_GRID_FIG)

        self.axes.set_axis_off()

        #self.axes.grid(True)

        # Connect the mouse events to handlers
        self.mpl_connect('button_press_event', self.on_mouse_press)
        self.mpl_connect('button_release_event', self.on_mouse_release)
        self.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.mpl_connect('scroll_event', self.on_mouse_scroll)

        self.move_componets = {'actived': False}

        self.draw_connections = {'actived': False, 'line_connection': None, 'line_data': [[], []],
                                 'vertical': False, 'inflexion': True}

        self.component = None

        self.grid_draw()

    def grid_draw(self):
        for n in range(2*SPACE_GRID_FIG):
            self.axes.plot([n/2]*SPACE_GRID_FIG*2, np.linspace(0, SPACE_GRID_FIG, 2*SPACE_GRID_FIG), "o", markersize=1, color='k', alpha=0.2)
        self.draw()

    def on_mouse_press(self, event):
        if event.inaxes:

            if event.button == 1:
                print('mouse 1')
            elif event.button == 2:
                print('mouse 2')
            elif event.button == 3:
                print('mouse 3')

    def on_mouse_release(self, event):
        if event.inaxes:
            print('release')

    def on_mouse_move(self, event):
        ...

    def on_mouse_scroll(self, event):
        if event.inaxes:
            print(f'Mouse scrolled at ({event.xdata}, {event.ydata}) with step {event.step}')
