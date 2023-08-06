# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Anchor(Component):
    """An Anchor component.
Display links with theme styles. For more information, see: https://mantine.dev/core/anchor/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align (a value equal to: 'initial', 'inherit', '-moz-initial', 'revert', 'unset', 'left', 'right', 'center', 'end', 'start', 'justify', 'match-parent'; optional):
    Sets text-align css property.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Key of theme.colors or any valid CSS color.

- gradient (dict; optional):
    Controls gradient settings in gradient variant only.

    `gradient` is a dict with keys:

    - deg (number; optional)

    - from (string; required)

    - to (string; required)

- href (string; required):
    href.

- inherit (boolean; optional):
    Inherit font properties from parent element.

- inline (boolean; optional):
    Sets line-height to 1 for centering.

- italic (boolean; optional):
    Adds font-style: italic style.

- lineClamp (number; optional):
    CSS -webkit-line-clamp property.

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

- refresh (boolean; optional):
    Whether to refresh the page.

- size (number; optional):
    Key of theme.fontSizes or number to set font-size in px.

- span (boolean; optional):
    Shorthand for component=\"span\".

- strikethrough (boolean; optional):
    Add strikethrough styles.

- style (boolean | number | string | dict | list; optional):
    Inline style.

- styles (dict; optional):
    Mantine styles API.

- sx (boolean | number | string | dict | list; optional):
    With sx you can add styles to component root element. If you need
    to customize styles of other elements within component use styles
    prop.

- target (a value equal to: '_blank', '_self'; optional):
    Target.

- transform (a value equal to: 'initial', 'inherit', '-moz-initial', 'revert', 'unset', 'none', 'capitalize', 'full-size-kana', 'full-width', 'lowercase', 'uppercase'; optional):
    Sets text-transform css property.

- underline (boolean; optional):
    Underline the text.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (a value equal to: 'gradient', 'text', 'link'; optional):
    Link or text variant.

- weight (number; optional):
    Sets font-weight css property."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'Anchor'
    @_explicitize_args
    def __init__(self, children=None, target=Component.UNDEFINED, href=Component.REQUIRED, refresh=Component.UNDEFINED, size=Component.UNDEFINED, color=Component.UNDEFINED, weight=Component.UNDEFINED, transform=Component.UNDEFINED, align=Component.UNDEFINED, variant=Component.UNDEFINED, lineClamp=Component.UNDEFINED, inline=Component.UNDEFINED, underline=Component.UNDEFINED, strikethrough=Component.UNDEFINED, italic=Component.UNDEFINED, inherit=Component.UNDEFINED, gradient=Component.UNDEFINED, span=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'align', 'className', 'color', 'gradient', 'href', 'inherit', 'inline', 'italic', 'lineClamp', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'refresh', 'size', 'span', 'strikethrough', 'style', 'styles', 'sx', 'target', 'transform', 'underline', 'unstyled', 'variant', 'weight']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'align', 'className', 'color', 'gradient', 'href', 'inherit', 'inline', 'italic', 'lineClamp', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'p', 'pb', 'pl', 'pr', 'pt', 'px', 'py', 'refresh', 'size', 'span', 'strikethrough', 'style', 'styles', 'sx', 'target', 'transform', 'underline', 'unstyled', 'variant', 'weight']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['href']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Anchor, self).__init__(children=children, **args)
