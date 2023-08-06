# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Alert(Component):
    """An Alert component.
Attract user attention with important static message. For more information, see: https://mantine.dev/core/alert/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Alert message.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- closeButtonLabel (string; optional):
    Close button aria-label.

- color (boolean | number | string | dict | list; optional):
    Color from theme.colors.

- duration (number; optional):
    Duration in milliseconds after which the Alert dismisses itself.

- hide (boolean; default False):
    Whether to hide the alert.

- icon (a list of or a singular dash component, string or number; optional):
    Icon displayed next to title.

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
    Radius from theme.radius, or number to set border-radius in px,
    defaults to theme.defaultRadius.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- title (a list of or a singular dash component, string or number; optional):
    Alert title.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (a value equal to: 'filled', 'outline', 'light'; optional):
    Controls Alert background, color and border styles, defaults to
    light.

- withCloseButton (boolean; optional):
    True to display close button."""
    _children_props = ['title', 'icon']
    _base_nodes = ['title', 'icon', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Alert'
    @_explicitize_args
    def __init__(self, children=None, title=Component.UNDEFINED, variant=Component.UNDEFINED, color=Component.UNDEFINED, icon=Component.UNDEFINED, withCloseButton=Component.UNDEFINED, radius=Component.UNDEFINED, duration=Component.UNDEFINED, hide=Component.UNDEFINED, closeButtonLabel=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'closeButtonLabel', 'color', 'duration', 'hide', 'icon', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'style', 'styles', 'sx', 'title', 'unstyled', 'variant', 'withCloseButton']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'closeButtonLabel', 'color', 'duration', 'hide', 'icon', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'style', 'styles', 'sx', 'title', 'unstyled', 'variant', 'withCloseButton']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Alert, self).__init__(children=children, **args)
