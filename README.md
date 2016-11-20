# py-LWCF
Light-weight Component Framework for Python 3

    Base component class
    
    Usage:
        class NewComponent(Component):
            def __setup__(self, *args, **kwargs):
                pass
    
    All components must inherit the Component base class
    to use the component framework.
    
    __setup__ is used in place of __init__
    
    Attaching components to eachother:
        component.attach(other, ...)
        component << other
        
    Sending messages(events):
        component.event(event_name=data, ...)
-

    Basic event receiver component
    
    Usage:
        component.attach(Receiver('event_name', function_callback)
        component << Receiver('event_name', function_callback)

    The Receiver will grab an event dispatched by the parent
    Component and call the function with event data.
