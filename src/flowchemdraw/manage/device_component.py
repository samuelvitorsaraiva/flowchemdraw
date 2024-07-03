from flowchemdraw.manage.component import component
from flowchemdraw.utils.drawclass import drawobject

class device_component_class(component):

    def __init__(self, parent, name: str, class_name: str, position: (float, float), draw: drawobject):
        super().__init__(parent, name=name, position=position, draw=draw)

        self.class_name = class_name

        if len(self.class_name.split('/')) > 1:
            self.class_name_device = self.class_name.split('/')[0]
            self.name_device = self.name.split('/')[0]
        else:
            self.class_name_device = self.class_name
            self.name_device = self.name

        self.configuration_block = {'device': {self.name_device: {'type': self.class_name_device}}}

    def update_configuration_file(self, new: dict):

        self.configuration_block['device'][self.name_device] = new
