"""Nib - Python framework for building native macOS menu bar applications.

Nib lets you write macOS menu bar apps in Python with a declarative,
SwiftUI-inspired API. Python code communicates with a Swift runtime
over Unix sockets using MessagePack serialization.

Quick Start:
    Create a simple menu bar app::

        import nib

        def main(app: nib.App):
            app.title = "My App"
            app.icon = nib.SFSymbol("star.fill")
            app.width = 300
            app.height = 200

            counter = nib.Text("0")

            def increment():
                counter.content = str(int(counter.content) + 1)

            app.build(
                nib.VStack(
                    controls=[counter, nib.Button("Add", action=increment)],
                    spacing=8,
                    padding=16,
                )
            )

        nib.run(main)

Main Components:
    **Core**:
        - :class:`App` - Main application class
        - :class:`SFSymbol` - Apple SF Symbol icons
        - :func:`run` - Application entry point
        - :class:`MenuItem`, :class:`MenuDivider` - Context menu items
        - :class:`UserDefaults` - Persistent storage

    **Views** (Layout):
        - :class:`VStack`, :class:`HStack`, :class:`ZStack` - Stack layouts
        - :class:`ScrollView`, :class:`List` - Scrollable containers
        - :class:`Spacer`, :class:`Divider` - Spacing and separators

    **Views** (Controls):
        - :class:`Text`, :class:`TextField`, :class:`SecureField` - Text
        - :class:`Button`, :class:`Toggle`, :class:`Slider` - Inputs
        - :class:`Picker`, :class:`ProgressView` - Selection and progress
        - :class:`Image`, :class:`Video`, :class:`Label`, :class:`Link` - Media

    **Views** (Shapes):
        - :class:`Rectangle`, :class:`RoundedRectangle` - Rectangles
        - :class:`Circle`, :class:`Ellipse`, :class:`Capsule` - Rounded shapes

    **Views** (Charts):
        - :class:`Chart` - Chart container
        - :class:`LineMark`, :class:`BarMark`, :class:`AreaMark` - Chart marks

    **Types**:
        - :class:`Color`, :class:`Font`, :class:`Animation` - Styling types
        - Various enums for alignment, styles, and transitions

For more information, see the full documentation at:
https://nib.readthedocs.io/
"""

from .core import App, MenuDivider, MenuItem, SFSymbol, State, UserDefaults, run
from . import draw
from .services import (
    Battery,
    BatteryInfo,
    BatteryState,
    Camera,
    CameraDevice,
    CameraFrame,
    CameraPosition,
    Connectivity,
    ConnectivityInfo,
    ConnectionType,
    Keychain,
    Screen,
    ScreenInfo,
)
from .types import (
    Alignment,
    # Core types
    Animation,
    AttributedString,
    BlendMode,
    BorderShape,
    ButtonRole,
    # Button enums
    ButtonStyle,
    Color,
    ContentMode,
    # Transition enums
    ContentTransition,
    ControlSize,
    # Custom transitions
    CustomTransitionBuilder,
    Font,
    FontWeight,
    # Alignment enums
    HorizontalAlignment,
    # Image enums
    ImageRenderingMode,
    LabelStyle,
    Offset,
    PickerStyle,
    ProgressStyle,
    ScrollAxis,
    SymbolRenderingMode,
    SymbolScale,
    TextCase,
    TextFieldStyle,
    TextStyle,
    # Control style enums
    ToggleStyle,
    Transition,
    TransitionConfig,
    # Text enums
    TruncationMode,
    VerticalAlignment,
)
from .views import (
    AngularGradient,
    AreaMark,
    BarMark,
    BlurStyle,
    Button,
    # Canvas (Core Graphics drawing)
    Canvas,
    PanEvent,
    Capsule,
    # Charts
    Chart,
    ChartAxis,
    ChartLegend,
    Circle,
    DisclosureGroup,
    Divider,
    Ellipse,
    EllipticalGradient,
    # New controls
    Gauge,
    GaugeStyle,
    # Grid layouts
    Grid,
    GridItem,
    GridItemSize,
    GridRow,
    Group,
    HStack,
    Image,
    InterpolationMethod,
    Label,
    LazyHGrid,
    LazyVGrid,
    # Gradients
    LinearGradient,
    LineMark,
    Link,
    List,
    Map,
    MapAnnotation,
    MapCircle,
    MapInteractionMode,
    MapMarker,
    MapPolygon,
    MapPolyline,
    MapStyle,
    Markdown,
    NavigationLink,
    NavigationStack,
    Picker,
    PointMark,
    ProgressView,
    RadialGradient,
    Rectangle,
    RectMark,
    # Shapes
    RoundedRectangle,
    RuleMark,
    ScrollView,
    Section,
    SectorMark,
    SecureField,
    ShareLink,
    Slider,
    Spacer,
    StackingMethod,
    SymbolShape,
    Table,
    TableColumn,
    # Controls
    Text,
    TextEditor,
    TextField,
    Toggle,
    Video,
    VideoGravity,
    # Base
    View,
    # Effects
    VisualEffectBlur,
    # Layout
    VStack,
    ZStack,
    # Camera
    CameraPreview,
    # WebView
    WebView,
)

__version__ = "0.1.0"
__all__ = [
    # Core
    "App",
    "State",
    "SFSymbol",
    "run",
    "MenuItem",
    "MenuDivider",
    "UserDefaults",
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
    # Canvas
    "Canvas",
    "PanEvent",
    "draw",
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
    # Core Types
    "Animation",
    "AttributedString",
    "Color",
    "Font",
    "FontWeight",
    "Offset",
    "TextStyle",
    # Button Enums
    "ButtonStyle",
    "ButtonRole",
    "BorderShape",
    "ControlSize",
    "LabelStyle",
    # Control Style Enums
    "ToggleStyle",
    "TextFieldStyle",
    "PickerStyle",
    "ProgressStyle",
    # Text Enums
    "TruncationMode",
    "TextCase",
    # Image Enums
    "ImageRenderingMode",
    "SymbolScale",
    "SymbolRenderingMode",
    "ContentMode",
    # Alignment Enums
    "HorizontalAlignment",
    "VerticalAlignment",
    "Alignment",
    "ScrollAxis",
    # Transition Enums
    "ContentTransition",
    "Transition",
    "TransitionConfig",
    "CustomTransitionBuilder",
    "BlendMode",
    # Services
    "Battery",
    "BatteryInfo",
    "BatteryState",
    "Camera",
    "CameraDevice",
    "CameraFrame",
    "CameraPosition",
    "CameraPreview",
    "WebView",
    "Connectivity",
    "ConnectivityInfo",
    "ConnectionType",
    "Screen",
    "ScreenInfo",
    "Keychain",
]
