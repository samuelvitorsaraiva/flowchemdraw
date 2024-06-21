from flowchemdraw.utils.drawclass import drawobject
from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.utils.constantes import *
from flowchemdraw.components import CustomMessageBox

from flowchemdraw.manage import device_component, utensils, connection

from PyQt5.QtWidgets import QMessageBox, QDialog
from matplotlib.figure import Figure
from loguru import logger


class manage:

    def __init__(self, ax: Figure):

        self.components = dict()

        self.utensils = dict()

        self.connection = dict()

        self.ax = ax


    def _add_utensils(self, name: str) -> str:
        ...

    def _add_component(self, name: str, type: str = 'device') -> str:

        class_name = name

        for dev in self.components.keys():
            if self._isnearby(dev):
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText("There is a device placed in the designated area to new ones. "
                            "Please move away its device of this area before add new one.")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                return '-'

        if type == 'others':

            figure_draw = class_name

        else:

            figure_draw = DRAW_DEVICES_CORRESPONDENT[class_name]

            dialog = CustomMessageBox(name=name, class_name=name.split('/')[0])
            if dialog.exec_() == QDialog.Accepted:
                [name, config_dict] = dialog.get_input()
            else:
                return '-'


        if name in self.components.keys():
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("There is a component with this name. "
                        "Please change the name to add new component.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return '-'

        dev = import_class('flowchemdraw.figures', figure_draw)

        self.components[name] = component(name=name,
                                          class_name=class_name,
                                          position=LOCATION_NEW_DEVICES,
                                          draw=dev(self.ax, pos=LOCATION_NEW_DEVICES,
                                                   name=name))

        self.components[name].update_configuration_file(config_dict)

        return name


    def _dell_component(self, name: str) -> list[str]:

        connection_dell = []
        for key in self.connection.keys():
            if self.connection[key].origin == name or self.connection[key].destiny == name:
                connection_dell.append(key)

        [self._dell_connection(key) for key in connection_dell]

        self.components[name].draw.active_draw(False)
        self.components[name].draw.remove_draw()
        self.components.pop(name)

        return connection_dell


    def _move_component(self, name: str, new_pos: (float, float)) -> list[str]:

        self.components[name].position = new_pos
        self.components[name].draw.set_position(new_pos=new_pos)

        connection_dell = []
        for key in self.connection.keys():
            if self.connection[key].origin == name or self.connection[key].destiny == name:
                connection_dell.append(key)

        [self._dell_connection(key) for key in connection_dell]

        return connection_dell


    def _rotate_component(self, angle: float) -> None:
        ...


    def _rename_component(self, new_name: str) -> None:
        ...


    def _isnearby(self, name, pos: (float, float) = LOCATION_NEW_DEVICES, active: str = 'active') -> bool:

        x, y = self.components[name].position
        dx = abs(x - pos[0])
        dy = abs(y - pos[1])

        if active == 'active':
            return dx < MIN_DISTANCE_TO_ACTIVATED and dy < MIN_DISTANCE_TO_ACTIVATED
        else:
            return dx < MIN_DISTANCE_TO_MOVE and dy < MIN_DISTANCE_TO_MOVE


    def _add_connection(self, origin: str, destiny: str, X: list[float], Y: list[float]) -> str | bool:

        name = f'{origin}_{destiny}'

        condition_1, ind1 = self.components[destiny]._add_connection_point(name, (X[-1], Y[-1]))
        condition_2, ind2 = self.components[origin]._add_connection_point(name, (X[0], Y[0]))

        if  condition_1 and condition_2 :

            self.components[destiny].connections[ind1] = name
            self.components[origin].connections[ind2] = name

            draw = drawobject(type_object='connections')
            draw.add_part(self.ax.plot(X, Y, alpha=1, color='k')[0])

            self.connection[name] = connection(origin, destiny, draw)

            return name

        if condition_1:
            x = origin
        else:
            x = destiny

        logger.info(f'The connection between {origin} and {destiny} can not be created because there is another '
                    f'line connected in the {x} at the same point.')

        return False


    def _dell_connection(self, name):

        for dev in [self.connection[name].destiny, self.connection[name].origin]:
            lista = self.components[dev].connections
            lista = [None if element == name else element for element in lista]
            self.components[dev].connections = lista

        self.connection[name].draw.remove_draw()
        self.connection.pop(name)


    def _add_devices_auto(self, class_name: str, name: str, configuration_file: dict | None = None):

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

        if  class_name in DRAW_DEVICES_CORRESPONDENT.keys():

            figure_draw = DRAW_DEVICES_CORRESPONDENT[class_name]

        dev = import_class('flowchemdraw.figures', figure_draw)

        self.components[name] = component(name=name,
                                          class_name=class_name,
                                          position=loc,
                                          draw=dev(self.ax, pos=loc, name=name))

        if configuration_file != None:

            self.components[name].update_configuration_file(configuration_file)
