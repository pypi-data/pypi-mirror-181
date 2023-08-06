# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SimpleGrid(Component):
    """A SimpleGrid component.
Responsive grid where each item takes equal amount of space. For more information, see: https://mantine.dev/core/simple-grid/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- breakpoints (list of dicts; optional):
    Breakpoints data to change items per row and spacing based on
    max-width.

    `breakpoints` is a list of dicts with keys:

    - cols (number; required)

    - maxWidth (number; optional)

    - minWidth (number; optional)

    - spacing (number; optional)

    - verticalSpacing (number; optional)

- className (string; optional):
    Often used with CSS to style elements with common properties.

- cols (number; optional):
    Default amount of columns, used when none of breakpoints can be
    applied.

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

- spacing (number; optional):
    Spacing between columns, used when none of breakpoints can be
    applied.

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
    Vertical spacing between columns, used when none of breakpoints
    can be applied."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'SimpleGrid'
    @_explicitize_args
    def __init__(self, children=None, breakpoints=Component.UNDEFINED, cols=Component.UNDEFINED, spacing=Component.UNDEFINED, verticalSpacing=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'breakpoints', 'className', 'cols', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'spacing', 'style', 'styles', 'sx', 'unstyled', 'verticalSpacing']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'breakpoints', 'className', 'cols', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'spacing', 'style', 'styles', 'sx', 'unstyled', 'verticalSpacing']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(SimpleGrid, self).__init__(children=children, **args)
