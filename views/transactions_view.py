import flet as ft
from common.cartera import Cartera


def transaction_view(page:ft.Page, wallet: Cartera) -> ft.Control:
    bottomAppBar = ft.BottomAppBar(
        #bgcolor=ft.colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.WALLET, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CHECKLIST, icon_color=ft.colors.BLACK),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CURRENCY_BITCOIN_ROUNDED, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/fee")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.SETTINGS, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/settings")),
            ]
        ),
    ) 
    

    transacciones = wallet.transactions(as_dict=True)
    #transacciones_full = wallet.transactions_full(include_new=True, limit=3)
    #print(transacciones_full[0])
    
    ft_transactions =[
        ft.Column([
                ft.CupertinoListTile(
                    additional_info=ft.Text(t['date'].strftime("%a %b %d %H:%M"), theme_style=ft.TextThemeStyle.BODY_SMALL),
                    #additional_info=ft.Text(t['date'], theme_style=ft.TextThemeStyle.BODY_SMALL),
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    #leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
                    title=ft.Text(f"{t['value']/100000000}", color= ft.colors.RED if 'index_n' in t else ft.colors.GREEN,  theme_style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(t["address"]),
                    #trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
                    on_click=lambda e, o=t['output_n'],  tid=t['txid']: page.go(f"/transaccions/{tid}/{o}"),
                    padding=2
                ), 
                ft.Divider()
            ]) for i, t in enumerate(transacciones)
    ]


    return \
        ft.View("/transacciones",
                 controls=[
                    ft.AppBar(title=ft.Text("Transacciones")), 
                    ft.Column(controls=ft_transactions if len(ft_transactions)> 0 else [ft.Text("No hay transacciones asociadas", color='grey')]),           
                    bottomAppBar
                 ],
                 scroll=ft.ScrollMode.HIDDEN if len(ft_transactions) > 0 else None, 
                 vertical_alignment=ft.MainAxisAlignment.CENTER,
                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
