"""Visual effect blur for frosted glass backgrounds.

Provides NSVisualEffectView-based blur effects for macOS.
"""

from enum import Enum
from typing import Optional
from ..base import View


class BlurStyle(Enum):
    """Visual effect blur material styles.

    These correspond to NSVisualEffectView.Material values.
    """
    # Standard materials
    HEADER_VIEW = "headerView"
    TOOLTIP = "tooltip"
    MENU = "menu"
    POPOVER = "popover"
    SIDEBAR = "sidebar"
    FULLSCREEN_UI = "fullScreenUI"
    HUD = "hud"
    SHEET = "sheet"
    WINDOW_BACKGROUND = "windowBackground"
    CONTENT_BACKGROUND = "contentBackground"
    UNDER_WINDOW_BACKGROUND = "underWindowBackground"
    UNDER_PAGE_BACKGROUND = "underPageBackground"

    # Vibrancy
    TITLEBAR = "titlebar"
    SELECTION = "selection"

    # System materials (newer)
    ULTRA_THIN = "ultraThin"
    THIN = "thin"
    REGULAR = "regular"
    THICK = "thick"
    ULTRA_THICK = "ultraThick"


class BlurBlendingMode(Enum):
    """Blur blending mode."""
    BEHIND_WINDOW = "behindWindow"
    WITHIN_WINDOW = "withinWindow"


class VisualEffectBlur(View):
    """A view that applies a blur effect, creating a frosted glass appearance.

    VisualEffectBlur wraps NSVisualEffectView to create the translucent
    blur effect commonly seen in macOS menu bar apps and system UI.

    Can be used as a background for other views or standalone.

    Args:
        material: The blur material/style (see BlurStyle).
        blending_mode: How the blur blends with content.
        is_emphasized: Whether to use emphasized appearance.
        corner_radius: Optional corner radius for rounded blur.
        **kwargs: Additional view modifiers.

    Example:
        As a view background::

            nib.VStack(
                controls=[...],
                background=nib.VisualEffectBlur(
                    material=nib.BlurStyle.POPOVER,
                ),
            )

        Menu bar style blur::

            nib.VisualEffectBlur(
                material=nib.BlurStyle.MENU,
                corner_radius=10,
            )

        Sidebar style::

            nib.VisualEffectBlur(
                material=nib.BlurStyle.SIDEBAR,
                blending_mode=nib.BlurBlendingMode.BEHIND_WINDOW,
            )
    """

    _type = "VisualEffectBlur"

    def __init__(
        self,
        material: BlurStyle = BlurStyle.POPOVER,
        blending_mode: BlurBlendingMode = BlurBlendingMode.BEHIND_WINDOW,
        is_emphasized: bool = False,
        corner_radius: Optional[float] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._material = material
        self._blending_mode = blending_mode
        self._is_emphasized = is_emphasized
        self._corner_radius = corner_radius

    @property
    def material(self) -> BlurStyle:
        """Blur material style."""
        return self._material

    @material.setter
    def material(self, val: BlurStyle) -> None:
        self._material = val
        self._mark_dirty()

    @property
    def blending_mode(self) -> BlurBlendingMode:
        """Blur blending mode."""
        return self._blending_mode

    @blending_mode.setter
    def blending_mode(self, val: BlurBlendingMode) -> None:
        self._blending_mode = val
        self._mark_dirty()

    @property
    def is_emphasized(self) -> bool:
        """Whether to use emphasized appearance."""
        return self._is_emphasized

    @is_emphasized.setter
    def is_emphasized(self, val: bool) -> None:
        self._is_emphasized = val
        self._mark_dirty()

    @property
    def corner_radius(self) -> Optional[float]:
        """Corner radius for rounded blur."""
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, val: Optional[float]) -> None:
        self._corner_radius = val
        self._mark_dirty()

    def _get_props(self) -> dict:
        props = {
            "material": self._material.value,
            "blendingMode": self._blending_mode.value,
        }
        if self._is_emphasized:
            props["isEmphasized"] = True
        if self._corner_radius is not None:
            props["cornerRadius"] = float(self._corner_radius)
        return props
