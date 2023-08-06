# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tooltip(Component):
    """A Tooltip component.
Renders tooltip at given element on mouse over or any other event. For more information, see: https://mantine.dev/core/tooltip/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Target element.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- arrowOffset (number; optional):
    Arrow offset in px.

- arrowSize (number; optional):
    Arrow size in px.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- closeDelay (number; optional):
    Close delay in ms.

- color (boolean | number | string | dict | list; optional):
    Key of theme.colors.

- disabled (boolean; optional):
    Disables tooltip.

- events (dict; optional):
    Determines which events will be used to show tooltip.

    `events` is a dict with keys:

    - focus (boolean; required)

    - hover (boolean; required)

    - touch (boolean; required)

- label (a list of or a singular dash component, string or number; required):
    Tooltip label.

- m (number; optional):
    margin props.

- mb (number; optional):
    margin props.

- ml (number; optional):
    margin props.

- mr (number; optional):
    margin props.

- mt (number; optional):
    margin props.

- multiline (boolean; optional):
    Defines whether content should be wrapped on to the next line.

- mx (number; optional):
    margin props.

- my (number; optional):
    margin props.

- offset (number; optional):
    Space between target element and tooltip in px.

- openDelay (number; optional):
    Open delay in ms.

- opened (boolean; optional):
    Controls opened state.

- p (number; optional):
    padding props.

- pb (number; optional):
    padding props.

- pl (number; optional):
    padding props.

- position (a value equal to: 'top', 'right', 'bottom', 'left', 'top-end', 'top-start', 'right-end', 'right-start', 'bottom-end', 'bottom-start', 'left-end', 'left-start'; optional):
    Tooltip position relative to target element (default) or mouse
    (floating).

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- radius (number; optional):
    Radius from theme.radius or number to set border-radius in px.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- transition (a value equal to: 'fade', 'skew-up', 'skew-down', 'rotate-right', 'rotate-left', 'slide-down', 'slide-up', 'slide-right', 'slide-left', 'scale-y', 'scale-x', 'scale', 'pop', 'pop-top-left', 'pop-top-right', 'pop-bottom-left', 'pop-bottom-right'; optional):
    One of premade transitions ot transition object.

- transitionDuration (number; optional):
    Transition duration in ms.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- width (number; optional):
    Tooltip width in px.

- withArrow (boolean; optional):
    Determines whether component should have an arrow.

- zIndex (number; optional):
    Tooltip z-index."""
    _children_props = ['label']
    _base_nodes = ['label', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Tooltip'
    @_explicitize_args
    def __init__(self, children=None, openDelay=Component.UNDEFINED, closeDelay=Component.UNDEFINED, opened=Component.UNDEFINED, offset=Component.UNDEFINED, withArrow=Component.UNDEFINED, arrowSize=Component.UNDEFINED, arrowOffset=Component.UNDEFINED, transition=Component.UNDEFINED, transitionDuration=Component.UNDEFINED, events=Component.UNDEFINED, position=Component.UNDEFINED, label=Component.REQUIRED, radius=Component.UNDEFINED, color=Component.UNDEFINED, multiline=Component.UNDEFINED, width=Component.UNDEFINED, zIndex=Component.UNDEFINED, disabled=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'arrowOffset', 'arrowSize', 'className', 'closeDelay', 'color', 'disabled', 'events', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'multiline', 'mx', 'my', 'offset', 'openDelay', 'opened', 'p', 'pb', 'pl', 'position', 'pr', 'pt', 'px', 'py', 'radius', 'style', 'styles', 'sx', 'transition', 'transitionDuration', 'unstyled', 'width', 'withArrow', 'zIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'arrowOffset', 'arrowSize', 'className', 'closeDelay', 'color', 'disabled', 'events', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'multiline', 'mx', 'my', 'offset', 'openDelay', 'opened', 'p', 'pb', 'pl', 'position', 'pr', 'pt', 'px', 'py', 'radius', 'style', 'styles', 'sx', 'transition', 'transitionDuration', 'unstyled', 'width', 'withArrow', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Tooltip, self).__init__(children=children, **args)
