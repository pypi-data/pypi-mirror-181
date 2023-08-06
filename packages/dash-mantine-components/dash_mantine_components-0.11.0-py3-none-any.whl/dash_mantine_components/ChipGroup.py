# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ChipGroup(Component):
    """A ChipGroup component.
Pick one or multiple values with inline controls. For more information, see: https://mantine.dev/core/chip/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Chip components only.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align (a value equal to: 'center', 'flex-start', 'flex-end', 'baseline', 'stretch'; optional):
    Defines align-items css property.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- grow (boolean; optional):
    Defines flex-grow property for each element, True -> 1, False ->
    0.

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

- multiple (boolean; optional):
    Allow multiple values to be selected at a time.

- mx (number; optional):
    margin props.

- my (number; optional):
    margin props.

- noWrap (boolean; optional):
    Defined flex-wrap property.

- p (number; optional):
    padding props.

- pb (number; optional):
    padding props.

- persisted_props (list of strings; default ["value"]):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- pl (number; optional):
    padding props.

- position (a value equal to: 'right', 'center', 'left', 'apart'; optional):
    Defines justify-content property.

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- spacing (number; optional):
    Space between elements.

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

- value (list of strings; optional):
    Value of currently selected Chip."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'ChipGroup'
    @_explicitize_args
    def __init__(self, children=None, value=Component.UNDEFINED, multiple=Component.UNDEFINED, position=Component.UNDEFINED, noWrap=Component.UNDEFINED, grow=Component.UNDEFINED, spacing=Component.UNDEFINED, align=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'align', 'className', 'grow', 'm', 'mb', 'ml', 'mr', 'mt', 'multiple', 'mx', 'my', 'noWrap', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'position', 'pr', 'pt', 'px', 'py', 'spacing', 'style', 'styles', 'sx', 'unstyled', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'align', 'className', 'grow', 'm', 'mb', 'ml', 'mr', 'mt', 'multiple', 'mx', 'my', 'noWrap', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'position', 'pr', 'pt', 'px', 'py', 'spacing', 'style', 'styles', 'sx', 'unstyled', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(ChipGroup, self).__init__(children=children, **args)
