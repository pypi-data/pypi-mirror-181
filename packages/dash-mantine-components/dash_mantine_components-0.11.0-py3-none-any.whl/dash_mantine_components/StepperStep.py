# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class StepperStep(Component):
    """A StepperStep component.
Display content divided into a steps sequence. For more information, see: https://mantine.dev/core/stepper/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    StepperStep content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- allowStepClick (boolean; optional):
    Set to False to disable clicks on step.

- allowStepSelect (boolean; optional):
    Should step selection be allowed.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (boolean | number | string | dict | list; optional):
    Step color from theme.colors.

- completedIcon (a list of or a singular dash component, string or number; optional):
    Step icon displayed when step is completed.

- description (a list of or a singular dash component, string or number; optional):
    Step description.

- icon (a list of or a singular dash component, string or number; optional):
    Step icon, defaults to step index + 1 when rendered within
    Stepper.

- iconPosition (a value equal to: 'right', 'left'; optional):
    Icon position relative to step body.

- iconSize (number; optional):
    Icon wrapper size in px.

- label (a list of or a singular dash component, string or number; optional):
    Step label, render after icon.

- loading (boolean; optional):
    Indicates loading state on step.

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

- orientation (a value equal to: 'vertical', 'horizontal'; optional):
    Component orientation.

- p (number; optional):
    padding props.

- pb (number; optional):
    padding props.

- pl (number; optional):
    padding props.

- pr (number; optional):
    padding props.

- progressIcon (a list of or a singular dash component, string or number; optional):
    Step icon displayed when step is in progress.

- pt (number; optional):
    padding props.

- px (number; optional):
    padding props.

- py (number; optional):
    padding props.

- radius (number; optional):
    Radius from theme.radius, or number to set border-radius in px.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Component size.

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

- withIcon (boolean; optional):
    Should icon be displayed."""
    _children_props = ['icon', 'completedIcon', 'progressIcon', 'label', 'description']
    _base_nodes = ['icon', 'completedIcon', 'progressIcon', 'label', 'description', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'StepperStep'
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, withIcon=Component.UNDEFINED, icon=Component.UNDEFINED, completedIcon=Component.UNDEFINED, progressIcon=Component.UNDEFINED, label=Component.UNDEFINED, description=Component.UNDEFINED, iconSize=Component.UNDEFINED, iconPosition=Component.UNDEFINED, size=Component.UNDEFINED, radius=Component.UNDEFINED, loading=Component.UNDEFINED, allowStepClick=Component.UNDEFINED, allowStepSelect=Component.UNDEFINED, orientation=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, styles=Component.UNDEFINED, id=Component.UNDEFINED, unstyled=Component.UNDEFINED, sx=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'allowStepClick', 'allowStepSelect', 'className', 'color', 'completedIcon', 'description', 'icon', 'iconPosition', 'iconSize', 'label', 'loading', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'orientation', 'p', 'pb', 'pl', 'pr', 'progressIcon', 'pt', 'px', 'py', 'radius', 'size', 'style', 'styles', 'sx', 'unstyled', 'withIcon']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'allowStepClick', 'allowStepSelect', 'className', 'color', 'completedIcon', 'description', 'icon', 'iconPosition', 'iconSize', 'label', 'loading', 'm', 'mb', 'ml', 'mr', 'mt', 'mx', 'my', 'orientation', 'p', 'pb', 'pl', 'pr', 'progressIcon', 'pt', 'px', 'py', 'radius', 'size', 'style', 'styles', 'sx', 'unstyled', 'withIcon']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(StepperStep, self).__init__(children=children, **args)
