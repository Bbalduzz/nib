"""
Nib - Python-SwiftUI Bridge for macOS Status Bar Apps

Write native macOS status bar apps in Python with a SwiftUI-like declarative API.
"""

from .core import App, State, SFSymbol, run, MenuItem, MenuDivider
from .views import (
    # Base
    View,
    # Layout
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
    # Controls
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
    # Shapes
    RoundedRectangle,
    Circle,
    Rectangle,
    Ellipse,
    Capsule,
    # Charts
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
from .types import (
    # Core types
    Animation,
    Color,
    Font,
    FontWeight,
    TextStyle,
    # Button enums
    ButtonStyle,
    ButtonRole,
    BorderShape,
    ControlSize,
    LabelStyle,
    # Control style enums
    ToggleStyle,
    TextFieldStyle,
    PickerStyle,
    ProgressStyle,
    # Text enums
    TruncationMode,
    TextCase,
    # Image enums
    ImageRenderingMode,
    SymbolScale,
    SymbolRenderingMode,
    ContentMode,
    # Alignment enums
    HorizontalAlignment,
    VerticalAlignment,
    Alignment,
    ScrollAxis,
    # Transition enums
    ContentTransition,
    Transition,
    BlendMode,
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
    # Shapes
    "RoundedRectangle",
    "Circle",
    "Rectangle",
    "Ellipse",
    "Capsule",
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
    "Color",
    "Font",
    "FontWeight",
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
    "BlendMode",
]
