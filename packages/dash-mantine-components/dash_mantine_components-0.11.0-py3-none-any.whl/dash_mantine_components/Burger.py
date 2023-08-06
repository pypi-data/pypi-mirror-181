# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Burger(Component):
    """A Burger component.
Display burger-style menu button. For more information, see: https://mantine.dev/core/burger/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (string; optional):
    Burger color value, not connected to theme.colors, defaults to
    theme.black with light color scheme and theme.white with dark.

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

- opened (boolean; default False):
    Burger state: True for cross, False for burger.

- p (number; optional):
    padding props.

- pb (number; optional):
    padding props.

- persisted_props (list of strings; default ["opened"]):
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

- size (number; optional):
    Predefined burger size or number to set width and height in px.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- title (string; optional):
    Set title prop to make Burger visible to screen readers.

- transitionDuration (number; optional):
    Transition duration in ms.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'Burger'
    @_explicitize_args
    def __init__(self, opened=Component.UNDEFINED, color=Component.UNDEFINED, size=Component.UNDEFINED, transitionDuration=Component.UNDEFINED, title=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'color', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'opened', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'pt', 'px', 'py', 'size', 'style', 'styles', 'sx', 'title', 'transitionDuration', 'unstyled']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'opened', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'pt', 'px', 'py', 'size', 'style', 'styles', 'sx', 'title', 'transitionDuration', 'unstyled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Burger, self).__init__(**args)
