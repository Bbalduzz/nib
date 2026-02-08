import nib


def main(app: nib.App):
    app.title = "WebView"
    app.icon = nib.SFSymbol("globe")
    app.width = 400
    app.height = 450

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Web Content", font=nib.Font.HEADLINE),
                nib.WebView(
                    html="""
                    <html>
                    <body style="font-family: -apple-system; padding: 20px; background: #1a1a1a; color: white;">
                        <h2>Hello from HTML</h2>
                        <p>This is rendered inside a <strong>WebView</strong>.</p>
                        <ul>
                            <li>Supports HTML</li>
                            <li>Supports CSS</li>
                            <li>Supports JavaScript</li>
                        </ul>
                    </body>
                    </html>
                    """,
                    height=300,
                ),
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
