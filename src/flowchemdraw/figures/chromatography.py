import numpy as np
from flowchemdraw.utils.drawclass import components
from matplotlib.figure import Figure
import matplotlib.patches as patches

PATTERN_DIMENSION = 1
class chromatography(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'chromatography'):

        super().__init__(ax=ax, position=pos, type_object=chromatography.type_object, name=name, parent=self)

        self.settup_connections(r_plus=0.1)

        self.build()

    def build(self):

        r = self.dimention + 0.2
        pos = (self.position[0] - r / 2, self.position[1] - r / 2)
        square = patches.Rectangle(pos, r, r, edgecolor='black', facecolor='none', alpha=1)
        self.add_part(self.ax.add_patch(square))

        x = np.linspace(self.position[0] - 4 * r / 10, self.position[0] + 4 * r / 10, 4)
        arg = self.position[1] - r / 2 + np.random.rand(4) * r
        for i in range(4):
            self.add_part(self.ax.plot([x[i]] * 2, [self.position[1] - r / 2, arg[i]], color='k')[0])

        self.add_part(self.ax.plot(x, arg, 'o', color='k')[0])

        self._putname_(pos[0] + r / 2, pos[1] - r / 5)