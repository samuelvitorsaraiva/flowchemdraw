from matplotlib.figure import Figure
import matplotlib.patches as patches
from flowchemdraw.utils import math
import numpy as np

from PyQt5.QtWidgets import QMessageBox

from flowchemdraw.utils.constantes import *

class drawobject:

    def __init__(self, type_object: str = 'connections', position: (float, float) = (0, 0), name: str = ''):

        self.position = position

        self.type_object = type_object

        self.name = name

        self.parts = []

        self.actived_square_action: Figure | None = None

        self.additional_configuration = {}

        self.operation = False

        self.operation_part = []

        self.warning_part = []

    def add_part(self, part):

        self.parts.append(part)

    def remove_draw(self) -> None:
        for part in self.parts:
            part.remove()

    def active_draw(self, actived: bool) -> None:
        if self.type_object == 'connections':
            if actived:
                for part in self.parts:
                    try:
                        part.set_color('blue')
                    except:
                        part.set_edgecolor('blue')
            else:
                for part in self.parts:
                    try:
                        part.set_color('k')
                    except:
                        part.set_edgecolor('k')
        else:
            if actived:
                pos = (self.position[0] - PATTERN_DIMENSION,
                       self.position[1] - PATTERN_DIMENSION)

                square = patches.Rectangle(pos, 2 * PATTERN_DIMENSION, 2 * PATTERN_DIMENSION, edgecolor='blue',
                                           fill=False, alpha=0.5)

                self.actived_square_action = self.ax.add_patch(square)

            else:
                if self.actived_square_action != None:

                    self.actived_square_action.remove()

                self.actived_square_action = None

    def operation_set(self, **kwargs):
        ...

class connections(drawobject):

    def __init__(self, ax: Figure, type_object: str = 'connections', position: (float, float) = (0, 0), name: str = ''):

        super().__init__(type_object=type_object, position=position, name=name)

        self.ax = ax

        self.fator = 0

    def operation_set(self, rate=0.2, orientation=1, operation=False):

        self.operation = operation

        if not self.operation:
            return

        c = self.additional_configuration

        if self.warning_part:
            self.warning_part[0].remove()

        try:

            r = rate / (c['DI'] ** 2 * np.pi * c['lenght'])

        except:
            r = 0.05
            #msg = QMessageBox()
            #msg.setWindowTitle("Warning")
            #msg.setText(f"Parameters of {self.name} need to be defined")
            #msg.setIcon(QMessageBox.Critical)
            #msg.exec_()
            #return

        if True:

            self.fator += r

            if self.fator >= 1:

                self.fator = r

                for v in self.operation_part:
                    v.remove()

                self.operation_part = []

            if orientation == -1:

                x, y = self.parts[-1].get_xdata()[::-1], self.parts[-1].get_ydata()[::-1]

            else:

                x, y = self.parts[-1].get_xdata(), self.parts[-1].get_ydata()

            # spacing of arrows
            aspace = .5  # good value for scale of 1
            aspace *= 1

            # r is the distance spanned between pairs of points
            r = [0]
            for i in range(1, len(x)):
                dx = x[i] - x[i - 1]
                dy = y[i] - y[i - 1]
                r.append(np.sqrt(dx * dx + dy * dy))
            r = np.array(r)

            # rtot is a cumulative sum of r, it's used to save time
            rtot = []
            for i in range(len(r)):
                rtot.append(r[0:i].sum())
            rtot.append(r.sum())

            arrowData = []  # will hold tuples of x,y,theta for each arrow
            arrowPos = 0  # current point on walk along data
            rcount = 1
            while arrowPos < r.sum() * self.fator:
                x1, x2 = x[rcount - 1], x[rcount]
                y1, y2 = y[rcount - 1], y[rcount]
                da = arrowPos - rtot[rcount]
                theta = np.arctan2((x2 - x1), (y2 - y1))
                ax = np.sin(theta) * da + x1
                ay = np.cos(theta) * da + y1
                arrowData.append((ax, ay, theta))
                arrowPos += aspace
                while arrowPos > rtot[rcount + 1]:
                    rcount += 1
                    if arrowPos > rtot[-1]:
                        break

            # could be done in above block if you want
            for a_x, a_y, theta in arrowData:
                # use aspace as a guide for size and length of things
                # scaling factors were chosen by experimenting a bit
                self.operation_part.append(self.ax.arrow(a_x,
                                                         a_y,
                                                         np.sin(theta) * aspace / 10,
                                                         np.cos(theta) * aspace / 10,
                                                         head_width=aspace / 8,
                                                         fc='k',
                                                         ec='k',
                                                         lw=3,
                                                         head_length=0.02,
                                                         overhang=0.5,
                                                         length_includes_head=True,
                                                         clip_on=False))

