# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Col(Component):
    """A Col component.
Inline or block code without syntax highlight. For more information, see: https://mantine.dev/core/code/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Col content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- lg (number; optional):
    Col span at (min-width: theme.breakpoints.lg).

- m (number; optional):
    margin props.

- mb (number; optional):
    margin props.

- md (number; optional):
    Col span at (min-width: theme.breakpoints.md).

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

- offset (number; optional):
    Column left offset.

- offsetLg (number; optional):
    Column left offset at (min-width: theme.breakpoints.lg).

- offsetMd (number; optional):
    Column left offset at (min-width: theme.breakpoints.md).

- offsetSm (number; optional):
    Column left offset at (min-width: theme.breakpoints.sm).

- offsetXl (number; optional):
    Column left offset at (min-width: theme.breakpoints.xl).

- offsetXs (number; optional):
    Column left offset at (min-width: theme.breakpoints.xs).

- order (number; optional):
    Default col order.

- orderLg (number; optional):
    Col order at (min-width: theme.breakpoints.lg).

- orderMd (number; optional):
    Col order at (min-width: theme.breakpoints.md).

- orderSm (number; optional):
    Col order at (min-width: theme.breakpoints.sm).

- orderXl (number; optional):
    Col order at (min-width: theme.breakpoints.xl).

- orderXs (number; optional):
    Col order at (min-width: theme.breakpoints.xs).

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

- sm (number; optional):
    Col span at (min-width: theme.breakpoints.sm).

- span (number; optional):
    Default col span.

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

- xl (number; optional):
    Col span at (min-width: theme.breakpoints.xl).

- xs (number; optional):
    Col span at (min-width: theme.breakpoints.xs)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'Col'
    @_explicitize_args
    def __init__(self, children=None, span=Component.UNDEFINED, offset=Component.UNDEFINED, order=Component.UNDEFINED, orderXs=Component.UNDEFINED, orderSm=Component.UNDEFINED, orderMd=Component.UNDEFINED, orderLg=Component.UNDEFINED, orderXl=Component.UNDEFINED, offsetXs=Component.UNDEFINED, offsetSm=Component.UNDEFINED, offsetMd=Component.UNDEFINED, offsetLg=Component.UNDEFINED, offsetXl=Component.UNDEFINED, xs=Component.UNDEFINED, sm=Component.UNDEFINED, md=Component.UNDEFINED, lg=Component.UNDEFINED, xl=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'lg', 'm', 'mb', 'md', 'ml', 'mr', 'mt', 'mx', 'my', 'offset', 'offsetLg', 'offsetMd', 'offsetSm', 'offsetXl', 'offsetXs', 'order', 'orderLg', 'orderMd', 'orderSm', 'orderXl', 'orderXs', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'sm', 'span', 'style', 'styles', 'sx', 'unstyled', 'xl', 'xs']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'lg', 'm', 'mb', 'md', 'ml', 'mr', 'mt', 'mx', 'my', 'offset', 'offsetLg', 'offsetMd', 'offsetSm', 'offsetXl', 'offsetXs', 'order', 'orderLg', 'orderMd', 'orderSm', 'orderXl', 'orderXs', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'sm', 'span', 'style', 'styles', 'sx', 'unstyled', 'xl', 'xs']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Col, self).__init__(children=children, **args)
