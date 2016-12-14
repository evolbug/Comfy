''' evolbug 2016

Comfy - Light-weight Component Framework

Can be used for component oriented programming
'''


class Component:
    ''' Base component class

    All components must inherit the Component base class to use the
    component framework.

    __setup__ is used in place of __init__

    Usage:
        class NewComponent(Component):
            def __setup__(self, *args, **kwargs):
                pass
    '''

    def __init__(self, *ag, **kw):
        ''' create component, super() this if used '''

        self._components = [] # child components
        self._parents = [] # own parents
        self.__setup__(*ag, **kw)

    def __setup__(self, *ag, **kw):
        ''' setup component '''

    def attach(self, *components):
        ''' attach components to self '''

        for c in components:
            self._components.append(c)
            c._parents.append(self) # bind both ways

        return components

    def __lshift__(self, components):
        ''' self << Component()

        Overloaded operator to attach a single component to self
        '''

        return self.attach(
            *components if type(components) in (tuple, list) else [components])

    def __call__(self, **kw): self.event(**kw) #implicit event
    def event(self, **kw): #explicit event
        ''' send all events down to children '''

        for k in kw:
            if type(kw[k]) not in (tuple, list):
                kw[k] = [kw[k]]

        for c in self._components: c.event(**kw)



class Receiver(Component):
    ''' Basic event receiver component

    The Receiver will grab an event dispatched by the parent Component
    and call the function with event data.

    Usage:
        Component << Receiver('event_name', function_callback)
    '''


    def __init__(self, event, callback, *ag, **kw):
        ''' store event name and function '''

        self._ev = event
        self._fn = callback
        super().__init__(*ag, **kw)

    def event(self, **kw):
        ''' find the stored event name in the messages'''

        if self._ev == '*': # capture all events
            for event in kw: # for each event
                self._fn(*kw[event]) # call the function

        if self._ev in kw: # capture specific event
            self._fn(*kw[self._ev]) # send event data to function



class LoggedReceiver(Receiver):
    ''' Receiver that logs event captures '''

    def event(self, **kw):
        ''' find the stored event name in the messages'''

        if self._ev == '*': # capture all events
            for event in kw: # for each event
                self._fn(*kw[event]) # call the function

        if self._ev in kw: # capture specific event
            self._log(', '.join(str(i) for i in kw[self._ev])) # log capture
            self._fn(*kw[self._ev]) # send event data to function

    def _log(self, argstr):
        ''' log the captured event, override for custom output '''

        print(
            'LOG:', ', '.join(str(c.__class__.__name__) for c in self._parents),
            'caught event:', self._ev, '>', argstr
        )



class LoggedComponent(Component):
    ''' Component that logs all messages that pass through '''

    def __init__(self, *ag, **kw):
        super().__init__(*ag, **kw)
        self << Receiver('*', self._log)

    def _log(self, *ag):
        ''' log passing events, override for custom output '''

        print('LOG:', self.__class__.__name__, 'received:',
            ', '.join(str(i) for i in ag))



if __name__ == '__main__':
    ''' Minimal test example '''

    class Movement(Component):
        def __setup__(self):
            self.pos = [0,0]
            self << LoggedReceiver('move', self.move)

        def move(self, x, y=0):
            self.pos[0] += x
            self.pos[1] += y
            print('Movement: moved by', x, ';', y, 'to', self.pos)

    class Player(LoggedComponent): pass

    player = Player()
    player << Movement()

    player(move=(-1,-1))
