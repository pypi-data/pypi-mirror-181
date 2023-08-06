# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Timeline(Component):
    """A Timeline component.
Display list of events in chronological order. For more information, see: https://mantine.dev/core/timeline/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    dmc.TimelineItem components only.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- active (number; optional):
    Index of active element.

- align (a value equal to: 'right', 'left'; optional):
    Timeline alignment.

- bulletSize (number; optional):
    Bullet size in px.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Active color from theme.

- lineWidth (number; optional):
    Line width in px.

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
    Radius from theme.radius, or number to set border-radius in px.

- reverseActive (boolean; optional):
    Reverse active direction without reversing items.

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
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'Timeline'
    @_explicitize_args
    def __init__(self, children=None, active=Component.UNDEFINED, color=Component.UNDEFINED, radius=Component.UNDEFINED, bulletSize=Component.UNDEFINED, align=Component.UNDEFINED, lineWidth=Component.UNDEFINED, reverseActive=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'active', 'align', 'bulletSize', 'className', 'color', 'lineWidth', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'reverseActive', 'style', 'styles', 'sx', 'unstyled']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'active', 'align', 'bulletSize', 'className', 'color', 'lineWidth', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'reverseActive', 'style', 'styles', 'sx', 'unstyled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Timeline, self).__init__(children=children, **args)
