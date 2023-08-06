# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Badge(Component):
    """A Badge component.
Render react node inside portal at fixed position. For more information, see: https://mantine.dev/core/Badge/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Badge label.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Key of theme.colors.

- fullWidth (boolean; optional):
    Sets badge width to 100% of parent element, hides overflow text
    with text-overflow: ellipsis.

- gradient (dict; optional):
    Controls gradient, applied to gradient variant only.

    `gradient` is a dict with keys:

    - deg (number; optional)

    - from (string; required)

    - to (string; required)

- leftSection (a list of or a singular dash component, string or number; optional):
    Section rendered on the left side of label.

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

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- radius (number; optional):
    Key of theme.radius or number to set border-radius in px.

- rightSection (a list of or a singular dash component, string or number; optional):
    Section rendered on the right side of label.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Badge height and font size.

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

- variant (a value equal to: 'filled', 'outline', 'light', 'gradient', 'dot'; optional):
    Controls appearance."""
    _children_props = ['leftSection', 'rightSection']
    _base_nodes = ['leftSection', 'rightSection', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Badge'
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, variant=Component.UNDEFINED, gradient=Component.UNDEFINED, size=Component.UNDEFINED, radius=Component.UNDEFINED, fullWidth=Component.UNDEFINED, leftSection=Component.UNDEFINED, rightSection=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'color', 'fullWidth', 'gradient', 'leftSection', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'rightSection', 'size', 'style', 'styles', 'sx', 'unstyled', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'color', 'fullWidth', 'gradient', 'leftSection', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'rightSection', 'size', 'style', 'styles', 'sx', 'unstyled', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Badge, self).__init__(children=children, **args)
