# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Image(Component):
    """An Image component.
Image with optional placeholder for loading and error state. For more information, see: https://mantine.dev/core/image/

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- alt (string; optional):
    Image alt text, used as title for placeholder if image was not
    loaded.

- caption (a list of or a singular dash component, string or number; optional):
    Image figcaption, displayed bellow image.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- fit (a value equal to: 'contain', 'cover'; optional):
    Image object-fit property.

- height (string | number; optional):
    Image height, defaults to original image height adjusted to given
    width.

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

- placeholder (a list of or a singular dash component, string or number; optional):
    Customize placeholder content.

- pr (number; optional):
    padding props.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- radius (number; optional):
    Predefined border-radius value from theme.radius or number for
    border-radius in px.

- src (string; optional):
    Image src.

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

- width (string | number; optional):
    Image width, defaults to 100%, cannot exceed 100%.

- withPlaceholder (boolean; optional):
    Enable placeholder when image is loading and when image fails to
    load."""
    _children_props = ['placeholder', 'caption']
    _base_nodes = ['placeholder', 'caption', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Image'
    @_explicitize_args
    def __init__(self, src=Component.UNDEFINED, alt=Component.UNDEFINED, fit=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, radius=Component.UNDEFINED, withPlaceholder=Component.UNDEFINED, placeholder=Component.UNDEFINED, caption=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'alt', 'caption', 'className', 'fit', 'height', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'placeholder', 'pr', 'pt', 'px', 'py', 'radius', 'src', 'style', 'styles', 'sx', 'unstyled', 'width', 'withPlaceholder']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alt', 'caption', 'className', 'fit', 'height', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'placeholder', 'pr', 'pt', 'px', 'py', 'radius', 'src', 'style', 'styles', 'sx', 'unstyled', 'width', 'withPlaceholder']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Image, self).__init__(**args)
