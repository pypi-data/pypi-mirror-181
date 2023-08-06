# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Table(Component):
    """A Table component.
A simple table component. For more information, see: https://mantine.dev/core/table/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Children, specifically an HTML representation of the table.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- captionSide (a value equal to: 'top', 'bottom'; optional):
    Table caption position.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- fontSize (number; optional):
    Sets font size of all text inside table.

- highlightOnHover (boolean; optional):
    If True row will have hover color.

- horizontalSpacing (number; optional):
    Horizontal cells spacing from theme.spacing or number to set value
    in px.

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

- striped (boolean; optional):
    If True every odd row of table will have gray background color.

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

- verticalSpacing (number; optional):
    Vertical cells spacing from theme.spacing or number to set value
    in px.

- withBorder (boolean; optional):
    Add border to table.

- withColumnBorders (boolean; optional):
    Add border to columns."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'Table'
    @_explicitize_args
    def __init__(self, children=None, striped=Component.UNDEFINED, highlightOnHover=Component.UNDEFINED, captionSide=Component.UNDEFINED, horizontalSpacing=Component.UNDEFINED, verticalSpacing=Component.UNDEFINED, fontSize=Component.UNDEFINED, withBorder=Component.UNDEFINED, withColumnBorders=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'captionSide', 'className', 'fontSize', 'highlightOnHover', 'horizontalSpacing', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'striped', 'style', 'styles', 'sx', 'unstyled', 'verticalSpacing', 'withBorder', 'withColumnBorders']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'captionSide', 'className', 'fontSize', 'highlightOnHover', 'horizontalSpacing', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'striped', 'style', 'styles', 'sx', 'unstyled', 'verticalSpacing', 'withBorder', 'withColumnBorders']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Table, self).__init__(children=children, **args)
