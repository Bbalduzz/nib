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

from .core import App, State, SFSymbol, run, MenuItem, MenuDivider, UserDefaults
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
