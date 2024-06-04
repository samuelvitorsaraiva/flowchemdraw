from matplotlib.figure import Figure
import matplotlib.patches as patches
from flowchemdraw.utils import math
from abc import ABC, abstractmethod

PATTERN_DIMENSION = 1

class drawobject:

    def __init__(self, type_object: str, position: (float, float) = (0, 0)):

        self.position = position

        self.type_object = type_object

        self.parts = []

    def add_part(self, part):

        self.parts.append(part)

    def remove_draw(self) -> None:
        for part in self.parts:
            part.remove()


    def active_draw(self, actived: bool) -> None:
        if actived:
            for part in self.parts:
                try:
                    part.set_color('red')
                except:
                    part.set_edgecolor('red')
        else:
            for part in self.parts:
                try:
                    part.set_color('k')
                except:
                    part.set_edgecolor('k')

    def build(self):
        pass

class components(drawobject):

    def __init__(self, ax: Figure, position: (float, float), type_object: str = 'devices', name: str = '', parent=None):

        super().__init__(type_object, position=position)

        self.ax = ax

        self.dimention = PATTERN_DIMENSION

        self.actived = False

        self.actived_to_connect = False

        self.parent = parent

        self.connection_points = [None]

        self.name = name

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
        point = self.connection_points[0]
        if len(self.connection_points) > 1:
            for c in self.connection_points:
                dist_n = math.dist_points(c, pos)
                if dist_n < dist:
                    dist = dist_n
                    point = c
            return point
        else:
            return self.connection_points[0]

    def build(self):
        pass

