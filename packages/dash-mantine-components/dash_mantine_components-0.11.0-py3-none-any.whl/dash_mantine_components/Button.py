# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.
Render button or link with button styles from mantine theme. For more information, see: https://mantine.dev/core/button/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Button label.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Button color from theme.

- compact (boolean; optional):
    Reduces vertical and horizontal spacing.

- disabled (boolean; optional):
    Disabled state.

- fullWidth (boolean; optional):
    Sets button width to 100% of parent element.

- gradient (dict; optional):
    Controls gradient settings in gradient variant only.

    `gradient` is a dict with keys:

    - deg (number; optional)

    - from (string; required)

    - to (string; required)

- leftIcon (a list of or a singular dash component, string or number; optional):
    Adds icon before button label.

- loaderPosition (a value equal to: 'left', 'right'; optional):
    Loader position relative to button label.

- loaderProps (dict; optional):
    Props spread to Loader component.

    `loaderProps` is a dict with keys:

    - color (boolean | number | string | dict | list; optional):
        Loader color from theme.

    - size (number; optional):
        Defines width of loader.

    - variant (a value equal to: 'bars', 'oval', 'dots'; optional):
        Loader appearance.

- loading (boolean; optional):
    Indicate loading state.

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

- radius (number; optional):
    Button border-radius from theme or number to set border-radius in
    px.

- rightIcon (a list of or a singular dash component, string or number; optional):
    Adds icon after button label.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Predefined button size.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- type (a value equal to: 'submit', 'button', 'reset'; optional):
    Button type attribute.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- uppercase (boolean; optional):
    Set text-transform to uppercase.

- variant (a value equal to: 'filled', 'outline', 'light', 'white', 'default', 'subtle', 'gradient'; optional):
    Controls button appearance."""
    _children_props = ['leftIcon', 'rightIcon']
    _base_nodes = ['leftIcon', 'rightIcon', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Button'
    @_explicitize_args
    def __init__(self, children=None, size=Component.UNDEFINED, type=Component.UNDEFINED, color=Component.UNDEFINED, leftIcon=Component.UNDEFINED, rightIcon=Component.UNDEFINED, fullWidth=Component.UNDEFINED, radius=Component.UNDEFINED, variant=Component.UNDEFINED, gradient=Component.UNDEFINED, uppercase=Component.UNDEFINED, compact=Component.UNDEFINED, loading=Component.UNDEFINED, loaderProps=Component.UNDEFINED, loaderPosition=Component.UNDEFINED, disabled=Component.UNDEFINED, n_clicks=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'color', 'compact', 'disabled', 'fullWidth', 'gradient', 'leftIcon', 'loaderPosition', 'loaderProps', 'loading', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'n_clicks', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'rightIcon', 'size', 'style', 'styles', 'sx', 'type', 'unstyled', 'uppercase', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'color', 'compact', 'disabled', 'fullWidth', 'gradient', 'leftIcon', 'loaderPosition', 'loaderProps', 'loading', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'n_clicks', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'rightIcon', 'size', 'style', 'styles', 'sx', 'type', 'unstyled', 'uppercase', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Button, self).__init__(children=children, **args)
