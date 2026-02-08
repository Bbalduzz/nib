# Types Reference

Nib provides a set of types, dataclasses, and enums used to configure views, styling, animations, and layout. All types are importable directly from the `nib` module.

```python
import nib

color = nib.Color(hex="#4287f5")
font = nib.Font.system(16, nib.FontWeight.BOLD)
animation = nib.Animation.spring()
```

## Type Classes

| Type | Description |
|------|-------------|
| [Color](color.md) | Color values -- named, hex, RGB, RGBA |
| [Font](font.md) | Font configuration -- system fonts and custom font files |
| [Animation](animation.md) | Animation timing curves and spring configurations |
| [Transition](transition.md) | View appearance/disappearance animations and content transitions |
| [TextStyle & AttributedString](text-style.md) | Rich text styling and multi-segment attributed strings |
| [Offset & CornerRadius](geometry.md) | Position offsets and per-corner radius configuration |

## Enum References

| Page | Enums |
|------|-------|
| [Style Enums](style-enums.md) | ButtonStyle, ButtonRole, BorderShape, ControlSize, LabelStyle, ToggleStyle, TextFieldStyle, EditorStyle, PickerStyle, ProgressStyle, FormStyle |
| [Alignment Enums](alignment-enums.md) | HorizontalAlignment, VerticalAlignment, Alignment, ScrollAxis |
| [Image Enums](image-enums.md) | ImageRenderingMode, SymbolScale, SymbolRenderingMode, ContentMode, TruncationMode, TextCase |
| [BlendMode](blend-mode.md) | All layer blending modes |
