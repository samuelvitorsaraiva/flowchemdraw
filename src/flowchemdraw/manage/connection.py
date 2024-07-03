from flowchemdraw.utils.drawclass import drawobject

class connection_class:

    def __init__(self, parent, origin: dict, destiny: dict, draw: drawobject):

        self.parent = parent

        self.origin = origin

        self.destiny = destiny

        self.draw = draw

        self.operation_ = False

        '''
        :param DI: Internal diameter m (SI)
        :param length: length of the connection m (SI)
        '''
        self.additional_configuration = {'DI': {'value': None, 'class': float},
                                         'length': {'value': None, 'class': float}}


    def operation_set(self, **kwargs) -> None:
        '''
        :param direction: 1 or -1 (infuse and withdraw)
        :param rate: valocity of the changes
        :return: None
        '''
        self.operation_direction = kwargs['direction']

        self.operation_rate = kwargs['rate']

        self.operation_ = True

        if kwargs['orientation'] == 'backward':

            kwargs['connection_id'] = self.origin['connetion_id']

            self.parent.components[self.origin['component']].operation_set(**kwargs)

        else:

            kwargs['connection_id'] = self.destiny['connetion_id']

            self.parent.components[self.destiny['component']].operation_set(**kwargs)




    def operation_draw(self) -> None:

        if self.operation_:

            self.draw.operation_set(rate=self.operation_rate, orientation=self.operation_direction, operation=True)


    def operation_stop(self) -> None:

        self.draw.operation_set(rate=self.operation_rate, orientation=self.operation_direction, operation=False)


