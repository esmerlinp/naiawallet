import flet as ft
from common.cartera import btc_price


def signup(page: ft.Page):
    precio = ft.Text(value=f"USD$ {btc_price()}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, color=ft.colors.GREY)

    def price(e):
        precio.value = f"USD$ {btc_price()}"
        page.update()
    

    return \
        ft.View(
            "/sign",
            [
                ft.AppBar(title=ft.Row([ft.Icon(ft.icons.MAP_ROUNDED, color=ft.colors.BLUE), 
                                        ft.Text(value="Naia Wallet", style=ft.TextThemeStyle.TITLE_LARGE)], 
                                        alignment=ft.MainAxisAlignment.CENTER)), #APPBAR
                ft.Container(expand=True),

                ft.Row([
                    ft.CupertinoFilledButton(
                                                content=ft.Text("Crear Cartera"),
                                                opacity_on_click=0.3,
                                                on_click=lambda _: page.go("/crear"),
                                                
                                            )
                ], alignment=ft.MainAxisAlignment.CENTER),

                ft.Row([
                    ft.CupertinoButton(
                                                content=ft.Text("Importar"),
                                                opacity_on_click=0.3,
                                                on_click=lambda _: page.go("/importar"),
                                            )
                ], alignment=ft.MainAxisAlignment.CENTER),

                ft.Container(expand=True),
                ft.Row([precio, ft.IconButton(icon=ft.icons.SYNC, icon_size=15, on_click=lambda e: price(e))], 
                       alignment=ft.MainAxisAlignment.CENTER),

            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )