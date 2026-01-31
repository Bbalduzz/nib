"""
Wheredoiwatchit - A nib application
"""

import webbrowser

import nib
from services.justwatch import search


def main(app: nib.App):
    app.icon = nib.SFSymbol(
        "sparkles.tv.fill", rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL
    )
    app.width = 280
    app.height = 350
    app.menu = [
        nib.MenuItem("Quit", shortcut="cmd+q", action=app.quit),
    ]

    """
    defaults = nib.UserDefaults()
    defaults.set(
        "paid_services",
        {
            "netflix": "https://images.justwatch.com/icon/207360008/s100/netflix.avif",
            "disney plus": "https://images.justwatch.com/icon/313118777/s100/disneyplus.avif",
            "prime video": "https://images.justwatch.com/icon/322992749/s100/amazonprimevideo.avif",
            "now": "https://images.justwatch.com/icon/243753092/s100/nowtv.avif",
        },
    )
    print(defaults.get("paid_services"))
    """

    paid_services = {
        "netflix": "https://images.justwatch.com/icon/207360008/s100/netflix.avif",
        "disneyplus": "https://images.justwatch.com/icon/313118777/s100/disneyplus.avif",  # no space
        "amazonprimevideo": "https://images.justwatch.com/icon/322992749/s100/amazonprimevideo.avif",
        "nowtv": "https://images.justwatch.com/icon/243753092/s100/nowtv.avif",
    }
    services_row = nib.HStack(
        controls=[
            nib.Image(src=service, width=15, height=15, corner_radius=5)
            for service in paid_services.values()
        ],
        spacing=-5,  # Negative spacing creates overlap
        # Gentle animation for the header icons
        animation=nib.Animation.easeOut(0.2),
    )

    # Custom slide-up transition for search results
    slide_up_transition = (
        nib.Transition.custom("slideUp")
        .at(0.0, opacity=0, scale=0.95, offset_y=10)
        .at(1.0, opacity=1, scale=1.0, offset_y=0)
        .build()
    )

    result_media = nib.VStack(
        controls=[],
        visible=False,
        background=nib.RoundedRectangle(
            fill=nib.Color.SECONDARY.with_opacity(0.1),
            stroke_color=nib.Color.GRAY.with_opacity(0.3),
            stroke_width=1,
            corner_radius=8,
        ),
        spacing=12,
        padding=8,
        alignment=nib.HorizontalAlignment.LEADING,
        width=225,
        # Animate when results appear
        transition=slide_up_transition,
        animation=nib.Animation.spring(response=0.4, damping=0.8),
    )

    def on_search(e):
        result = search(e, country="IT", language="it", count=1)[0]
        print(result.offers)
        # todo:
        # 1. build a view for the result:
        # Hstack -> image + hstack [-> (title + release_year)  + short_description] + duration
        image = nib.Image(
            src=result.poster,
            width=50,
            height=75,
            corner_radius=8,
            animation=nib.Animation.easeOut(0.3),
        )
        title = nib.Text(
            result.title,
            style=nib.TextStyle(
                font=nib.Font.custom("SF Pro Rounded", 15, weight=nib.FontWeight.BOLD)
            ),
            # Smooth content transition when title changes
            content_transition=nib.ContentTransition.INTERPOLATE,
        )
        release_year = nib.Text(
            str(result.release_year),
            style=nib.TextStyle(
                font=nib.Font.custom("SF Pro Rounded", 10),
                color=nib.Color.SECONDARY,
            ),
        )
        short_description = nib.Text(
            result.short_description,
            line_limit=4,
            style=nib.TextStyle(font=nib.Font.custom("SF Pro Rounded", 9)),
        )
        duration = nib.Text(
            str(result.runtime_minutes),
            style=nib.TextStyle(
                font=nib.Font.custom("SF Pro Rounded", 10),
                color=nib.Color.SECONDARY,
            ),
        )

        my_offers = [
            offer
            for offer in result.offers
            if offer.package.technical_name in paid_services
            or offer.package.name.lower() in paid_services
        ]
        seen = set()
        unique_offers = []
        for offer in my_offers:
            if offer.package.name not in seen:
                seen.add(offer.package.name)
                unique_offers.append(offer)

        if unique_offers:
            offers_row = nib.HStack(
                controls=[
                    nib.Button(
                        content=nib.Image(
                            src=offer.package.icon,
                            width=20,
                            height=20,
                            corner_radius=5,
                        ),
                        style=nib.ButtonStyle.PLAIN,
                        action=lambda url=offer.url: webbrowser.open(url),
                    )
                    for offer in unique_offers
                ],
                spacing=-5,
                # Animate offers appearing
                transition=nib.Transition.combined(nib.Transition.OPACITY, nib.Transition.SCALE),
            )
        else:
            # No matching services - show rent/buy options with prices
            rent_buy = [
                o
                for o in result.offers
                if o.monetization_type in ("RENT", "BUY") and o.price_string
            ]

            # Deduplicate and get cheapest per service
            seen = set()
            unique_rent_buy = []
            for offer in sorted(rent_buy, key=lambda o: o.price_value or 999):
                if offer.package.name not in seen:
                    seen.add(offer.package.name)
                    unique_rent_buy.append(offer)

            offers_row = nib.HStack(
                controls=[
                    nib.HStack(
                        controls=[
                            nib.Image(
                                src=offer.package.icon,
                                width=16,
                                height=16,
                                corner_radius=4,
                            ),
                            nib.Text(
                                offer.price_string,
                                font=nib.Font.system(9),
                                foreground_color=nib.Color.SECONDARY,
                            ),
                        ],
                        spacing=2,
                    )
                    for offer in unique_rent_buy[:4]  # Limit to 4
                ],
                spacing=8,
                # Animate rent/buy options appearing
                transition=nib.Transition.combined(nib.Transition.OPACITY, nib.Transition.SCALE),
            )

        app.height += 100
        result_media.visible = True
        result_media.controls = [
            nib.HStack(
                [
                    image,
                    nib.VStack(
                        [nib.HStack([title, release_year]), short_description],
                        alignment=nib.HorizontalAlignment.LEADING,
                        spacing=5,
                    ),
                    # nib.Spacer(),
                ],
                width=225,
            ),
            offers_row,
        ]

        #
        # 2. build offers row:

    url_input = nib.TextField(
        placeholder="Search... ",
        style=nib.TextFieldStyle.plain,
        foreground_color=nib.Color.SECONDARY,
        # padding=10,
        on_submit=on_search,
    )

    home_view = nib.VStack(
        controls=[
            # Header
            nib.HStack(
                [
                    nib.HStack(
                        controls=[
                            nib.VStack(
                                [
                                    nib.Text(
                                        "Where do i watch it?",
                                        style=nib.TextStyle(
                                            font=nib.Font.custom(
                                                "SF Pro Rounded",
                                                size=15,
                                            )
                                        ),
                                    ),
                                ],
                                alignment=nib.HorizontalAlignment.LEADING,
                            ),
                            nib.Spacer(),
                            services_row,
                        ],
                        alignment=nib.HorizontalAlignment.LEADING,
                    ),
                ]
            ),
            nib.ZStack(
                controls=[
                    # nib.RoundedRectangle(
                    #    fill=nib.Color.SECONDARY.with_opacity(0.1),
                    #    stroke_color=nib.Color.GRAY.with_opacity(0.3),
                    #    stroke_width=1,
                    #    corner_radius=8,
                    #    height=32,
                    # ),
                    url_input,
                ]
            ),
            result_media,
        ],
        spacing=12,
        padding=20,
        alignment=nib.HorizontalAlignment.LEADING,
    )

    app.build(home_view)


nib.run(main)
