from flowchemdraw.utils.drawclass import drawobject
from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.utils.constantes import *
from flowchemdraw.components import CustomMessageBox

from PyQt5.QtWidgets import QMessageBox, QDialog
from matplotlib.figure import Figure
from abc import ABC

class component:

    def __init__(self, name: str, position: (float, float), draw: drawobject):

        self.class_name = name

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

        figure_draw = 'undefined'

        if name.split('_')[0] in COMPONENTS_NONELETRONIC:

            figure_draw = name.split('_')[0]

        elif name.split('_')[0] in DRAW_DEVICES_CORRESPONDENT.keys():

            figure_draw = DRAW_DEVICES_CORRESPONDENT[name.split('_')[0]]


        dialog = CustomMessageBox(name=name)
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.get_input()

            dev = import_class('flowchemdraw.figures', figure_draw)

            self.components[name] = component(name=name,
                                              position=LOCATION_NEW_DEVICES,
                                              draw=dev(self.ax, pos=LOCATION_NEW_DEVICES, name=name))
            return name

        else:

            return '-'


    def _dell_component(self, name: str) -> list[str]:
        self.components[name].draw.active_draw(False)
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


    def _add_devices_auto(self, class_name, name):

        loc = (0, 0)
        for i in range(1, SPACE_GRID_FIG, PATTERN_DIMENSION*4):
            for j in range(1, SPACE_GRID_FIG, PATTERN_DIMENSION*4):
                aprove = True
                for key in self.components.keys():
                    aprove = aprove and not self._isnearby(key, (i, j))
                if aprove:
                    loc = (i, j)
                    break
            else:
                continue
            break

        figure_draw = 'undefined'

        if  class_name.split('_')[0] in DRAW_DEVICES_CORRESPONDENT.keys():

            figure_draw = DRAW_DEVICES_CORRESPONDENT[class_name.split('_')[0]]

        dev = import_class('flowchemdraw.figures', figure_draw)

        self.components[name] = component(name=name,
                                          position=loc,
                                          draw=dev(self.ax, pos=loc, name=name))

        self.components[name].class_name = class_name