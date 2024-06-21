class connection:

    def __init__(self, origin: str, destiny: str, draw: drawobject):

        self.origin = origin

        self.destiny = destiny

        self.draw = draw

        self.DI: float | None = None

        self.length: float | None = None

    def _set_configuration(self, DI: float, lenght: float) -> None:
        '''
        Set the configurations parameter of the connections

        :param DI: Internal diameter m (SI)
        :param lenght: lenght of the connection m (SI)
        :return: None
        '''
        self.DI = DI
        self.length = lenght