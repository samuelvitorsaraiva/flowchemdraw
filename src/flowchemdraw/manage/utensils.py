from flowchemdraw.manage.component import component

class utensils(component):
    def __init__(self, name: str, class_name: str, position: (float, float), draw: drawobject):
        super().__init__(name=name, position=position, draw=draw)

