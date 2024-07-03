import numpy as np
from flowchemdraw.utils.drawclass import components
import matplotlib.patches as patches
from matplotlib.figure import Figure

class flowreactor(components):

    type_object = 'others'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'flowreactor'):

        super().__init__(ax=ax, position=pos, type_object=flowreactor.type_object, name=name, parent=self)

        self.settup_connections(r_plus=0.1)

        self.build()

    def build(self):

        r = self.dimention + 0.2
        pos = (self.position[0] - r / 2, self.position[1] - r / 2)
        square = patches.Rectangle(pos, r, r, edgecolor='black', facecolor='red', alpha=0.5)
        self.add_part(self.ax.add_patch(square))
        x = np.linspace(pos[0]+r/8, pos[0] + 0.883 * r, 100)
        self.add_part(self.ax.plot(x, 0.5 * self.dimention * np.sin(50*(x-pos[0]+r/8)) + pos[1] + r / 2, color='k')[0])

        self._putname_(pos[0] + r / 2, pos[1] - r / 5)