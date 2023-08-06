# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AppShell(Component):
    """An AppShell component.
Responsive shell for your application with header and navbar. For more information, see: https://mantine.dev/core/app-shell/

Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    AppShell content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aside (a list of or a singular dash component, string or number; optional):
    <Aside /> component.

- asideOffsetBreakpoint (number; optional):
    Breakpoint at which Aside component should no longer be offset
    with padding-right, applicable only for fixed position.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- fixed (boolean; optional):
    True to switch from static layout to fixed.

- footer (a list of or a singular dash component, string or number; optional):
    <Footer /> component.

- header (a list of or a singular dash component, string or number; optional):
    <Header /> component.

- hidden (boolean; optional):
    True to hide all AppShell parts and render only children.

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

- navbar (a list of or a singular dash component, string or number; optional):
    <Navbar /> component.

- navbarOffsetBreakpoint (number; optional):
    Breakpoint at which Navbar component should no longer be offset
    with padding-left, applicable only for fixed position.

- p (number; optional):
    padding props.

- padding (number; optional):
    Content padding.

- pb (number; optional):
    padding props.

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

- zIndex (number; optional):
    zIndex prop passed to Navbar and Header components."""
    _children_props = ['navbar', 'aside', 'header', 'footer']
    _base_nodes = ['navbar', 'aside', 'header', 'footer', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'AppShell'
    @_explicitize_args
    def __init__(self, children=None, navbar=Component.UNDEFINED, aside=Component.UNDEFINED, header=Component.UNDEFINED, footer=Component.UNDEFINED, zIndex=Component.UNDEFINED, fixed=Component.UNDEFINED, hidden=Component.UNDEFINED, padding=Component.UNDEFINED, navbarOffsetBreakpoint=Component.UNDEFINED, asideOffsetBreakpoint=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aside', 'asideOffsetBreakpoint', 'className', 'fixed', 'footer', 'header', 'hidden', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'navbar', 'navbarOffsetBreakpoint', 'p', 'padding', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'style', 'styles', 'sx', 'unstyled', 'zIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'aside', 'asideOffsetBreakpoint', 'className', 'fixed', 'footer', 'header', 'hidden', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'navbar', 'navbarOffsetBreakpoint', 'p', 'padding', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'style', 'styles', 'sx', 'unstyled', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(AppShell, self).__init__(children=children, **args)
