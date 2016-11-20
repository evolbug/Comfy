''' evolbug 2016

LWCF - Light-weight Component Framework 1.0

Can be used for Component Oriented Programming
'''


class Component:
    ''' Base component class
    
    Usage:
        class NewComponent(Component):
            def __setup__(self, *args, **kwargs):
                pass

    Example:
        class Mouse(Component):
            def __setup__(self):
                pass
    
    All components must inherit the Component base class to use the 
    component framework.

    __setup__ is used in place of __init__
    '''

    def __init__(self, *ag, **kw):
        ''' create component - DO NOT OVERRIDE THIS '''

        self.components = []
        self.__setup__(*ag, **kw)

    def __setup__(self, *ag, **kw):
        ''' setup component '''

    def attach(self, *components):
        ''' attach components to self '''

        for c in components: self.components.append(c)

    def __lshift__(self, component):
        ''' self << Component()

        Overloaded operator to attach a single component to self
        '''

        self.components.append(component)

    def event(self, **kw):
        ''' send all events down to children '''
        for k in kw:
            if type(kw[k]) not in (tuple, list):
                kw[k] = [kw[k]]

        for c in self.components:
            c.event(**kw)


class Receiver(Component):
    ''' Basic event receiver component

    Usage:
        Component << Receiver('event_name', function_callback)

    Example:
        class Mouse(Component):
            def __init__(self):
                self.attach(Receiver('mouse_press', self.on_mouse_press))

            def on_mouse_press(self, *args):
                print('press', *args)

    The Receiver will grab an event dispatched by Emitter and call the 
    function with event data.
    '''

    def __setup__(self, event, callback):
        ''' setup, storing event name and function '''

        self.ev = event
        self.fn = callback

    def event(self, **kw):
        ''' find the stored event name in the messages'''
        
        if self.ev in kw:
            # event is found, call stored function with message data
            self.fn(*kw[self.ev])




if __name__ == '__main__':
    ''' Minimal test example '''
    
    class Movement(Component):
        def __setup__(self):
            self.pos = [0,0]
            self << Receiver('move', self.move)

        def move(self, x, y=0):
            self.pos[0] += x
            self.pos[1] += y
            print('Movement: moved by', x, ';', y, 'to', self.pos)

    class Player(Component):
        def move(self, x, y):
            print('Player: I AM MOVING!')
            self.event(move=(x, y))

    player = Player()
    player << Movement()

    player.move(-1,-1)
