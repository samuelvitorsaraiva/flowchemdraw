from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT

from matplotlib.figure import Figure

from flowchemdraw.utils.drawclass import drawobject

import numpy as np

#plt.style.use('dark_background')

MIN_DISTANCE_TO_ACTIVATED = 1

MIN_DISTANCE_TO_MOVE = 1

SPACE_GRID_FIG = 20

LOCATION_NEW_DEVICES = (SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED, SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED)

class mplwidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        self.Main_Window = None

        self.axes.set_xlim(0, SPACE_GRID_FIG)
        self.axes.set_ylim(0, SPACE_GRID_FIG)

        self.axes.set_axis_off()

        #self.axes.grid(True)

        # Connect the mouse events to handlers
        self.mpl_connect('button_press_event', self.on_mouse_press)
        self.mpl_connect('button_release_event', self.on_mouse_release)
        self.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.mpl_connect('scroll_event', self.on_mouse_scroll)

        self.move_componets = {'actived': False}

        self.draw_connections = {'actived': False, 'line_connection': None, 'line_data': [[], []],
                                 'vertical': False, 'inflexion': True}

        self.component = None

        self.grid_draw()

    def grid_draw(self):
        for n in range(2*SPACE_GRID_FIG):
            self.axes.plot([n/2]*SPACE_GRID_FIG*2, np.linspace(0, SPACE_GRID_FIG, 2*SPACE_GRID_FIG), "o", markersize=1, color='k', alpha=0.2)
        self.draw()

    def on_mouse_press(self, event):
        if event.inaxes:

            if self.draw_connections['actived'] and event.button == 1:

                for dev in self.Main_Window.components.keys():

                    if dev != self.component:

                        dx = abs(self.Main_Window.components[dev]['draw_class'].position[0] - event.xdata)
                        dy = abs(self.Main_Window.components[dev]['draw_class'].position[1] - event.ydata)

                        if dx < MIN_DISTANCE_TO_ACTIVATED and dy < MIN_DISTANCE_TO_ACTIVATED:

                            'get the closest connection point of the receptor component'
                            point = self.Main_Window.components[dev]['draw_class'].get_nearby_connection(pos=(event.xdata, event.ydata))
                            if self.draw_connections['vertical']:
                                'Abscissa need to change (x-coordinate)'
                                self.draw_connections['line_data'][0][-2] = point[0]
                            else:
                                'Ordinate need to change (y-coordinate)'
                                self.draw_connections['line_data'][1][-2] = point[1]

                            self.draw_connections['line_data'][0][-1] = point[0]
                            self.draw_connections['line_data'][1][-1] = point[1]

                            obj = drawobject(type_object='connections')
                            obj.add_part(self.axes.plot(
                                self.draw_connections['line_data'][0],
                                self.draw_connections['line_data'][1], alpha=1, color='k')[0])

                            self.Main_Window.components[f'{self.component}_{dev}'] = {'draw_class': obj}
                            self.Main_Window.add_new_item_Qtree('connections', f'{self.component}_{dev}')

                            break

                self.draw_connections['line_connection'][0].remove()
                self.draw_connections = {'actived': False, 'line_connection': None, 'line_data': [[], []],
                                         'vertical': False, 'inflexion': True}

                self.Main_Window.components[self.component]['draw_class'].square_activation_connect(False)
                self.draw_connections['actived'] = False
                self.component = None
                self.draw()
                return

            elif self.draw_connections['actived'] and event.button == 3:

                self.draw_connections['inflexion'] = True
                self.draw_connections['vertical'] = not self.draw_connections['vertical']
                return

            #self.Main_Window.active_item('', active=False)

            for dev in self.Main_Window.components.keys():

                dx = abs(self.Main_Window.components[dev]['draw_class'].position[0] - event.xdata)
                dy = abs(self.Main_Window.components[dev]['draw_class'].position[1] - event.ydata)

                if dx < MIN_DISTANCE_TO_ACTIVATED and dy < MIN_DISTANCE_TO_ACTIVATED:
                    if event.button == 1 and not self.move_componets['actived']:
                        self.Main_Window.components[dev]['draw_class'].square_activation_draw(True)
                        self.move_componets['actived'] = True
                        self.component = dev

                    elif event.button == 3:
                        self.Main_Window.components[dev]['draw_class'].square_activation_connect(True)
                        self.draw_connections['actived'] = True
                        self.component = dev

                    self.draw()

    def on_mouse_release(self, event):
        if event.inaxes:

            if self.move_componets['actived']:

                dx = abs(self.Main_Window.components[self.component]['draw_class'].position[0] - event.xdata)
                dy = abs(self.Main_Window.components[self.component]['draw_class'].position[1] - event.ydata)

                if dx > MIN_DISTANCE_TO_ACTIVATED or dy > MIN_DISTANCE_TO_ACTIVATED:

                    position = (int(event.xdata) + 0.5, int(event.ydata) + 0.5)

                    for dev in self.Main_Window.components.keys():

                        position_dev = self.Main_Window.components[dev]['draw_class'].position

                        if position_dev[0] == position[0] and position_dev[1] == position[1]:
                            self.Main_Window.components[self.component]['draw_class'].square_activation_draw(False)
                            self.move_componets['actived'] = False
                            self.component = None
                            self.draw()
                            return
                else:
                    self.Main_Window.components[self.component]['draw_class'].square_activation_draw(False)
                    self.move_componets['actived'] = False
                    self.component = None
                    self.draw()
                    return

            if self.move_componets['actived']:
                self.Main_Window.components[self.component]['draw_class'].set_position(new_pos=position)
                self.Main_Window.components[self.component]['draw_class'].square_activation_draw(False)
                self.move_componets['actived'] = False
                self.component = None
                self.draw()
                return

    def on_mouse_move(self, event):
        if event.inaxes:
            if self.draw_connections['actived']:
                if self.draw_connections['line_connection']:
                    self.draw_connections['line_connection'][0].remove()

                if self.draw_connections['inflexion']:
                    if not self.draw_connections['line_data'][0]:
                        '''creating the first point of connection'''
                        first_point = self.Main_Window.components[self.component]['draw_class'].get_nearby_connection(pos=(event.xdata, event.ydata))
                        self.draw_connections['line_data'][0].append(first_point[0])
                        self.draw_connections['line_data'][1].append(first_point[1])

                    else:
                        self.draw_connections['line_data'][0].append(event.xdata)
                        self.draw_connections['line_data'][1].append(event.ydata)

                    if len(self.draw_connections['line_data'][0]) > 2:
                        self.draw_connections['inflexion'] = False
                else:
                    if self.draw_connections['vertical']:
                        self.draw_connections['line_data'][0][-1] = self.draw_connections['line_data'][0][-2]
                        self.draw_connections['line_data'][1][-1] = event.ydata
                    else:
                        self.draw_connections['line_data'][0][-1] = event.xdata
                        self.draw_connections['line_data'][1][-1] = self.draw_connections['line_data'][1][-2]

                n = len(self.draw_connections['line_data'][0])
                if n == 2:
                    self.draw_connections['inflexion'] = False
                    dx = abs(self.draw_connections['line_data'][0][-1] - self.draw_connections['line_data'][0][-2])
                    dy = abs(self.draw_connections['line_data'][1][-1] - self.draw_connections['line_data'][1][-2])
                    if dx > dy:
                        self.draw_connections['vertical'] = False
                    else:
                        self.draw_connections['vertical'] = True

                self.draw_connections['line_connection'] = self.axes.plot(self.draw_connections['line_data'][0], self.draw_connections['line_data'][1], alpha=0.5)
                self.draw()

    def on_mouse_scroll(self, event):
        if event.inaxes:
            #print(f'Mouse scrolled at ({event.xdata}, {event.ydata}) with step {event.step}')
            pass
