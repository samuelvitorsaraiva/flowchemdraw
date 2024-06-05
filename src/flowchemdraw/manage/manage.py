from flowchemdraw.utils.drawclass import drawobject
from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.utils.constantes import *

from PyQt5.QtWidgets import QMessageBox
from matplotlib.figure import Figure
from abc import ABC

class component:

    def __init__(self, name: str, position: (float, float), draw: drawobject):

        self.name = name

        self.position = position

        self.draw = draw

        self.type = draw.type_object


class connection:

    def __init__(self, origen: str, destiny: str, draw: drawobject):

        self.origen = origen

        self.destiny = destiny

        self.draw = draw


class manage:

    def __init__(self, ax: Figure):

        self.components = dict()

        self.connection = dict()

        self.ax = ax


    def _add_component(self, name: str) -> str:

        k = 1
        for dev in self.components.keys():
            if dev.split('_')[0] == name:
                k += 1

        name = name + '_' + str(k)

        for dev in self.components.keys():
            x, y = self.components[dev].position
            if LOCATION_NEW_DEVICES[0] == x and LOCATION_NEW_DEVICES[0] == y:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText("There is a device placed in the designated area to new ones. "
                            "Please move away its device of this area before add new one.")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                return '-'

        dev = import_class('flowchemdraw.figures', name.split('_')[0])
        if dev == None:
            dev = import_class('flowchemdraw.figures', 'undefined')


        self.components[name] = component(name=name,
                                          position=LOCATION_NEW_DEVICES,
                                          draw=dev(self.ax, pos=LOCATION_NEW_DEVICES))

        return name


    def _dell_component(self, name: str) -> list[str]:
        self.components[name].draw.remove_draw()
        self.components.pop(name)

        connection_dell = []
        for key in self.connection.keys():
            if self.connection[key].origen == name or self.connection[key].destiny == name:
                connection_dell.append(key)

        [self._dell_connection(key) for key in connection_dell]

        return connection_dell


    def _move_component(self, name: str, new_pos: (float, float)) -> list[str]:

        self.components[name].position = new_pos
        self.components[name].draw.set_position(new_pos=new_pos)

        connection_dell = []
        for key in self.connection.keys():
            if self.connection[key].origen == name or self.connection[key].destiny == name:
                connection_dell.append(key)

        [self._dell_connection(key) for key in connection_dell]

        return connection_dell


    def _rotate_component(self, angle: float) -> None:
        ...


    def _rename_component(self, new_name: str) -> None:
        ...


    def _isnearby(self, name, pos, active: str = 'active') -> bool:

        x, y = self.components[name].position
        dx = abs(x - pos[0])
        dy = abs(y - pos[1])

        if active == 'active':
            return dx < MIN_DISTANCE_TO_ACTIVATED and dy < MIN_DISTANCE_TO_ACTIVATED
        else:
            return dx < MIN_DISTANCE_TO_MOVE and dy < MIN_DISTANCE_TO_MOVE


    def _add_connection(self, origin: str, destiny: str, X: list[float], Y: list[float]) -> str:

        draw = drawobject(type_object='connections')
        draw.add_part(self.ax.plot(X, Y, alpha=1, color='k')[0])

        name = f'{origin}_{destiny}'

        self.connection[name] = connection(origin, destiny, draw)

        return name


    def _dell_connection(self, name):
        self.connection[name].draw.remove_draw()
        self.connection.pop(name)