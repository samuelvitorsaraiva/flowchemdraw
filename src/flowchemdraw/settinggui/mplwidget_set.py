from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT

from matplotlib.figure import Figure

from PyQt5.QtWidgets import QMenu

from PyQt5.QtCore import QPoint

from functools import partial

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
        #self.mpl_connect('button_release_event', self.on_mouse_release)
        #self.mpl_connect('motion_notify_event', self.on_mouse_move)
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

            name = self.Main_Window.manage._nearbydevice(pos=(event.xdata, event.ydata))

            if name != '-':

                if event.button == 1:

                    self.Main_Window.tableWidget._update_device(name)

                elif event.button == 2:
                    ...
                elif event.button == 3:

                    if self.Main_Window.manage.components[name].class_name in DRAW_DEVICES_CORRESPONDENT.keys():
                        figure_name = DRAW_DEVICES_CORRESPONDENT[self.Main_Window.manage.components[name].class_name]
                    else:
                        figure_name = self.Main_Window.manage.components[name].class_name


                    if figure_name in COMANDS_PROTOCOLS.keys():

                        menu = QMenu()

                        protocol = menu.addMenu("Protocols")

                        action_protocol = []

                        for key in COMANDS_PROTOCOLS[figure_name].keys():
                            action_protocol.append(protocol.addAction(key))
                            action_protocol[-1].triggered.connect(partial(self.protocoll_call, name, figure_name, key))


                        x = int(event.xdata/(SPACE_GRID_FIG+1) * self.figure.bbox.bounds[-2])
                        y = 100+int(self.figure.bbox.bounds[-1] - event.ydata/(SPACE_GRID_FIG+1) * self.figure.bbox.bounds[-1])
                        menu.exec_(self.Main_Window.mapToGlobal(QPoint(x, y)))

    def on_mouse_scroll(self, event):
        if event.inaxes:
            print(f'Mouse scrolled at ({event.xdata}, {event.ydata}) with step {event.step}')


    def setting(self):
        ...

    def protocoll_call(self, name: str, figure_class: str, protocol: str):

        configuration = dict()

        configuration['Device'] = name

        configuration['command'] = protocol

        configuration['component'] = self.Main_Window.manage.components[name]

        configuration = configuration | COMANDS_PROTOCOLS[figure_class][protocol]

        self.Main_Window.manage_protocol._add_commands(configuration)

        self.Main_Window.treeView.update_protocols()




