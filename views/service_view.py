import  flet as ft 
from common.cartera import Cartera, btc_price
from common.keyboard import keyboard

def service_view(page: ft.Page, mwallet:Cartera):
    """Vista de servicios.
    Esta vista tiene el objetivo de obtener informaciones de direcciones y transacciones de terceros.
    """
    utxos = mwallet.utxos()
    print(utxos)
    k =  keyboard() 


    def tile_clicked(e):
        print("Tile clicked")

    return \
        ft.View(
            "/service",
            [
                ft.AppBar(title=ft.Text("Servicios", theme_style=ft.TextThemeStyle.BODY_MEDIUM), center_title=True),
                ft.Text("UTXO's", theme_style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Column(
                    
                    [
                        ft.CupertinoListTile(
                            additional_info=ft.Text('{:.2f} USD'.format(float(mwallet.saldo.split(" ")[0]) * btc_price()), size=12, ),
                            bgcolor_activated=ft.colors.AMBER_ACCENT,
                            #leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
                            title=ft.Text(f'{u["value"]} sats'),
                            subtitle=ft.Text(u["txid"]),
                            #trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
                            on_click=tile_clicked,
                        ) for u in utxos 
                    
                    ]
                    
                ) ,
                k,


            ],scroll=ft.ScrollMode.ALWAYS,
        )
