# Video

![Video control](../../../assets/img/controls/video.png)

A view that displays and plays video content from URLs or local files. Video supports autoplay, looping, audio muting, playback controls, and various scaling modes. All playback properties are reactive.

## Constructor

```python
nib.Video(
    src=None,
    autoplay=False,
    loop=False,
    muted=False,
    controls=True,
    gravity=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `src` | `str` | `None` | Video source. Supports remote URLs (`"https://..."`), absolute file paths (`"/path/to/video.mp4"`), or asset references (`"intro.mp4"` resolves to `assets/intro.mp4`). |
| `autoplay` | `bool` | `False` | Whether to start playing automatically when the video loads. |
| `loop` | `bool` | `False` | Whether to restart playback automatically when the video ends. |
| `muted` | `bool` | `False` | Whether to mute the audio track. |
| `controls` | `bool` | `True` | Whether to show playback controls (play/pause, scrubber, volume). |
| `gravity` | `VideoGravity \| str` | `None` | How the video scales within its frame. Options: `VideoGravity.RESIZE_ASPECT` (fit, may letterbox -- default), `VideoGravity.RESIZE_ASPECT_FILL` (fill, may crop), `VideoGravity.RESIZE` (stretch to fill, distorts). |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `corner_radius`, `opacity`, `padding`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `src` | `str` | Get or set the video source. Setting triggers a UI update and may reset playback position. |
| `autoplay` | `bool` | Get or set autoplay. |
| `loop` | `bool` | Get or set looping. |
| `muted` | `bool` | Get or set muted state. |
| `controls` | `bool` | Get or set controls visibility. |

## Examples

### Basic video player

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Video(
            src="https://example.com/tutorial.mp4",
            width=480,
            height=270,
            corner_radius=8,
            padding=16,
        )
    )

nib.run(main)
```

### Autoplay looping background

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(controls=[
            nib.Video(
                src="ambient.mp4",
                autoplay=True,
                loop=True,
                muted=True,
                controls=False,
                gravity=nib.VideoGravity.RESIZE_ASPECT_FILL,
                width=400,
                height=300,
            ),
            nib.Text(
                "Welcome",
                font=nib.Font.LARGE_TITLE,
                foreground_color=nib.Color.WHITE,
            ),
        ])
    )

nib.run(main)
```

### Video with reactive source

```python
import nib

def main(app: nib.App):
    player = nib.Video(
        src="https://example.com/video1.mp4",
        autoplay=True,
        width=400,
        height=225,
        corner_radius=8,
    )

    app.build(
        nib.VStack(controls=[
            player,
            nib.HStack(controls=[
                nib.Button("Video 1", action=lambda: setattr(
                    player, "src", "https://example.com/video1.mp4")),
                nib.Button("Video 2", action=lambda: setattr(
                    player, "src", "https://example.com/video2.mp4")),
            ], spacing=8),
        ], spacing=12, padding=16)
    )

nib.run(main)
```
