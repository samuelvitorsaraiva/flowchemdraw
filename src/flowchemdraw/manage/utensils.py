from flowchemdraw.manage.component import component
from flowchemdraw.utils.drawclass import drawobject

class utensils_class(component):
    def __init__(self, parent, name: str, class_name: str, position: (float, float), draw: drawobject):

        super().__init__(parent, name=name, position=position, draw=draw)

        self.class_name = class_name
