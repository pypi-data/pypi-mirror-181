# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Slider(Component):
    """A Slider component.
Capture user feedback from a range of values. For more information, see: https://mantine.dev/core/slider/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Color from theme.colors.

- disabled (boolean; optional):
    Disables slider.

- labelAlwaysOn (boolean; optional):
    If True label will be not be hidden when user stops dragging.

- labelTransition (a value equal to: 'fade', 'skew-up', 'skew-down', 'rotate-right', 'rotate-left', 'slide-down', 'slide-up', 'slide-right', 'slide-left', 'scale-y', 'scale-x', 'scale', 'pop', 'pop-top-left', 'pop-top-right', 'pop-bottom-left', 'pop-bottom-right'; optional):
    Label appear/disappear transition.

- labelTransitionDuration (number; optional):
    Label appear/disappear transition duration in ms.

- labelTransitionTimingFunction (string; optional):
    Label appear/disappear transition timing function, defaults to
    theme.transitionRimingFunction.

- m (number; optional):
    margin props.

- marks (list of dicts; optional):
    Marks which will be placed on the track.

    `marks` is a list of dicts with keys:

    - label (a list of or a singular dash component, string or number; optional)

    - value (number; required)

- max (number; optional):
    Maximum possible value.

- mb (number; optional):
    margin props.

- min (number; optional):
    Minimal possible value.

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

- precision (number; optional):
    Amount of digits after the decimal point.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- radius (number; optional):
    Track border-radius from theme or number to set border-radius in
    px.

- showLabelOnHover (boolean; optional):
    If True slider label will appear on hover.

- size (number; optional):
    Predefined track and thumb size, number to set sizes in px.

- step (number; optional):
    Number by which value will be incremented/decremented with thumb
    drag and arrows.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- thumbChildren (a list of or a singular dash component, string or number; optional):
    Thumb children, can be used to add icon.

- thumbLabel (string; optional):
    Thumb aria-label.

- thumbSize (number; optional):
    Thumb width and height in px.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- updatemode (a value equal to: 'mouseup', 'drag'; default 'mouseup'):
    Determines when the component should update its value property. If
    mouseup (the default) then the slider will only trigger its value
    when the user has finished dragging the slider. If drag, then the
    slider will update its value continuously as it is being dragged.

- value (number; optional):
    Current value for controlled slider."""
    _children_props = ['marks[].label', 'thumbChildren']
    _base_nodes = ['thumbChildren', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Slider'
    @_explicitize_args
    def __init__(self, value=Component.UNDEFINED, thumbLabel=Component.UNDEFINED, color=Component.UNDEFINED, radius=Component.UNDEFINED, size=Component.UNDEFINED, min=Component.UNDEFINED, max=Component.UNDEFINED, step=Component.UNDEFINED, precision=Component.UNDEFINED, marks=Component.UNDEFINED, labelTransition=Component.UNDEFINED, labelTransitionDuration=Component.UNDEFINED, labelTransitionTimingFunction=Component.UNDEFINED, labelAlwaysOn=Component.UNDEFINED, showLabelOnHover=Component.UNDEFINED, thumbChildren=Component.UNDEFINED, disabled=Component.UNDEFINED, thumbSize=Component.UNDEFINED, updatemode=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'color', 'disabled', 'labelAlwaysOn', 'labelTransition', 'labelTransitionDuration', 'labelTransitionTimingFunction', 'm', 'marks', 'max', 'mb', 'min', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'precision', 'pt', 'px', 'py', 'radius', 'showLabelOnHover', 'size', 'step', 'style', 'styles', 'sx', 'thumbChildren', 'thumbLabel', 'thumbSize', 'unstyled', 'updatemode', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'disabled', 'labelAlwaysOn', 'labelTransition', 'labelTransitionDuration', 'labelTransitionTimingFunction', 'm', 'marks', 'max', 'mb', 'min', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'pr', 'precision', 'pt', 'px', 'py', 'radius', 'showLabelOnHover', 'size', 'step', 'style', 'styles', 'sx', 'thumbChildren', 'thumbLabel', 'thumbSize', 'unstyled', 'updatemode', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Slider, self).__init__(**args)
