import flet as ft 
from common.cartera import Cartera, DEFAULT_DATABASE, btc_price
from bitcoinlib.wallets import wallet_delete_if_exists, wallets_list


def main_view(mwallet: Cartera, page: ft.Page):
    """
    Vista Principal Muestra saldo, opciones para enviar y recibir btc.

    :param mwallet: Instancia de la cartera.
    :type mwallet: Cartera.
    :param page: Pagina principal.
    :type  page: ft.Page.
    """


    #FUNCIONES
    def open_info(e):
        """Muestra informacion del la cartera actual. Address principal, tipo de direccion, precio de bitcoin en dolares."""
        dlg = ft.AlertDialog(title=ft.Text(mwallet.network_name, theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                                            content=ft.Text(f"Addr:\n{mwallet.addresslist()[0]}\nType: {mwallet.witness_type}\nPrice: {btc_price()}", theme_style=ft.TextThemeStyle.BODY_SMALL),
                                            on_dismiss=lambda e: print("Dialog dismissed!"),
                                            )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def update(e):
        """Actualizar cartera"""
        
        update_button.visible = False
        pr_update.visible = True
        page.update()
        mwallet.scan()

        pr_update.visible = False
        update_button.visible = True
        page.go("/")

    def logOut(e):
        """Eliminar cartera actual y sale del sistema."""
        pr.visible = True
        pr.update()
        if wallet_delete_if_exists("bitcoin", db_uri=DEFAULT_DATABASE, force=True):
            page.go("/load")

    def show_picker(e):
        """Picker para cambiar de wallet( no implementado aun)"""

        ####################################################################
        wallets_Obj = wallets_list(db_uri=DEFAULT_DATABASE)
        wallets = [w['name'] for w in wallets_Obj]
        ####################################################################

        def handle_picker_change(e):
            CURRENT_WALLET = wallets[int(e.data)]
            print(CURRENT_WALLET)
            page.update()  

        picker = ft.CupertinoPicker(
            selected_index=3,
            # item_extent=40,
            magnification=1.22,
            # diameter_ratio=2,
            squeeze=1.2,
            use_magnifier=True,
            # looping=False,
            on_change= lambda e: handle_picker_change(e),
            controls=[ft.Text(f) for f in wallets],
            )
        
        
        page.show_bottom_sheet(
                            ft.CupertinoBottomSheet(
                                picker,
                                height=216,
                                padding=ft.padding.only(top=6),
                                on_dismiss=lambda e: update(e),
                            )
                        )
       # picker.visible = not picker.visible
        page.update() 

    
    #COMPONENTES
    
    btcprice = ft.Text('{:.2f} USD'.format(float(mwallet.saldo.split(" ")[0]) * btc_price()), theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    update_button = ft.IconButton(ft.icons.UPDATE, icon_color="blue400", icon_size=20, on_click= update)
    wallets_list_button = ft.IconButton(ft.icons.WALLET_ROUNDED, icon_color="blue400", icon_size=20, on_click=show_picker)
    pr_update = ft.ProgressRing(width=12, height=12, stroke_width = 2, visible=False)
    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2, visible=False)
    appbar = ft.AppBar(
        #leading=ft.Icon(ft.icons.ATTACH_MONEY),
        leading_width=40,
        title=ft.Row([ft.Icon(ft.icons.MAP_ROUNDED), 
                                        ft.Text(value=mwallet.name, theme_style=ft.TextThemeStyle.TITLE_LARGE)], 
                                        alignment=ft.MainAxisAlignment.START),
        center_title=False,
        bgcolor=ft.colors.WHITE,
        actions=[
            ft.IconButton(ft.icons.INFO, icon_color="blue400", icon_size=20, on_click=open_info),
            update_button,
            wallets_list_button,
            ft.Container(pr_update, padding=ft.padding.only(right=15))
        ],
    ) 
    bottomAppBar = ft.BottomAppBar(
        #bgcolor=ft.colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.WALLET, icon_color=ft.colors.BLACK),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CHECKLIST, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/transacciones")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CURRENCY_BITCOIN_ROUNDED, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/fee")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.SETTINGS, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/settings")),
            ]
        ),
    )   
    
    

    
    #VISTA PRINCIPAL

    return \
        ft.View(
            "/main",
            [
                appbar,
                ft.Column([
                            #BALANCE
                            ft.Row(
                                [ft.Text(str(mwallet.saldo), theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),

                            #BALANCE USD
                            ft.Row(
                                    [
                                        btcprice,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                            ),

                            #BOTONES RECIBIR / ENVIAR
                            ft.Row(
                                    [
                                        ft.CupertinoFilledButton(
                                            content=ft.Text("RECIBIR"),
                                            opacity_on_click=0.3,
                                            on_click=lambda _: page.go("/recibir"),
                                        ),
                                        ft.CupertinoFilledButton(
                                            content=ft.Text("ENVIAR"),
                                            opacity_on_click=0.3,
                                            on_click=lambda _: page.go("/enviar")
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ft.Row([ft.TextButton("Log Out", on_click=logOut )], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([pr], alignment=ft.MainAxisAlignment.CENTER),
                            
                            
                        ], alignment=ft.MainAxisAlignment.CENTER
                ),
                bottomAppBar
                    
                            
            ], vertical_alignment=ft.MainAxisAlignment.CENTER,
        
        )