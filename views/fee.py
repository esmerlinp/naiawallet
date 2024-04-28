from bitcoinlib.services.mempool import MempoolClient
import flet as ft
from common.cartera import Cartera, btc_price

def fee(page: ft.Page, wallet:Cartera):

    price = wallet.btc_usd_float

    def usd_fee(block: int):
        return "$ {:.2f}".format((((wallet.estimatefee(block)/ 1000) * 140) / 100000000) * price)
    
    text_price = ft.Text(value=wallet.btc_usd, theme_style=ft.TextThemeStyle.TITLE_LARGE)
    
    text_high_sats_usd = ft.Text(f"{usd_fee(1)}", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.colors.GREEN if int(wallet.estimatefee(1) / 1000) <= 20 else ft.colors.ORANGE)
    text_high_sats = ft.Text(f"{int(wallet.estimatefee(1) / 1000)} sat/vB", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    
    text_medium_sats_usd = ft.Text(f"{usd_fee(3)}", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.colors.GREEN if int(wallet.estimatefee(3) / 1000) <= 20 else ft.colors.ORANGE)
    text_medium_sats = ft.Text(f"{int(wallet.estimatefee(3) / 1000)} sat/vB", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    
    text_low_sats = ft.Text(f"{int(wallet.estimatefee(6) / 1000)} sat/vB", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    text_low_sats_usd = ft.Text(f"{usd_fee(6)}", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.colors.GREEN if int(wallet.estimatefee(6) / 1000) <= 20 else ft.colors.ORANGE)
   
    text_min_sats = ft.Text(f"{int(wallet.estimatefee(9) / 1000)} sat/vB", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    text_min_sats_usd = ft.Text(f"{usd_fee(8)}", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.colors.GREEN if int(wallet.estimatefee(8) / 1000) <= 20 else ft.colors.ORANGE)

    text_bloque = ft.Text(f"Bloque Actual: {wallet.bloque_actual}", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    def callback(**kargs)-> None:

        text_price.value = kargs['btc_usd']
        price = kargs['btc_usd_float']
        
        text_high_sats.value = f"{int(kargs['rate_high'])} sat/vB"
        text_medium_sats.value = f"{int(kargs['rate_medium'])} sat/vB"
        text_low_sats.value = f"{int(kargs['rate_low'])} sat/vB"
        text_min_sats.value = f"{int(kargs['rate_min'])} sat/vB"

        text_high_sats_usd.value = "$ {:.2f}".format(((int(kargs['rate_high']) * 140) / 100000000) * price)
        text_medium_sats_usd.value = "$ {:.2f}".format(((int(kargs['rate_medium']) * 140) / 100000000) * price)
        text_low_sats_usd.value = "$ {:.2f}".format(((int(kargs['rate_low']) * 140) / 100000000) * price)
        text_min_sats_usd.value = "$ {:.2f}".format(((int(kargs['rate_min']) * 140) / 100000000) * price)
        text_bloque.value  = f"Bloque Actual: {kargs['bloque_actual']}"

        page.update()




    wallet.start_background_task(callback=callback)
    
   
    
    priceCard = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.CURRENCY_BITCOIN, size=30),
                            title=text_price,
                            subtitle=text_bloque,
                        ),
                    ]
                ),
                padding=10,
            )
        )
    

    feecard = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(value="Prioridad Alta", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                            subtitle=ft.Row([
                                text_high_sats,
                                ft.Container(expand=True),
                                text_high_sats_usd
                                ]),
                        ),
                        ft.Divider(),
                        ft.ListTile(
                            title=ft.Text(value="Prioridad Media", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                            subtitle=ft.Row([
                                text_medium_sats,
                                ft.Container(expand=True),
                                text_medium_sats_usd,
                                ]),
                        ),
                        ft.Divider(),

                        ft.ListTile(
                            title=ft.Text(value="Prioridad Baja", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                            subtitle=ft.Row([
                                text_low_sats,        
                                ft.Container(expand=True),
                                text_low_sats_usd,
                                ]),
                        ),
                        ft.Divider(),

                        ft.ListTile(
                            title=ft.Text(value="Prioridad Minima", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                            subtitle=ft.Row([
                                text_min_sats,
                                ft.Container(expand=True),
                                text_min_sats_usd,
                                ]),
                        ),
                    ]
                ),
                padding=10,
            )
        )
    
    bottomAppBar = ft.BottomAppBar(
        #bgcolor=ft.colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.WALLET, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CHECKLIST, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/transacciones")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CURRENCY_BITCOIN_ROUNDED, icon_color=ft.colors.BLACK),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.SETTINGS, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/settings")),
            ]
        ),
    ) 
    
    return \
            ft.View(
                "/fee",
                [
                    ft.AppBar(title=ft.Text("Fee source", theme_style=ft.TextThemeStyle.BODY_MEDIUM)),

                    ft.Column([
                        ft.Text("Precio Actual", theme_style=ft.TextThemeStyle.BODY_LARGE),
                        priceCard,
                        ft.Container(),
                        ft.Text("Comisiones Estimadas", theme_style=ft.TextThemeStyle.BODY_LARGE),
                        feecard

                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bottomAppBar
                ], scroll=ft.ScrollMode.HIDDEN
            )