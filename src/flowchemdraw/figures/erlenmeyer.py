import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

class erlenmeyer(components):
    def __init__(self, ax: Figure, pos=(0.5, 0.5)):

        super().__init__(ax=ax, position=pos, parent=self)

        self.build()


    def build(self):

        r = self.dimention

        p = self.position

        self.add_part(self.ax.plot([p[0] - r / 2, p[0] - r / 4], [p[1] - r / 2, p[1] + r / 2], color='k')[0])
        self.add_part(self.ax.plot([p[0] + r / 4, p[0] + r / 2], [p[1] + r / 2, p[1] - r / 2], color='k')[0])

        self.add_part(self.ax.plot([p[0] - r / 4, p[0] + r / 4], [p[1] + 1.25 * r] * 2, color='k')[0])
        self.add_part(self.ax.plot([p[0] - r / 4, p[0] + r / 4], [p[1] + 1.25 * r + r / 10] * 2, color='k')[0])
        self.add_part(self.ax.plot([p[0] - r / 4] * 2, [p[1] + r / 2, p[1] + 1.25 * r], color='k')[0])
        self.add_part(self.ax.plot([p[0] + r / 4] * 2, [p[1] + r / 2, p[1] + 1.25 * r], color='k')[0])

        self.connection_points = [(p[0], p[1] + 1.25 * r)]

        phis = np.arange(0, 2 * np.pi, 0.01)
        self.add_part(self.ax.plot(*math.ellipse(0.37 * r, r / 10, phis, pos=p), c='k', ls='-')[0])

        phis = np.arange(0, 2 * np.pi, 0.01)
        self.add_part(self.ax.plot(*math.ellipse(r / 2, r / 10, phis, pos=(p[0], p[1] - r / 2)), c='k', ls='-')[0])

        phis = np.arange(np.pi/2, 3 * np.pi / 2, 0.01)
        self.add_part(
            self.ax.plot(*math.xy(r / 20, phis, pos=(p[0] - r / 4, p[1] + 1.25 * r + r / 20)), c='k',
                         ls='-')[0])
        phis = np.arange(- np.pi / 2, np.pi / 2, 0.01)
        self.add_part(
            self.ax.plot(*math.xy(r / 20, phis, pos=(p[0] + r / 4, p[1] + 1.25 * r + r / 20)),
                         c='k',
                         ls='-')[0])