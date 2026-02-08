import nib


def main(app: nib.App):
    app.title = "Gauge"
    app.icon = nib.SFSymbol("gauge.medium")
    app.width = 300
    app.height = 350

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Linear", font=nib.Font.HEADLINE),
                nib.Gauge(
                    value=0.7,
                    label="Battery",
                    current_value_label="70%",
                    min_value_label="0%",
                    max_value_label="100%",
                    style=nib.GaugeStyle.LINEAR_CAPACITY,
                    tint=nib.Color.GREEN,
                ),
                nib.Divider(),
                nib.Text("Circular", font=nib.Font.HEADLINE),
                nib.HStack(
                    controls=[
                        nib.Gauge(
                            value=0.4,
                            label="CPU",
                            current_value_label="40%",
                            style=nib.GaugeStyle.ACCESSORY_CIRCULAR_CAPACITY,
                            tint=nib.Color.BLUE,
                        ),
                        nib.Gauge(
                            value=0.85,
                            label="RAM",
                            current_value_label="85%",
                            style=nib.GaugeStyle.ACCESSORY_CIRCULAR_CAPACITY,
                            tint=nib.Color.ORANGE,
                        ),
                    ],
                    spacing=20,
                ),
                nib.Divider(),
                nib.Text("Accessory Linear", font=nib.Font.HEADLINE),
                nib.Gauge(
                    value=0.55,
                    label="Storage",
                    style=nib.GaugeStyle.ACCESSORY_LINEAR_CAPACITY,
                    tint=nib.Color.PURPLE,
                ),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
