import nib


def main(app: nib.App):
    welcome_tip = nib.Tip(
        id="welcome-tip",
        title="Welcome!",
        message="Click here to get started.",
        image="star.fill",
        actions=[
            nib.TipAction(
                id="learn", label="Learn More", action=lambda: print("Learn more")
            ),
        ],
        rules=[
            nib.ParameterRule(param_id="show_tips", operator="==", value=True),
        ],
    )

    app.tips.set_parameter("show_tips", True)

    app.build(nib.Button("Start", action=lambda: print("Started"), tip=welcome_tip))


nib.run(main)
