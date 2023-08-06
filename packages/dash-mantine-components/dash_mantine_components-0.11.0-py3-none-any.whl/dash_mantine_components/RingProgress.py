# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RingProgress(Component):
    """A RingProgress component.
Give user feedback for status of the task with circle diagram. For more information, see: https://mantine.dev/core/ring-progress/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- label (a list of or a singular dash component, string or number; optional):
    Label displayed in the center of the ring.

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

- roundCaps (boolean; optional):
    Sets whether the edges of the progress circle are rounded.

- sections (list of dicts; required):
    Ring sections.

    `sections` is a list of dicts with keys:

    - color (boolean | number | string | dict | list; required)

    - tooltip (a list of or a singular dash component, string or number; optional)

    - value (number; required)

- size (number; optional):
    Width and height of the progress ring in px.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- thickness (number; optional):
    Ring thickness.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component."""
    _children_props = ['label', 'sections[].tooltip']
    _base_nodes = ['label', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'RingProgress'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, thickness=Component.UNDEFINED, size=Component.UNDEFINED, roundCaps=Component.UNDEFINED, sections=Component.REQUIRED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'roundCaps', 'sections', 'size', 'style', 'styles', 'sx', 'thickness', 'unstyled']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'label', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'roundCaps', 'sections', 'size', 'style', 'styles', 'sx', 'thickness', 'unstyled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['sections']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(RingProgress, self).__init__(**args)
