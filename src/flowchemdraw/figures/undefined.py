from flowchemdraw.utils.drawclass import components
import matplotlib.patches as patches
from matplotlib.figure import Figure

class undefined(components):

    type_object = 'others'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5),  name: str = 'undefined'):

        super().__init__(ax=ax, position=pos, type_object=undefined.type_object, name=name, parent=self)

        self.build()

    def build(self):

        r = self.dimention + 0.2
        pos = (self.position[0] - r / 2, self.position[1] - r / 2)
        square = patches.Rectangle(pos, r, r, edgecolor='black', facecolor='none', alpha=1)
        self.add_part(self.ax.add_patch(square))

        self._putname_(pos[0]+r/2, pos[1]-r/5)

        self.connection_points = [(self.position[0] - r/2, self.position[1]),
                                  (self.position[0] + r/2, self.position[1]),
                                  (self.position[0], self.position[1] - r/2),
                                  (self.position[0], self.position[1] + r/2)]