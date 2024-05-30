import numpy as np
from flowchemdraw.utils.drawclass import components
import matplotlib.patches as patches

class flowreactor(components):

    def __init__(self, ax, pos=(0.5, 0.5)):

        super().__init__(ax=ax, position=pos, parent=self)

        self.build()

    def build(self):

        r = self.dimention + 0.2
        pos = (self.position[0] - r / 2, self.position[1] - r / 2)
        square = patches.Rectangle(pos, r, r, edgecolor='black', facecolor='red', alpha=0.5)
        self.add_part(self.ax.add_patch(square))
        x = np.linspace(pos[0]+r/8, pos[0] + 0.883 * r, 100)
        self.add_part(self.ax.plot(x, 0.5 * self.dimention * np.sin(50*(x-pos[0]+r/8)) + pos[1] + r / 2, color='k')[0])

        self.connection_points = [(self.position[0] - r/2, self.position[1]),
                                  (self.position[0] + r/2, self.position[1]),
                                  (self.position[0], self.position[1] - r/2),
                                  (self.position[0], self.position[1] + r/2)]