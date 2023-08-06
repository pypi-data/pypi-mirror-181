# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MenuItem(Component):
    """A MenuItem component.
Combine a list of secondary actions into single interactive area. For more information, see: https://mantine.dev/core/menu/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Item label.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- closeMenuOnClick (boolean; optional):
    Determines whether menu should be closed when item is clicked,
    overrides closeOnItemClick prop on Menu component.

- color (boolean | number | string | dict | list; optional):
    Key of theme.colors.

- disabled (boolean; optional):
    Is item disabled.

- href (string; optional):
    href if MenuItem is supposed to be used as a link.

- icon (a list of or a singular dash component, string or number; optional):
    Icon rendered on the left side of the label.

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

- refresh (boolean; optional):
    Whether to refresh the page.

- rightSection (a list of or a singular dash component, string or number; optional):
    Section rendered on the right side of the label.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- target (a value equal to: '_blank', '_self'; optional):
    Target if MenuItem is supposed to be used as a link.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component."""
    _children_props = ['icon', 'rightSection']
    _base_nodes = ['icon', 'rightSection', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'MenuItem'
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, closeMenuOnClick=Component.UNDEFINED, icon=Component.UNDEFINED, rightSection=Component.UNDEFINED, disabled=Component.UNDEFINED, href=Component.UNDEFINED, n_clicks=Component.UNDEFINED, target=Component.UNDEFINED, refresh=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'closeMenuOnClick', 'color', 'disabled', 'href', 'icon', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'n_clicks', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'refresh', 'rightSection', 'style', 'styles', 'sx', 'target', 'unstyled']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'closeMenuOnClick', 'color', 'disabled', 'href', 'icon', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'n_clicks', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'refresh', 'rightSection', 'style', 'styles', 'sx', 'target', 'unstyled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(MenuItem, self).__init__(children=children, **args)
