import nib


def main(app: nib.App):
    app.title = "Rich Text"
    app.icon = nib.SFSymbol("textformat")
    app.width = 350
    app.height = 400

    app.build(
        nib.VStack(
            controls=[
                nib.Text("AttributedString Demo", font=nib.Font.HEADLINE),
                nib.Divider(),
                # Example 1: Error message with styled prefix
                nib.Text(
                    strings=[
                        nib.AttributedString(
                            "Error: ",
                            style=nib.TextStyle(color="red", bold=True),
                        ),
                        nib.AttributedString(
                            "File not found",
                            style=nib.TextStyle.BODY,
                        ),
                    ],
                ),
                # Example 2: Colored text segments
                nib.Text(
                    strings=[
                        nib.AttributedString("Red ", color=nib.Color.RED),
                        nib.AttributedString("Green ", color=nib.Color.GREEN),
                        nib.AttributedString("Blue", color=nib.Color.BLUE),
                    ],
                ),
                # Example 3: Mixed fonts
                nib.Text(
                    strings=[
                        nib.AttributedString("Title ", font=nib.Font.TITLE),
                        nib.AttributedString("+ ", font=nib.Font.BODY),
                        nib.AttributedString("Caption", font=nib.Font.CAPTION),
                    ],
                ),
                # Example 4: Styled code snippet
                nib.Text(
                    strings=[
                        nib.AttributedString("def ", color="#FF79C6"),
                        nib.AttributedString("hello", color="#50FA7B"),
                        nib.AttributedString("():", color=nib.Color.WHITE),
                    ],
                    padding=8,
                    background=nib.Color(hex="#282A36"),
                ),
                # Example 5: Decorations
                nib.Text(
                    strings=[
                        nib.AttributedString(
                            "Bold ",
                            style=nib.TextStyle(bold=True),
                        ),
                        nib.AttributedString(
                            "Italic ",
                            style=nib.TextStyle(italic=True),
                        ),
                        nib.AttributedString(
                            "Underline",
                            style=nib.TextStyle(underline=True),
                        ),
                    ],
                ),
                # Example 6: With line limit
                nib.Text(
                    strings=[
                        nib.AttributedString(
                            "Important: ", style=nib.TextStyle(bold=True)
                        ),
                        nib.AttributedString(
                            "This is a very long message that will be truncated "
                            "if it exceeds the line limit we've set.",
                        ),
                    ],
                    line_limit=4,
                    truncation_mode=nib.TruncationMode.TAIL,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )


nib.run(main)
