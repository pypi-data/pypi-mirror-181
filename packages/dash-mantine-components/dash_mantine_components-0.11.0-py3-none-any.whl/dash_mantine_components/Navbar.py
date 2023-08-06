# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Navbar(Component):
    """A Navbar component.
Navbar. For more information, see: https://mantine.dev/core/app-shell/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Section Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- fixed (boolean; optional):
    Set position to fixed.

- height (string | number; optional):
    Component height.

- hidden (boolean; optional):
    Set to True to hide component at hiddenBreakpoint.

- hiddenBreakpoint (number; optional):
    Breakpoint at which component will be hidden if hidden prop is
    True.

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

- p (number; optional):
    padding props.

- pb (number; optional):
    padding props.

- pl (number; optional):
    padding props.

- position (dict; optional):
    Position for fixed variant.

    `position` is a dict with keys:

    - bottom (number; optional)

    - left (number; optional)

    - right (number; optional)

    - top (number; optional)

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- width (dict; optional):
    Component width with breakpoints.

    `width` is a dict with keys:


- withBorder (boolean; optional):
    Border.

- zIndex (number; optional):
    z-index."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'Navbar'
    @_explicitize_args
    def __init__(self, children=None, width=Component.UNDEFINED, height=Component.UNDEFINED, withBorder=Component.UNDEFINED, fixed=Component.UNDEFINED, position=Component.UNDEFINED, hiddenBreakpoint=Component.UNDEFINED, hidden=Component.UNDEFINED, zIndex=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'fixed', 'height', 'hidden', 'hiddenBreakpoint', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'position', 'pr', 'pt', 'px', 'py', 'style', 'styles', 'sx', 'unstyled', 'width', 'withBorder', 'zIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'fixed', 'height', 'hidden', 'hiddenBreakpoint', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'position', 'pr', 'pt', 'px', 'py', 'style', 'styles', 'sx', 'unstyled', 'width', 'withBorder', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Navbar, self).__init__(children=children, **args)
