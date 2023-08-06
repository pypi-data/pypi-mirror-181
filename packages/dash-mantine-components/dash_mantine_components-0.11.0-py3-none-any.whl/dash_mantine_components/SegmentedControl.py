# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SegmentedControl(Component):
    """A SegmentedControl component.
Horizontal control made of multiple segments, alternative to RadioGroup. For more information, see: https://mantine.dev/core/segmented-control/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Active control color from theme.colors, defaults to white in light
    color scheme and theme.colors.dark[9] in dark.

- data (list of strings; required):
    Data based on which controls are rendered.

- disabled (boolean; optional):
    Disabled input state.

- fullWidth (boolean; optional):
    True if component should have 100% width.

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

- mx (number; optional):
    margin props.

- my (number; optional):
    margin props.

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    Display Vertically.

- p (number; optional):
    padding props.

- pb (number; optional):
    padding props.

- persisted_props (list of strings; default ["value"]):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- pl (number; optional):
    padding props.

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- radius (number; optional):
    Border-radius from theme or number to set border-radius in px.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Controls font-size, paddings and height.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- transitionDuration (number; optional):
    Transition duration in ms, set to 0 to turn off transitions.

- transitionTimingFunction (string; optional):
    Transition timing function for all transitions, defaults to
    theme.transitionTimingFunction.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- value (string; optional):
    Current selected value."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'SegmentedControl'
    @_explicitize_args
    def __init__(self, data=Component.REQUIRED, value=Component.UNDEFINED, disabled=Component.UNDEFINED, fullWidth=Component.UNDEFINED, color=Component.UNDEFINED, size=Component.UNDEFINED, radius=Component.UNDEFINED, transitionDuration=Component.UNDEFINED, transitionTimingFunction=Component.UNDEFINED, orientation=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'color', 'data', 'disabled', 'fullWidth', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'orientation', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'size', 'style', 'styles', 'sx', 'transitionDuration', 'transitionTimingFunction', 'unstyled', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'data', 'disabled', 'fullWidth', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'orientation', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'size', 'style', 'styles', 'sx', 'transitionDuration', 'transitionTimingFunction', 'unstyled', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SegmentedControl, self).__init__(**args)
