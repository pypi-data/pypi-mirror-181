# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CheckboxGroup(Component):
    """A CheckboxGroup component.
Capture boolean input from user. For more information, see: https://mantine.dev/core/checkbox/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    dmc.Checkbox components only.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- description (a list of or a singular dash component, string or number; optional):
    Input description, displayed after label.

- error (a list of or a singular dash component, string or number; optional):
    Displays error message after input.

- inputWrapperOrder (list of a value equal to: 'label', 'description', 'error', 'input's; optional):
    Controls order of the Input.Wrapper elements.

- label (a list of or a singular dash component, string or number; optional):
    Input label, displayed before input.

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

- offset (number; optional):
    Space between label and inputs.

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    Horizontal or vertical orientation.

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

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- required (boolean; optional):
    Adds required attribute to the input and red asterisk on the right
    side of label.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Predefined label fontSize, checkbox width, height and
    border-radius.

- spacing (number; optional):
    Spacing between checkboxes in horizontal orientation.

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
    Value of currently selected checkbox.

- withAsterisk (boolean; optional):
    Determines whether required asterisk should be rendered, overrides
    required prop, does not add required attribute to the input."""
    _children_props = ['label', 'description', 'error']
    _base_nodes = ['label', 'description', 'error', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'CheckboxGroup'
    @_explicitize_args
    def __init__(self, children=None, value=Component.UNDEFINED, orientation=Component.UNDEFINED, spacing=Component.UNDEFINED, offset=Component.UNDEFINED, size=Component.UNDEFINED, label=Component.UNDEFINED, description=Component.UNDEFINED, error=Component.UNDEFINED, required=Component.UNDEFINED, withAsterisk=Component.UNDEFINED, inputWrapperOrder=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'description', 'error', 'inputWrapperOrder', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'offset', 'orientation', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'pt', 'px', 'py', 'required', 'size', 'spacing', 'style', 'styles', 'sx', 'unstyled', 'value', 'withAsterisk']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'description', 'error', 'inputWrapperOrder', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'offset', 'orientation', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'pt', 'px', 'py', 'required', 'size', 'spacing', 'style', 'styles', 'sx', 'unstyled', 'value', 'withAsterisk']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(CheckboxGroup, self).__init__(children=children, **args)
