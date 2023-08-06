# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class List(Component):
    """A List component.
Display ordered or unordered list, see: https://mantine.dev/core/list/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    dmc.ListItem components only.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- center (boolean; optional):
    Center items with icon.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- icon (a list of or a singular dash component, string or number; optional):
    Icon that should replace list item dot.

- listStyleType (a value equal to: 'disc', 'circle', 'square', 'decimal', 'lower-roman', 'upper-roman', 'lower-greek', 'lower-latin', 'upper-latin', 'lower-alpha', 'upper-alpha', 'none', 'inherit'; optional):
    List style.

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

- size (number; optional):
    Font size from theme or number to set value in px.

- spacing (number; optional):
    Spacing between items from theme or number to set value in px.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- type (a value equal to: 'ordered', 'unordered'; optional):
    List type: ol or ul.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- withPadding (boolean; optional):
    Include padding-left to offset list from main content."""
    _children_props = ['icon']
    _base_nodes = ['icon', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'List'
    @_explicitize_args
    def __init__(self, children=None, type=Component.UNDEFINED, withPadding=Component.UNDEFINED, size=Component.UNDEFINED, icon=Component.UNDEFINED, spacing=Component.UNDEFINED, center=Component.UNDEFINED, listStyleType=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'center', 'className', 'icon', 'listStyleType', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'size', 'spacing', 'style', 'styles', 'sx', 'type', 'unstyled', 'withPadding']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'center', 'className', 'icon', 'listStyleType', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'size', 'spacing', 'style', 'styles', 'sx', 'type', 'unstyled', 'withPadding']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(List, self).__init__(children=children, **args)