class components(drawobject):

    def __init__(self, ax: Figure, position: (float, float), type_object: str = 'devices', name: str = '', parent=None):

        super().__init__(type_object, position=position, name=name)

        self.ax = ax

        self.dimention = PATTERN_DIMENSION

        self.actived = False

        self.actived_to_connect = False

        self.parent = parent

        self.connection_points = []

    def _putname_(self, x, y, where='below'):

        if where == 'below':
            pos = self.position[1] - 1.5 * PATTERN_DIMENSION
        else:
            pos = self.position[1] + 1.5 * PATTERN_DIMENSION

        self.add_part(self.ax.text(self.position[0], pos, self.name, fontsize=8,
                                   bbox=dict(facecolor='red', alpha=0.25),
                                   horizontalalignment='center'))

    def _rename_(self, new):
        self.name = new
        self.set_position(new_pos=self.position)

    def set_position(self, new_pos: (float, float)) -> None:
        '''

        :param new_pos:
        :return:
        '''
        self.remove_draw()
        self.parent.parts = []
        self.position = new_pos
        self.settup_connections()
        self.build()

    def square_activation_draw(self, active: bool) -> None:

        if active:
            pos = (self.position[0] - PATTERN_DIMENSION,
                   self.position[1] - PATTERN_DIMENSION)

            square = patches.Rectangle(pos, 2 * PATTERN_DIMENSION, 2 * PATTERN_DIMENSION, edgecolor='red', fill=False, alpha=0.5)

            self.actived_square = self.ax.add_patch(square)

            self.actived = active

        else:
            self.actived_square.remove()
            self.actived = active

    def square_activation_connect(self, active: bool) -> None:

        if active:
            pos = (self.position[0] - PATTERN_DIMENSION,
                   self.position[1] - PATTERN_DIMENSION)

            square = patches.Rectangle(pos, 2 * PATTERN_DIMENSION, 2 * PATTERN_DIMENSION, edgecolor='g', fill=False, alpha=0.5)

            self.actived_square_connect = self.ax.add_patch(square)

            self.actived_to_connect = active

        else:
            self.actived_square_connect.remove()
            self.actived_to_connect = active

    def get_nearby_connection(self, pos) -> tuple:

        dist = 1e3
        point = self.connection_points[1]['position']
        if len(self.connection_points) > 1:
            for c in self.connection_points.values():
                dist_n = math.dist_points(c['position'], pos)
                if dist_n < dist:
                    dist = dist_n
                    point = c['position']
            return point
        else:
            return self.connection_points[1]['position']

    def build(self):
        ...

    def settup_connections(self, **kwargs):
        rp = 0
        if kwargs:
            rp = kwargs['r_plus']
        r = self.dimention / 2 + rp
        self.connection_points = {1: {'name': None, 'pairs': [2], 'position': (self.position[0] - r, self.position[1])},
                                  2: {'name': None, 'pairs': [1], 'position': (self.position[0] + r, self.position[1])}}


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 5))
    ob = connections(ax)
    ob.add_part(ax.plot([1, 2, 2], [1, 1, 2])[0])
    ob.additional_configuration['DI'] = 0.1
    ob.additional_configuration['lenght'] = 10
    ob.operation = True
    ob.operation_set()
    plt.show()