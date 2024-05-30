from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

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
        self.axes.clear()
        self.axes.set_axis_off()
        dev = import_class('flowchemdraw.figures', name)
        dev(self.axes, pos=(1, 1))
        self.draw()






