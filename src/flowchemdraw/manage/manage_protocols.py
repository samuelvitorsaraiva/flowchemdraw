from flowchemdraw.manage import manage
from flowchemdraw.utils.constantes import SIMULATION_VELOCITY
from flowchemdraw.manage import manage

from PyQt5.QtWidgets import QMessageBox

class manage_protocols:

    def __init__(self, manage_class: manage):

        self.manage = manage_class

        self.commands = {'Initializations': dict()}

        self.current_stage = 'Initializations'

        self.id_ = 1

    def _add_commands(self, command: dict):

        self.commands[self.current_stage][self.id_] = command

        self.id_ += 1

    def _remove_commands(self, command: dict, stage=None):

        if stage == None:
            stage = self.current_stage

        k = 0
        for order in self.commands[stage]:
            if order == command:
                self.commands[stage].pop(k)
            k += 1

        self.id_ -= 1

    def _add_new_stage(self, name):

        self.commands[name] = []


    def _remove_stage(self, name):

        self.commands.pop(name)


    def actived_protocol(self, stage, name):

        command = self.commands[stage][int(name.split()[0])]

        if command['component'].figure_class == 'pump':
            if command['command'] == 'infuse':
                direction = 1
            else:
                direction = -1

            self.manage.components[command['Device']].operation_set(direction=direction,
                                                                    connection_id=2,
                                                                    rate=command['rate'],
                                                                    orientation='backward')

            self.manage.components[command['Device']].operation_set(direction=direction,
                                                                    connection_id=1,
                                                                    rate=command['rate'],
                                                                    orientation='forward')

    def simulation_protocols_settup(self, mng: manage) -> bool:

        # Find devices and connections actived in this protocol
        time_pattern = SIMULATION_VELOCITY * 10

        k = 1; self.time_stage = dict()
        for var in self.commands.keys():
            self.time_stage[var] = time_pattern * k
            k += 1

        self.running_simulation = {var: False for var in self.commands.keys()}
        for stage, commands in self.commands.items():
            for key, command in commands.items():
                if command['component'].figure_class == 'pump':
                    try:
                        time = command['volume'] / (command['rate'] * SIMULATION_VELOCITY)
                        if time > time_pattern:
                            self.time_stage[stage] = time
                        else:
                            self.time_stage[stage] = time_pattern
                    except:
                        msg = QMessageBox()
                        msg.setWindowTitle("Warning")
                        msg.setText(f"The parameters rate and volume need to be defined")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                        return False


    def simulation_protocols(self, time, components):

        # Estimated time of each stage (simulated)


        # Verify what stage is running actually




        if not self.running_simulation.values():
            for stage in self.commands.keys():
                if time <= self.time_stage[stage]:
                    for key, command in self.commands[stage].values():
                        if command['component'].figure_draw == 'pump':
                            if command['command'] == 'infuse':
                                direction = 1
                            else:
                                direction = -1
                            components[command['Device']].operation_set(self,
                                                                        direction=direction,
                                                                        connection_id=1,
                                                                        rate=command['rate'])
                    break

