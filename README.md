# py-LWCF
# Light-weight Component Framework for Python 3

### Base component class
All components must inherit the Component base class to use the component framework.
`__setup__` is used in place of `__init__` for code cleanliness, although `__init__` is allowed if superclass gets initialised.

```Python
class NewComponent(Component):
    def __setup__(self, *args, **kwargs):
        pass
```

##### Attaching components to eachother:
```Python
component.attach(other, ...)
component << other
self.other = other
```

##### Sending messages(events):
```Python
component(event_name=data, ...)
component.event(event_name=data, ...)

component.other(event_name=data, ...)
component.other.event(event_name=data, ...)
```
-
### Basic event receiver component
The Receiver will grab an event dispatched by the parent Component and call the function with event data.

```Python
component.attach(Receiver('event_name', function_callback)
component << Receiver('event_name', function_callback)
self.receiver = Receiver('event_name', function_callback)
```
-
### Simple test example
```Python
class Movement(Component):
    def __setup__(self): # using __setup__
        self.pos = [0,0]
        self << Receiver('move', self.move) # this receiver will grab the 'move' event

    def move(self, x, y=0): # function that's called on 'move' event
        self.pos[0] += x
        self.pos[1] += y
        print('Movement: moved by', x, ';', y, 'to', self.pos)

class Player(Component): pass # component container class

player = Player()
player << Movement() # giving the player movement

player(move=(-1,-1)) # dispatching an event 'move', the Movement component will catch this
```
