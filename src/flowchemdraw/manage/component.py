class component:

    def __init__(self, name: str, position: (float, float), draw: drawobject):

        self.name = name

        self.position = position

        self.draw = draw

        self.type = draw.type_object

        self.connections = [None] * len(draw.connection_points)

    def _add_connection_point(self, name, pos):

        i = 0
        for connection in self.draw.connection_points:
            if connection == pos and self.connections[i] == None:
                return [True, i]
            i += 1

        return [False, 0]

