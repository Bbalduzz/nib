"""Type definitions and enums for Nib views and styling.

This module provides all the type definitions, enums, and helper classes
used throughout Nib for styling views, configuring controls, and defining
animations.

Type Classes:
    - :class:`Color` - Color values (named, hex, RGB, RGBA)
    - :class:`Font` - Font configuration (system and custom fonts)
    - :class:`TextStyle` - Semantic text styling
    - :class:`Animation` - Animation timing and spring configurations

Style Enums:
    - :class:`ButtonStyle`, :class:`ButtonRole` - Button appearance
    - :class:`ToggleStyle` - Toggle/switch appearance
    - :class:`TextFieldStyle` - Text input appearance
    - :class:`PickerStyle` - Selection picker appearance
    - :class:`ProgressStyle` - Progress indicator appearance

Layout Enums:
    - :class:`HorizontalAlignment`, :class:`VerticalAlignment` - Alignment
    - :class:`Alignment` - Combined 2D alignment for ZStack
    - :class:`ScrollAxis` - Scroll direction

Visual Enums:
    - :class:`FontWeight` - Text weight
    - :class:`TruncationMode`, :class:`TextCase` - Text formatting
    - :class:`ImageRenderingMode`, :class:`ContentMode` - Image display
    - :class:`SymbolScale`, :class:`SymbolRenderingMode` - SF Symbol config
    - :class:`BlendMode` - Layer blending

Animation Enums:
    - :class:`ContentTransition` - Content change animations
    - :class:`Transition` - View appearance/disappearance animations

Example:
    Using types in views::

        import nib

        # Colors
        text = nib.Text("Hello", foreground_color=nib.Color.BLUE)
        text = nib.Text("World", foreground_color=nib.Color(hex="#FF5733"))

        # Fonts
        title = nib.Text("Title", font=nib.Font.TITLE)
        custom = nib.Text("Custom", font=nib.Font.system(18, nib.FontWeight.BOLD))

        # Enums
        button = nib.Button("Click", style=nib.ButtonStyle.BORDERED_PROMINENT)
        toggle = nib.Toggle(is_on=True, style=nib.ToggleStyle.SWITCH)

        # Animations
        animated = nib.Text("Count", animation=nib.Animation.spring())

Note:
    Most enums provide both UPPERCASE (preferred) and lowercase (deprecated)
    names for backwards compatibility. New code should use UPPERCASE names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from .views.base import View


# ─────────────────────────────────────────────────────────────────────────────
# Utility Functions
# ─────────────────────────────────────────────────────────────────────────────


def resolve_enum(value) -> Optional[str]:
    """Convert an enum value or string to its string representation.

    This utility function normalizes enum values and strings for
    serialization to the Swift runtime.

    Args:
        value: An enum value, string, or None.

    Returns:
        The string value of the enum, the string itself, or None.

    Example:
        >>> resolve_enum(ButtonStyle.BORDERED)
        'bordered'
        >>> resolve_enum("bordered")
        'bordered'
        >>> resolve_enum(None)
        None
    """
    if value is None:
        return None
    # Check Enum BEFORE str because str-enums inherit from both
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, str):
        return value
    return str(value)


class FontWeight(str, Enum):
    """Font weight values matching SwiftUI Font.Weight.

    Use these values with :meth:`Font.system` or the ``font_weight`` modifier
    to control text thickness.

    Example:
        >>> nib.Text("Bold", font_weight=FontWeight.BOLD)
        >>> nib.Text("Light", font=nib.Font.system(16, FontWeight.LIGHT))
    """

    # CAPS names (preferred)
    ULTRA_LIGHT = "ultraLight"
    THIN = "thin"
    LIGHT = "light"
    REGULAR = "regular"
    MEDIUM = "medium"
    SEMIBOLD = "semibold"
    BOLD = "bold"
    HEAVY = "heavy"
    BLACK = "black"

    # Backwards-compatible aliases (deprecated)
    ultraLight = "ultraLight"
    thin = "thin"
    light = "light"
    regular = "regular"
    medium = "medium"
    semibold = "semibold"
    bold = "bold"
    heavy = "heavy"
    black = "black"


# ─────────────────────────────────────────────────────────────────────────────
# Button Enums
# ─────────────────────────────────────────────────────────────────────────────


class ButtonStyle(str, Enum):
    """Button visual styles matching SwiftUI ButtonStyle.

    Controls the visual appearance of buttons.

    Styles:
        - AUTOMATIC: System default style
        - BORDERED: Button with a visible border
        - BORDERED_PROMINENT: Bordered with accent color fill
        - BORDERLESS: No visible border
        - PLAIN: Minimal styling
        - LINK: Appears as a clickable link

    Example:
        >>> nib.Button("Primary", style=ButtonStyle.BORDERED_PROMINENT)
        >>> nib.Button("Secondary", style=ButtonStyle.BORDERED)
        >>> nib.Button("Link", style=ButtonStyle.LINK)
    """

    # CAPS names (preferred)
    AUTOMATIC = "automatic"
    BORDERED = "bordered"
    BORDERED_PROMINENT = "borderedProminent"
    BORDERLESS = "borderless"
    PLAIN = "plain"
    LINK = "link"

    # Backwards-compatible aliases (deprecated)
    automatic = "automatic"
    bordered = "bordered"
    borderedProminent = "borderedProminent"
    borderless = "borderless"
    plain = "plain"
    link = "link"


class ButtonRole(str, Enum):
    """Button semantic roles matching SwiftUI ButtonRole."""

    # CAPS names (preferred)
    DESTRUCTIVE = "destructive"
    CANCEL = "cancel"

    # Backwards-compatible aliases (deprecated)
    destructive = "destructive"
    cancel = "cancel"


class BorderShape(str, Enum):
    """Border shape options for buttons and other controls."""

    # CAPS names (preferred)
    AUTOMATIC = "automatic"
    CAPSULE = "capsule"
    ROUNDED_RECTANGLE = "roundedRectangle"
    CIRCLE = "circle"

    # Backwards-compatible aliases (deprecated)
    automatic = "automatic"
    capsule = "capsule"
    roundedRectangle = "roundedRectangle"
    circle = "circle"


class ControlSize(str, Enum):
    """Control size options matching SwiftUI ControlSize."""

    # CAPS names (preferred)
    MINI = "mini"
    SMALL = "small"
    REGULAR = "regular"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"

    # Backwards-compatible aliases (deprecated)
    mini = "mini"
    small = "small"
    regular = "regular"
    large = "large"
    extraLarge = "extraLarge"


class LabelStyle(str, Enum):
    """Label display style options."""

    # CAPS names (preferred)
    AUTOMATIC = "automatic"
    ICON_ONLY = "iconOnly"
    TITLE_ONLY = "titleOnly"
    TITLE_AND_ICON = "titleAndIcon"

    # Backwards-compatible aliases (deprecated)
    automatic = "automatic"
    iconOnly = "iconOnly"
    titleOnly = "titleOnly"
    titleAndIcon = "titleAndIcon"


# ─────────────────────────────────────────────────────────────────────────────
# Toggle Enums
# ─────────────────────────────────────────────────────────────────────────────


class ToggleStyle(str, Enum):
    """Toggle visual styles matching SwiftUI ToggleStyle."""

    # CAPS names (preferred)
    AUTOMATIC = "automatic"
    SWITCH = "switch"
    BUTTON = "button"
    CHECKBOX = "checkbox"

    # Backwards-compatible aliases (deprecated)
    automatic = "automatic"
    switch = "switch"
    button = "button"
    checkbox = "checkbox"


# ─────────────────────────────────────────────────────────────────────────────
# TextField Enums
# ─────────────────────────────────────────────────────────────────────────────


class TextFieldStyle(str, Enum):
    """TextField visual styles matching SwiftUI TextFieldStyle."""

    # CAPS names (preferred)
    AUTOMATIC = "automatic"
    PLAIN = "plain"
    ROUNDED_BORDER = "roundedBorder"
    SQUARE_BORDER = "squareBorder"

    # Backwards-compatible aliases (deprecated)
    automatic = "automatic"
    plain = "plain"
    roundedBorder = "roundedBorder"
    squareBorder = "squareBorder"


# ─────────────────────────────────────────────────────────────────────────────
# Picker Enums
# ─────────────────────────────────────────────────────────────────────────────


class PickerStyle(str, Enum):
    """Picker visual styles matching SwiftUI PickerStyle."""

    # CAPS names (preferred)
    AUTOMATIC = "automatic"
    MENU = "menu"
    SEGMENTED = "segmented"
    WHEEL = "wheel"
    INLINE = "inline"

    # Backwards-compatible aliases (deprecated)
    automatic = "automatic"
    menu = "menu"
    segmented = "segmented"
    wheel = "wheel"
    inline = "inline"


# ─────────────────────────────────────────────────────────────────────────────
# ProgressView Enums
# ─────────────────────────────────────────────────────────────────────────────


class ProgressStyle(str, Enum):
    """ProgressView visual styles."""

    # CAPS names (preferred)
    AUTOMATIC = "automatic"
    LINEAR = "linear"
    CIRCULAR = "circular"

    # Backwards-compatible aliases (deprecated)
    automatic = "automatic"
    linear = "linear"
    circular = "circular"


# ─────────────────────────────────────────────────────────────────────────────
# Text Enums
# ─────────────────────────────────────────────────────────────────────────────


class TruncationMode(str, Enum):
    """Text truncation mode options."""

    # CAPS names (preferred)
    HEAD = "head"
    MIDDLE = "middle"
    TAIL = "tail"

    # Backwards-compatible aliases (deprecated)
    head = "head"
    middle = "middle"
    tail = "tail"


class TextCase(str, Enum):
    """Text case transformation options."""

    # CAPS names (preferred)
    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"

    # Backwards-compatible aliases (deprecated)
    uppercase = "uppercase"
    lowercase = "lowercase"


# ─────────────────────────────────────────────────────────────────────────────
# Image Enums
# ─────────────────────────────────────────────────────────────────────────────


class ImageRenderingMode(str, Enum):
    """Image rendering mode options."""

    # CAPS names (preferred)
    ORIGINAL = "original"
    TEMPLATE = "template"

    # Backwards-compatible aliases (deprecated)
    original = "original"
    template = "template"


class SymbolScale(str, Enum):
    """SF Symbol scale options."""

    # CAPS names (preferred)
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    # Backwards-compatible aliases (deprecated)
    small = "small"
    medium = "medium"
    large = "large"


class SymbolRenderingMode(str, Enum):
    """SF Symbol rendering mode options."""

    # CAPS names (preferred)
    MONOCHROME = "monochrome"
    HIERARCHICAL = "hierarchical"
    PALETTE = "palette"
    MULTICOLOR = "multicolor"

    # Backwards-compatible aliases (deprecated)
    monochrome = "monochrome"
    hierarchical = "hierarchical"
    palette = "palette"
    multicolor = "multicolor"


class ContentMode(str, Enum):
    """Image content mode options for aspect ratio handling."""

    FIT = "fit"  # Scale to fit within bounds, maintaining aspect ratio
    FILL = "fill"  # Scale to fill bounds, maintaining aspect ratio (may clip)


# ─────────────────────────────────────────────────────────────────────────────
# Alignment Enums
# ─────────────────────────────────────────────────────────────────────────────


class HorizontalAlignment(str, Enum):
    """Horizontal alignment options."""

    # CAPS names (preferred)
    LEADING = "leading"
    CENTER = "center"
    TRAILING = "trailing"

    # Backwards-compatible aliases (deprecated)
    leading = "leading"
    center = "center"
    trailing = "trailing"


class VerticalAlignment(str, Enum):
    """Vertical alignment options."""

    # CAPS names (preferred)
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"

    # Backwards-compatible aliases (deprecated)
    top = "top"
    center = "center"
    bottom = "bottom"


class Alignment(str, Enum):
    """Combined alignment options for ZStack."""

    # CAPS names (preferred)
    TOP_LEADING = "topLeading"
    TOP = "top"
    TOP_TRAILING = "topTrailing"
    LEADING = "leading"
    CENTER = "center"
    TRAILING = "trailing"
    BOTTOM_LEADING = "bottomLeading"
    BOTTOM = "bottom"
    BOTTOM_TRAILING = "bottomTrailing"

    # Backwards-compatible aliases (deprecated)
    topLeading = "topLeading"
    top = "top"
    topTrailing = "topTrailing"
    leading = "leading"
    center = "center"
    trailing = "trailing"
    bottomLeading = "bottomLeading"
    bottom = "bottom"
    bottomTrailing = "bottomTrailing"


# ─────────────────────────────────────────────────────────────────────────────
# ScrollView Enums
# ─────────────────────────────────────────────────────────────────────────────


class ScrollAxis(str, Enum):
    """ScrollView axis options."""

    # CAPS names (preferred)
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    BOTH = "both"

    # Backwards-compatible aliases (deprecated)
    horizontal = "horizontal"
    vertical = "vertical"
    both = "both"


# ─────────────────────────────────────────────────────────────────────────────
# Transition Enums
# ─────────────────────────────────────────────────────────────────────────────


class ContentTransition(str, Enum):
    """
    Content transition types for animating content changes.

    Used with Text to animate how content changes are displayed.

    Example:
        Text(f"{count}", content_transition=ContentTransition.NUMERIC_TEXT)
        Text(f"{count}", content_transition=ContentTransition.NUMERIC_TEXT_DOWN)
    """

    # CAPS names (preferred)
    IDENTITY = "identity"
    INTERPOLATE = "interpolate"
    NUMERIC_TEXT = "numericText"
    NUMERIC_TEXT_DOWN = "numericTextDown"
    OPACITY = "opacity"

    # Backwards-compatible aliases (deprecated)
    identity = "identity"
    interpolate = "interpolate"
    numericText = "numericText"
    numericTextDown = "numericTextDown"
    opacity = "opacity"


class Transition(str, Enum):
    """
    View transition types for appearance/disappearance animations.

    Used to animate how views enter and exit the view hierarchy.

    Example:
        Text("Hello", transition=Transition.OPACITY)
        VStack([...], transition=Transition.SLIDE)
    """

    # CAPS names (preferred)
    IDENTITY = "identity"
    OPACITY = "opacity"
    SCALE = "scale"
    SLIDE = "slide"
    MOVE_LEADING = "moveLeading"
    MOVE_TRAILING = "moveTrailing"
    MOVE_TOP = "moveTop"
    MOVE_BOTTOM = "moveBottom"
    PUSH = "push"

    # Backwards-compatible aliases (deprecated)
    identity = "identity"
    opacity = "opacity"
    scale = "scale"
    slide = "slide"
    moveLeading = "moveLeading"
    moveTrailing = "moveTrailing"
    moveTop = "moveTop"
    moveBottom = "moveBottom"
    push = "push"


class BlendMode(str, Enum):
    """Blend mode options for combining views."""

    # CAPS names (preferred)
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    DARKEN = "darken"
    LIGHTEN = "lighten"
    COLOR_DODGE = "colorDodge"
    COLOR_BURN = "colorBurn"
    SOFT_LIGHT = "softLight"
    HARD_LIGHT = "hardLight"
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"
    HUE = "hue"
    SATURATION = "saturation"
    COLOR = "color"
    LUMINOSITY = "luminosity"

    # Backwards-compatible aliases (deprecated)
    normal = "normal"
    multiply = "multiply"
    screen = "screen"
    overlay = "overlay"
    darken = "darken"
    lighten = "lighten"
    colorDodge = "colorDodge"
    colorBurn = "colorBurn"
    softLight = "softLight"
    hardLight = "hardLight"
    difference = "difference"
    exclusion = "exclusion"
    hue = "hue"
    saturation = "saturation"
    color = "color"
    luminosity = "luminosity"


@dataclass
class Color:
    """
    Color type supporting named colors and hex values.

    Two primary ways to define colors:
    1. Hexadecimal values:
       - Color(hex="#4287f5") or Color(hex="4287f5")
       - Supports alpha channel: Color(hex="#7fff6666") - ARGB format

    2. Named colors:
       - Color.RED, Color.BLUE, Color.PRIMARY, Color.INDIGO, etc.

    Both support the with_opacity method:
       - Color(hex="#4287f5").with_opacity(0.8)
       - Color.INDIGO.with_opacity(0.5)
    """

    value: str
    opacity: Optional[float] = None

    # Predefined colors (will be set below)
    # Basic colors
    RED = None
    BLUE = None
    GREEN = None
    YELLOW = None
    ORANGE = None
    PURPLE = None
    PINK = None
    WHITE = None
    BLACK = None
    GRAY = None
    CLEAR = None

    # Extended colors
    INDIGO = None
    CYAN = None
    MINT = None
    TEAL = None
    BROWN = None

    # Semantic colors
    PRIMARY = None
    SECONDARY = None
    ACCENT = None

    # Legacy lowercase aliases (deprecated, for backwards compatibility)
    red = None
    blue = None
    green = None
    yellow = None
    orange = None
    purple = None
    pink = None
    white = None
    black = None
    gray = None
    clear = None
    primary = None
    secondary = None
    accent = None

    def __init__(
        self,
        value: Optional[str] = None,
        *,
        hex: Optional[str] = None,
        opacity: Optional[float] = None,
    ):
        """
        Create a Color.

        Args:
            value: Named color string (e.g., "red", "blue") - used internally
            hex: Hex color string (e.g., "#4287f5" or "4287f5")
            opacity: Optional opacity value (0.0 to 1.0)

        Examples:
            Color(hex="#4287f5")
            Color(hex="4287f5")
            Color(hex="#7fff6666")  # With alpha in hex
        """
        if hex is not None:
            if not hex.startswith("#"):
                hex = f"#{hex}"
            self.value = hex
        elif value is not None:
            self.value = value
        else:
            raise ValueError("Either 'value' or 'hex' must be provided")
        self.opacity = opacity

    def with_opacity(self, opacity: float) -> "Color":
        """
        Return a new Color with the specified opacity.

        Args:
            opacity: Opacity value from 0.0 (fully transparent) to 1.0 (fully opaque)

        Returns:
            A new Color instance with the specified opacity

        Examples:
            Color(hex="#4287f5").with_opacity(0.8)
            Color.INDIGO.with_opacity(0.5)
        """
        return Color(value=self.value, opacity=opacity)

    @classmethod
    def hex(cls, hex_value: str) -> "Color":
        """
        Create a color from a hex string.

        Deprecated: Use Color(hex="...") instead.
        """
        if not hex_value.startswith("#"):
            hex_value = f"#{hex_value}"
        return cls(value=hex_value)

    @classmethod
    def rgb(cls, r: int, g: int, b: int) -> "Color":
        """Create a color from RGB values (0-255)."""
        return cls(value=f"#{r:02x}{g:02x}{b:02x}")

    @classmethod
    def rgba(cls, r: int, g: int, b: int, a: float) -> "Color":
        """Create a color from RGBA values (RGB: 0-255, A: 0.0-1.0)."""
        alpha = int(a * 255)
        return cls(value=f"#{alpha:02x}{r:02x}{g:02x}{b:02x}")

    def to_dict(self) -> str:
        """Serialize the color for transmission to Swift."""
        if self.opacity is not None:
            return f"{self.value}:{self.opacity}"
        return self.value


# Set up predefined colors (UPPERCASE - preferred)
Color.RED = Color(value="red")
Color.BLUE = Color(value="blue")
Color.GREEN = Color(value="green")
Color.YELLOW = Color(value="yellow")
Color.ORANGE = Color(value="orange")
Color.PURPLE = Color(value="purple")
Color.PINK = Color(value="pink")
Color.WHITE = Color(value="white")
Color.BLACK = Color(value="black")
Color.GRAY = Color(value="gray")
Color.CLEAR = Color(value="clear")

# Extended colors
Color.INDIGO = Color(value="indigo")
Color.CYAN = Color(value="cyan")
Color.MINT = Color(value="mint")
Color.TEAL = Color(value="teal")
Color.BROWN = Color(value="brown")

# Semantic colors
Color.PRIMARY = Color(value="primary")
Color.SECONDARY = Color(value="secondary")
Color.ACCENT = Color(value="accentColor")

# Legacy lowercase aliases (for backwards compatibility)
Color.red = Color(value="red")
Color.blue = Color(value="blue")
Color.green = Color(value="green")
Color.yellow = Color(value="yellow")
Color.orange = Color(value="orange")
Color.purple = Color(value="purple")
Color.pink = Color(value="pink")
Color.white = Color(value="white")
Color.black = Color(value="black")
Color.gray = Color(value="gray")
Color.clear = Color(value="clear")
Color.primary = Color(value="primary")
Color.secondary = Color(value="secondary")
Color.accent = Color(value="accentColor")


# Type for font weight - can be FontWeight enum or string
FontWeightLike = Union[FontWeight, str]


def _resolve_weight(weight: Optional[FontWeightLike]) -> Optional[str]:
    """Convert font weight to string representation.

    Args:
        weight: A FontWeight enum value or string, or None.

    Returns:
        The string value of the weight, or None.

    Example:
        >>> _resolve_weight(FontWeight.BOLD)
        'bold'
        >>> _resolve_weight("medium")
        'medium'
    """
    if weight is None:
        return None
    if isinstance(weight, FontWeight):
        return weight.value
    return weight


@dataclass
class Font:
    """Font type supporting system fonts, custom sizes, and custom font files."""

    name: Optional[str] = None
    size: Optional[float] = None
    weight: Optional[str] = None
    path: Optional[str] = None  # Path to font file for runtime loading

    # System fonts (CAPS - preferred)
    LARGE_TITLE = None
    TITLE = None
    TITLE2 = None
    TITLE3 = None
    HEADLINE = None
    SUBHEADLINE = None
    BODY = None
    CALLOUT = None
    CAPTION = None
    CAPTION2 = None
    FOOTNOTE = None

    # Backwards-compatible aliases (deprecated)
    largeTitle = None
    title = None
    title2 = None
    title3 = None
    headline = None
    subheadline = None
    body = None
    callout = None
    caption = None
    caption2 = None
    footnote = None

    @classmethod
    def system(cls, size: float, weight: Optional[FontWeightLike] = None) -> "Font":
        """
        Create a system font with custom size and optional weight.

        Args:
            size: Font size in points
            weight: FontWeight enum or string (e.g., FontWeight.medium, "bold")

        Example:
            Font.system(14, FontWeight.medium)
            Font.system(16, FontWeight.bold)
        """
        return cls(size=size, weight=_resolve_weight(weight))

    @classmethod
    def custom(
        cls,
        name: str,
        size: float,
        weight: Optional[FontWeightLike] = None,
        path: Optional[str] = None,
    ) -> "Font":
        """
        Create a custom font.

        Args:
            name: Font family name (e.g., "Inter", "Roboto")
            size: Font size in points
            weight: FontWeight enum or string
            path: Optional path to .ttf/.otf file for runtime loading
        """
        return cls(name=name, size=size, weight=_resolve_weight(weight), path=path)

    def to_dict(self) -> dict:
        return {
            "fontName": self.name,
            "fontSize": float(self.size) if self.size is not None else None,
            "fontWeight": self.weight,
            "fontPath": self.path,
        }


# Set up system fonts (CAPS - preferred)
Font.LARGE_TITLE = Font(name="largeTitle")
Font.TITLE = Font(name="title")
Font.TITLE2 = Font(name="title2")
Font.TITLE3 = Font(name="title3")
Font.HEADLINE = Font(name="headline")
Font.SUBHEADLINE = Font(name="subheadline")
Font.BODY = Font(name="body")
Font.CALLOUT = Font(name="callout")
Font.CAPTION = Font(name="caption")
Font.CAPTION2 = Font(name="caption2")
Font.FOOTNOTE = Font(name="footnote")

# Backwards-compatible aliases (deprecated)
Font.largeTitle = Font.LARGE_TITLE
Font.title = Font.TITLE
Font.title2 = Font.TITLE2
Font.title3 = Font.TITLE3
Font.headline = Font.HEADLINE
Font.subheadline = Font.SUBHEADLINE
Font.body = Font.BODY
Font.callout = Font.CALLOUT
Font.caption = Font.CAPTION
Font.caption2 = Font.CAPTION2
Font.footnote = Font.FOOTNOTE


# Type alias for colors that can be string or Color
ColorLike = Union[str, Color]


def resolve_color(color: ColorLike) -> str:
    """Convert a color-like value to its string representation.

    Normalizes Color objects and string values for serialization
    to the Swift runtime.

    Args:
        color: A Color instance or color string (name or hex).

    Returns:
        The serialized color string. For Color objects with opacity,
        returns "color:opacity" format.

    Example:
        >>> resolve_color(Color.BLUE)
        'blue'
        >>> resolve_color("#FF5733")
        '#FF5733'
        >>> resolve_color(Color.RED.with_opacity(0.5))
        'red:0.5'
    """
    if isinstance(color, Color):
        return color.to_dict()
    return color


@dataclass
class TextStyle:
    """Text style configuration combining font, decorations, and spacing.

    TextStyle groups all text-related styling options into a single object.
    Use predefined presets like `TextStyle.title` or create custom styles.

    Example:
        Using a preset::

            nib.Text("Hello", style=nib.TextStyle.title)

        Custom style::

            nib.Text(
                "Custom",
                style=nib.TextStyle(
                    font=nib.Font.system(18),
                    bold=True,
                    underline=True,
                ),
            )
    """

    # Font settings
    font: Optional[Font] = None
    color: Optional[str] = None
    weight: Optional[str] = None

    # Text decorations
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    strikethrough_color: Optional[str] = None
    underline: bool = False
    underline_color: Optional[str] = None

    # Font variations
    monospaced: bool = False
    monospaced_digit: bool = False

    # Spacing
    kerning: Optional[float] = None
    tracking: Optional[float] = None
    baseline_offset: Optional[float] = None

    # Predefined styles (set after class definition)
    LARGE_TITLE = None
    TITLE = None
    TITLE2 = None
    TITLE3 = None
    HEADLINE = None
    SUBHEADLINE = None
    BODY = None
    CALLOUT = None
    CAPTION = None
    CAPTION2 = None
    FOOTNOTE = None

    # Backwards-compatible aliases (deprecated)
    largeTitle = None
    title = None
    title2 = None
    title3 = None
    heading = None
    subheading = None
    body = None
    callout = None
    caption = None
    caption2 = None
    footnote = None

    def to_dict(self) -> dict:
        """Serialize the text style for transmission to Swift."""
        result = {}

        if self.font:
            result["font"] = self.font.to_dict()
        if self.color:
            result["color"] = self.color
        if self.weight:
            result["weight"] = self.weight
        if self.bold:
            result["bold"] = True
        if self.italic:
            result["italic"] = True
        if self.strikethrough:
            result["strikethrough"] = True
            if self.strikethrough_color:
                result["strikethroughColor"] = self.strikethrough_color
        if self.underline:
            result["underline"] = True
            if self.underline_color:
                result["underlineColor"] = self.underline_color
        if self.monospaced:
            result["monospaced"] = True
        if self.monospaced_digit:
            result["monospacedDigit"] = True
        if self.kerning is not None:
            result["kerning"] = float(self.kerning)
        if self.tracking is not None:
            result["tracking"] = float(self.tracking)
        if self.baseline_offset is not None:
            result["baselineOffset"] = float(self.baseline_offset)

        return result


# Set up predefined text styles (CAPS - preferred)
TextStyle.LARGE_TITLE = TextStyle(font=Font.LARGE_TITLE)
TextStyle.TITLE = TextStyle(font=Font.TITLE)
TextStyle.TITLE2 = TextStyle(font=Font.TITLE2)
TextStyle.TITLE3 = TextStyle(font=Font.TITLE3)
TextStyle.HEADLINE = TextStyle(font=Font.HEADLINE)
TextStyle.SUBHEADLINE = TextStyle(font=Font.SUBHEADLINE)
TextStyle.BODY = TextStyle(font=Font.BODY)
TextStyle.CALLOUT = TextStyle(font=Font.CALLOUT)
TextStyle.CAPTION = TextStyle(font=Font.CAPTION)
TextStyle.CAPTION2 = TextStyle(font=Font.CAPTION2)
TextStyle.FOOTNOTE = TextStyle(font=Font.FOOTNOTE)


@dataclass
class Animation:
    """Animation configuration for view transitions."""

    type: str  # "linear", "easeIn", "easeOut", "easeInOut", "spring"
    duration: Optional[float] = None
    delay: Optional[float] = None
    # Spring-specific parameters
    response: Optional[float] = None
    damping: Optional[float] = None

    # Presets (set after class definition)
    default = None
    fast = None
    slow = None
    bouncy = None

    @classmethod
    def linear(cls, duration: float = 0.3) -> "Animation":
        """Create a linear animation."""
        return cls(type="linear", duration=duration)

    @classmethod
    def easeIn(cls, duration: float = 0.3) -> "Animation":
        """Create an ease-in animation (slow start, fast end)."""
        return cls(type="easeIn", duration=duration)

    @classmethod
    def easeOut(cls, duration: float = 0.3) -> "Animation":
        """Create an ease-out animation (fast start, slow end)."""
        return cls(type="easeOut", duration=duration)

    @classmethod
    def easeInOut(cls, duration: float = 0.3) -> "Animation":
        """Create an ease-in-out animation (slow start and end)."""
        return cls(type="easeInOut", duration=duration)

    @classmethod
    def spring(cls, response: float = 0.3, damping: float = 0.7) -> "Animation":
        """
        Create a spring animation.

        Args:
            response: How quickly the spring settles (lower = faster)
            damping: How much the spring bounces (0 = forever, 1 = no bounce)
        """
        return cls(type="spring", response=response, damping=damping)

    def to_dict(self) -> dict:
        return {
            "animationType": self.type,
            "animationDuration": self.duration,
            "animationDelay": self.delay,
            "springResponse": self.response,
            "springDamping": self.damping,
        }


# Set up animation presets
Animation.default = Animation.easeInOut(0.3)
Animation.fast = Animation.easeOut(0.15)
Animation.slow = Animation.easeInOut(0.5)
Animation.bouncy = Animation.spring(response=0.3, damping=0.5)
