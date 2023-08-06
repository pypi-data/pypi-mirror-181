# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Blockquote(Component):
    """A Blockquote component.
Blockquote with optional cite. For more information, see: https://mantine.dev/core/blockquote/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- cite (a list of or a singular dash component, string or number; optional):
    Describe a reference to a cited quote.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Icon color from theme.

- icon (a list of or a singular dash component, string or number; optional):
    Icon, defaults to quote icon.

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

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component."""
    _children_props = ['icon', 'cite']
    _base_nodes = ['icon', 'cite', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Blockquote'
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, icon=Component.UNDEFINED, cite=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'cite', 'className', 'color', 'icon', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'style', 'styles', 'sx', 'unstyled']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'cite', 'className', 'color', 'icon', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'style', 'styles', 'sx', 'unstyled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Blockquote, self).__init__(children=children, **args)
