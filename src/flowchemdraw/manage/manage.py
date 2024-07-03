from flowchemdraw.utils.drawclass import connections
from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.utils.constantes import *
from flowchemdraw.components import CustomMessageBox

from flowchemdraw.manage.connection import connection_class
from flowchemdraw.manage.device_component import device_component_class
from flowchemdraw.manage.utensils import utensils_class

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

            dialog = CustomMessageBox(name=name, class_name=name.split('/')[0], type=type)
            if dialog.exec_() == QDialog.Accepted:
                name = dialog.get_input_utensils()
            else:
                return '-'

        else:

            figure_draw = DRAW_DEVICES_CORRESPONDENT[class_name]

            dialog = CustomMessageBox(name=name, class_name=name.split('/')[0])
            if dialog.exec_() == QDialog.Accepted:
                [name, config_dict] = dialog.get_input_device()
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

        if type == 'others':

            self.components[name] = utensils_class(self,
                                                   name=name,
                                                   class_name=class_name,
                                                   position=LOCATION_NEW_DEVICES,
                                                   draw=dev(self.ax, pos=LOCATION_NEW_DEVICES,
                                                            name=name))
        else:

            self.components[name] = device_component_class(self,
                                                           name=name,
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


    def _nearbydevice(self, pos: (float, float) = LOCATION_NEW_DEVICES) -> str:

        for name in self.components.keys():

            if self._isnearby(name=name, pos=pos):

                return name

        return '-'


    def _add_connection(self, origin: str, destiny: str, X: list[float], Y: list[float]) -> str | bool:

        name = f'{origin}_{destiny}'

        condition_1, ind1 = self.components[destiny]._add_connection_point((X[-1], Y[-1]))
        condition_2, ind2 = self.components[origin]._add_connection_point((X[0], Y[0]))

        if condition_1 and condition_2:

            self.components[destiny].draw.connection_points[ind1]['name'] = name
            self.components[origin].draw.connection_points[ind2]['name'] = name

            draw = connections(self.ax, type_object='connections')
            draw.add_part(self.ax.plot(X, Y, alpha=1, color='k')[0])

            self.connection[name] = connection_class(self,
                                                     origin={'component': origin, 'connetion_id': ind2},
                                                     destiny={'component': destiny, 'connetion_id': ind1},
                                                     draw=draw)

            return name

        if condition_1:
            x = origin
        else:
            x = destiny

        logger.info(f'The connection between {origin} and {destiny} can not be created because there is another '
                    f'line connected in the {x} at the same point.')

        return False


    def _dell_connection(self, name):

        for dev in [self.connection[name].destiny['component'], self.connection[name].origin['component']]:
            for id_ in self.components[dev].draw.connection_points.keys():
                if self.components[dev].draw.connection_points[id_]['name'] == name:
                    self.components[dev].draw.connection_points[id_]['name'] = None

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

        if class_name in DRAW_DEVICES_CORRESPONDENT.keys():

            figure_draw = DRAW_DEVICES_CORRESPONDENT[class_name]

        dev = import_class('flowchemdraw.figures', figure_draw)

        self.components[name] = device_component_class(self,
                                                       name=name,
                                                       class_name=class_name,
                                                       position=loc,
                                                       draw=dev(self.ax, pos=loc, name=name))

        if configuration_file != None:

            self.components[name].update_configuration_file(configuration_file)


    def _update(self, manage_file):

        for item in manage_file.components.values():

            figure_draw = item.class_name

            if item.class_name in DRAW_DEVICES_CORRESPONDENT.keys():
                figure_draw = DRAW_DEVICES_CORRESPONDENT[item.class_name]

            dev = import_class('flowchemdraw.figures', figure_draw)

            if item.draw.type_object == 'devices':

                self.components[item.name] = device_component_class(self,
                                                                    name=item.name,
                                                                    class_name=item.class_name,
                                                                    position=item.position,
                                                                    draw=dev(self.ax,
                                                                             pos=item.position,
                                                                             name=item.name))

                self.components[item.name].configuration_block = item.configuration_block

            else:

                self.components[item.name] = utensils_class(self,
                                                            name=item.name,
                                                            class_name=item.class_name,
                                                            position=item.position,
                                                            draw=dev(self.ax,
                                                                     pos=item.position,
                                                                     name=item.name))

        for item in manage_file.connection.values():

            X = item.draw.parts[0].get_xdata()

            Y = item.draw.parts[0].get_ydata()

            name = self._add_connection(origin=item.origin['component'], destiny=item.destiny['component'], X=X, Y=Y)
