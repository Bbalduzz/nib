"""Nib view components for building user interfaces.

This module exports all view types available in Nib for building
macOS menu bar application interfaces.

View Categories:
    **Base**:
        - :class:`View` - Base class for all views

    **Layout Containers**:
        - :class:`VStack` - Vertical stack layout
        - :class:`HStack` - Horizontal stack layout
        - :class:`ZStack` - Overlay/depth stack layout
        - :class:`ScrollView` - Scrollable container
        - :class:`List` - Data-driven list
        - :class:`Section` - Grouped content with header/footer
        - :class:`Group` - Logical grouping without layout
        - :class:`Spacer` - Flexible spacing
        - :class:`NavigationStack`, :class:`NavigationLink` - Navigation
        - :class:`DisclosureGroup` - Expandable content

    **Controls**:
        - :class:`Text` - Static/dynamic text display
        - :class:`Button` - Clickable button
        - :class:`TextField`, :class:`SecureField` - Text input
        - :class:`Toggle` - On/off switch
        - :class:`Slider` - Value slider
        - :class:`Picker` - Selection picker
        - :class:`ProgressView` - Progress indicator
        - :class:`Label` - Icon + text combination
        - :class:`Link` - Clickable URL link
        - :class:`Image`, :class:`Video` - Media display
        - :class:`Divider` - Visual separator

    **Shapes**:
        - :class:`Rectangle`, :class:`RoundedRectangle` - Rectangles
        - :class:`Circle`, :class:`Ellipse` - Circular shapes
        - :class:`Capsule` - Pill/capsule shape

    **Charts**:
        - :class:`Chart` - Chart container
        - :class:`LineMark`, :class:`BarMark`, :class:`AreaMark` - Chart marks
        - :class:`PointMark`, :class:`RuleMark`, :class:`RectMark` - More marks
        - :class:`SectorMark` - Pie/donut chart sectors
        - :class:`ChartAxis`, :class:`ChartLegend` - Chart configuration

Example:
    Building a simple interface::

        import nib

        app.build(
            nib.VStack(
                controls=[
                    nib.Text("Hello", font=nib.Font.TITLE),
                    nib.Button("Click Me", action=on_click),
                ],
                spacing=8,
                padding=16,
            )
        )
"""

from .base import View
from .layout import (
    VStack,
    HStack,
    ZStack,
    Spacer,
    ScrollView,
    List,
    Section,
    Group,
    NavigationStack,
    NavigationLink,
    DisclosureGroup,
    # Grid layouts
    Grid,
    GridRow,
    LazyVGrid,
    LazyHGrid,
    GridItem,
    GridItemSize,
)
from .controls import (
    Text,
    Button,
    Divider,
    TextField,
    SecureField,
    Toggle,
    Slider,
    Picker,
    ProgressView,
    Label,
    Link,
    Image,
    Video,
    VideoGravity,
    Markdown,
    Map,
    MapMarker,
    MapAnnotation,
    MapCircle,
    MapPolyline,
    MapPolygon,
    MapStyle,
    MapInteractionMode,
    # New controls
    Gauge,
    GaugeStyle,
    TextEditor,
    Table,
    TableColumn,
    ShareLink,
    CameraPreview,
)
from .shapes import (
    RoundedRectangle,
    Circle,
    Rectangle,
    Ellipse,
    Capsule,
    LinearGradient,
    RadialGradient,
    AngularGradient,
    EllipticalGradient,
)
from .effects import (
    VisualEffectBlur,
    BlurStyle,
)
from .charts import (
    Chart,
    LineMark,
    BarMark,
    AreaMark,
    PointMark,
    RuleMark,
    RectMark,
    SectorMark,
    ChartAxis,
    ChartLegend,
    InterpolationMethod,
    StackingMethod,
    SymbolShape,
)

__all__ = [
    # Base
    "View",
    # Layout
    "VStack",
    "HStack",
    "ZStack",
    "Spacer",
    "ScrollView",
    "List",
    "Section",
    "Group",
    "NavigationStack",
    "NavigationLink",
    "DisclosureGroup",
    # Grid layouts
    "Grid",
    "GridRow",
    "LazyVGrid",
    "LazyHGrid",
    "GridItem",
    "GridItemSize",
    # Controls
    "Text",
    "Button",
    "Divider",
    "TextField",
    "SecureField",
    "Toggle",
    "Slider",
    "Picker",
    "ProgressView",
    "Label",
    "Link",
    "Image",
    "Video",
    "VideoGravity",
    "Markdown",
    "Map",
    "MapMarker",
    "MapAnnotation",
    "MapCircle",
    "MapPolyline",
    "MapPolygon",
    "MapStyle",
    "MapInteractionMode",
    # New controls
    "Gauge",
    "GaugeStyle",
    "TextEditor",
    "Table",
    "TableColumn",
    "ShareLink",
    "CameraPreview",
    # Shapes
    "RoundedRectangle",
    "Circle",
    "Rectangle",
    "Ellipse",
    "Capsule",
    # Gradients
    "LinearGradient",
    "RadialGradient",
    "AngularGradient",
    "EllipticalGradient",
    # Effects
    "VisualEffectBlur",
    "BlurStyle",
    # Charts
    "Chart",
    "LineMark",
    "BarMark",
    "AreaMark",
    "PointMark",
    "RuleMark",
    "RectMark",
    "SectorMark",
    "ChartAxis",
    "ChartLegend",
    "InterpolationMethod",
    "StackingMethod",
    "SymbolShape",
]
