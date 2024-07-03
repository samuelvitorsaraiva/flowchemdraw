from flowchemdraw.utils.drawclass import components

class component:

    def __init__(self, parent, name: str, position: (float, float), draw: components):

        self.parent = parent

        self.name = name

        self.position = position

        self.draw = draw

        self.type = draw.type_object

        self.operation_ = False

        self.figure_class = str(draw.__class__).split('.')[-2]

    def _add_connection_point(self, pos):

        for key, connection in self.draw.connection_points.items():
            if connection['position'] == pos and connection['name'] == None:
                return [True, key]

        return [False, 0]

    def operation_set(self, **kwargs):
        '''

        :param direction: 1 or -1 (infuse and withdraw)
        :return:
        '''

        self.operation_direction = kwargs['direction']

        self.operation_rate = kwargs['rate']

        connection = self.draw.connection_points[kwargs['connection_id']]

        self.operation_ = True

        n = len(connection['pairs'])
        if n > 1:
            for pair in connection['pairs']:
                name = connection[pair]['name']
                kwargs['rate'] *= 1/n
                self.parent.connections[name].operation_set(**kwargs)
        elif connection['pairs'][0] != kwargs['connection_id']:
            name = self.draw.connection_points[connection['pairs'][0]]['name']
            self.parent.connection[name].operation_set(**kwargs)


    def operation_draw(self):

        if self.operation_:

            self.draw.operation_set(direction=self.operation_direction)


