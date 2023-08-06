# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LoadingOverlay(Component):
    """A LoadingOverlay component.
Similar to dcc.Loading, overlay over given container with centered Loader from Mantine Theme. For more information, see: https://mantine.dev/core/loading-overlay/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- exitTransitionDuration (number; optional):
    Exit transition duration in ms.

- loader (a list of or a singular dash component, string or number; optional):
    Provide custom loader.

- loaderProps (dict; optional):
    Loader component props.

    `loaderProps` is a dict with keys:

    - color (boolean | number | string | dict | list; optional):
        Loader color from theme.

    - size (number; optional):
        Defines width of loader.

    - variant (a value equal to: 'bars', 'oval', 'dots'; optional):
        Loader appearance.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; required):
        Holds the name of the component that is loading.

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

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

- overlayBlur (number; optional):
    Sets overlay blur in px.

- overlayColor (string; optional):
    Sets overlay color, defaults to theme.white in light theme and to
    theme.colors.dark[5] in dark theme.

- overlayOpacity (number; optional):
    Sets overlay opacity.

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
    Value from theme.radius or number to set border-radius in px.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- transitionDuration (number; optional):
    Animation duration in ms.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- zIndex (number; optional):
    Loading overlay z-index."""
    _children_props = ['loader']
    _base_nodes = ['loader', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'LoadingOverlay'
    @_explicitize_args
    def __init__(self, children=None, loader=Component.UNDEFINED, loaderProps=Component.UNDEFINED, overlayOpacity=Component.UNDEFINED, overlayColor=Component.UNDEFINED, overlayBlur=Component.UNDEFINED, zIndex=Component.UNDEFINED, transitionDuration=Component.UNDEFINED, exitTransitionDuration=Component.UNDEFINED, radius=Component.UNDEFINED, loading_state=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'exitTransitionDuration', 'loader', 'loaderProps', 'loading_state', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'overlayBlur', 'overlayColor', 'overlayOpacity', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'style', 'styles', 'sx', 'transitionDuration', 'unstyled', 'zIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'exitTransitionDuration', 'loader', 'loaderProps', 'loading_state', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'overlayBlur', 'overlayColor', 'overlayOpacity', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'radius', 'style', 'styles', 'sx', 'transitionDuration', 'unstyled', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(LoadingOverlay, self).__init__(children=children, **args)
