"""WebView Demo - Display web content in a menu bar app."""

import nib


def main(app: nib.App):
    app.title = "Web"
    app.icon = nib.SFSymbol("globe")
    app.width = 500
    app.height = 400

    # WebView loading a URL
    web = nib.WebView(
        url="https://example.com",
        width=480,
        height=360,
    )

    # Navigation buttons
    def go_back():
        web.go_back()

    def go_forward():
        web.go_forward()

    def reload():
        web.reload()

    def load_github():
        web.load_url("https://github.com")

    def load_html():
        web.load_html("""
        <html>
            <body style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                         color: white; font-family: -apple-system, system-ui;
                         display: flex; align-items: center; justify-content: center;
                         height: 100vh; margin: 0;">
                <div style="text-align: center;">
                    <h1>Hello from Nib!</h1>
                    <p>This is custom HTML content</p>
                </div>
            </body>
        </html>
        """)

    app.build(
        nib.VStack(
            controls=[
                # Toolbar
                nib.HStack(
                    controls=[
                        nib.Button("←", action=go_back),
                        nib.Button("→", action=go_forward),
                        nib.Button("↻", action=reload),
                        nib.Spacer(),
                        nib.Button("GitHub", action=load_github),
                        nib.Button("HTML", action=load_html),
                    ],
                    spacing=4,
                ),
                # WebView
                web,
            ],
            spacing=8,
            padding=10,
        )
    )


nib.run(main)
