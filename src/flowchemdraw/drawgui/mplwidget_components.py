from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

from flowchemdraw.utils.constantes import *

#plt.style.use('dark_background')


from flowchemdraw.utils.manage_class import import_class

class mplwidget_components(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        self.main_widget = None

        self.axes.set_xlim(0, 2)
        self.axes.set_ylim(0, 2)

        self.axes.set_axis_off()

    def draw_component(self, name):

        if name in DRAW_DEVICES_CORRESPONDENT.keys():

            name = DRAW_DEVICES_CORRESPONDENT[name]

        self.axes.clear()
        self.axes.set_axis_off()
        dev = import_class('flowchemdraw.figures', name)
        if dev == None:
            dev = import_class('flowchemdraw.figures', 'undefined')
        obj = dev(self.axes, pos=(1, 1))
        for p in obj.connection_points:
            self.axes.plot(p[0], p[1], 'x', color='r')
        self.draw()






