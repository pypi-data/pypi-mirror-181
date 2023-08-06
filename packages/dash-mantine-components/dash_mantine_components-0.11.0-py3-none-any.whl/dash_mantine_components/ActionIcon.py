# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ActionIcon(Component):
    """An ActionIcon component.
Icon button. For more information, see: https://mantine.dev/core/action-icon/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Icon.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Key of theme.colors.

- disabled (boolean; optional):
    Indicates disabled state.

- gradient (dict; optional):
    Controls gradient settings in gradient variant only.

    `gradient` is a dict with keys:

    - deg (number; optional)

    - from (string; required)

    - to (string; required)

- loaderProps (dict; optional):
    Props spread to Loader component.

    `loaderProps` is a dict with keys:

    - color (boolean | number | string | dict | list; optional):
        Loader color from theme.

    - size (number; optional):
        Defines width of loader.

    - variant (a value equal to: 'bars', 'oval', 'dots'; optional):
        Loader appearance.

- loading (boolean; optional):
    Indicates loading state.

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

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- p (number; optional):
    padding props.

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

- radius (number; optional):
    Button border-radius from theme or number to set border-radius in
    px.

- size (number; optional):
    Predefined icon size or number to set width and height in px.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- title (string; optional):
    Set title prop to make ActionIcon visible to screen readers.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (a value equal to: 'subtle', 'filled', 'outline', 'light', 'default', 'transparent', 'gradient'; optional):
    Controls appearance."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'ActionIcon'
    @_explicitize_args
    def __init__(self, children=None, variant=Component.UNDEFINED, color=Component.UNDEFINED, gradient=Component.UNDEFINED, radius=Component.UNDEFINED, size=Component.UNDEFINED, loaderProps=Component.UNDEFINED, loading=Component.UNDEFINED, disabled=Component.UNDEFINED, n_clicks=Component.UNDEFINED, title=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'color', 'disabled', 'gradient', 'loaderProps', 'loading', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'n_clicks', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'size', 'style', 'styles', 'sx', 'title', 'unstyled', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'color', 'disabled', 'gradient', 'loaderProps', 'loading', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'n_clicks', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'size', 'style', 'styles', 'sx', 'title', 'unstyled', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(ActionIcon, self).__init__(children=children, **args)
