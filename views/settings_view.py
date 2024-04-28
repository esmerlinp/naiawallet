import flet as ft
from common.keyboard import keyboard

def settings_view(page: ft.Page):
    k =  keyboard() 

    bottomAppBar = ft.BottomAppBar(
        #bgcolor=ft.colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.WALLET, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CHECKLIST, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/transacciones")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.CURRENCY_BITCOIN_ROUNDED, icon_color=ft.colors.BLACK, on_click=lambda _: page.go("/fee")),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.SETTINGS, icon_color=ft.colors.BLACK),
            ]
        ),
    ) 
    
    return \
        ft.View(
            "/settings",
            [
                ft.AppBar(title=ft.Text("Ajustes", theme_style=ft.TextThemeStyle.BODY_MEDIUM), center_title=True),
               
                ft.Card(
                        content=ft.Container(
                            #width=500,
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        title=ft.Text("One-line list tile"),
                                    ),
                                    ft.ListTile(title=ft.Text("One-line dense list tile"), dense=True),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.SETTINGS),
                                        title=ft.Text("One-line selected list tile"),
                                        selected=True,
                                    ),
                                    ft.ListTile(
                                        leading=ft.Image(src="/icons/icon-192.png", fit="contain"),
                                        title=ft.Text("One-line with leading control"),
                                    ),
                                    ft.ListTile(
                                        title=ft.Text("One-line with trailing control"),
                                        trailing=ft.PopupMenuButton(
                                            icon=ft.icons.MORE_VERT,
                                            items=[
                                                ft.PopupMenuItem(text="Item 1"),
                                                ft.PopupMenuItem(text="Item 2"),
                                            ],
                                        ),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.ALBUM),
                                        title=ft.Text("One-line with leading and trailing controls"),
                                        trailing=ft.PopupMenuButton(
                                            icon=ft.icons.MORE_VERT,
                                            items=[
                                                ft.PopupMenuItem(text="Item 1"),
                                                ft.PopupMenuItem(text="Item 2"),
                                            ],
                                        ),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.SNOOZE),
                                        title=ft.Text("Two-line with leading and trailing controls"),
                                        subtitle=ft.Text("Here is a second title."),
                                        trailing=ft.PopupMenuButton(
                                            icon=ft.icons.MORE_VERT,
                                            items=[
                                                ft.PopupMenuItem(text="Item 1"),
                                                ft.PopupMenuItem(text="Item 2"),
                                            ],
                                        ),
                                    ),
                                ],
                                spacing=0,
                            ),
                            padding=ft.padding.symmetric(vertical=10),
                        )
                    ),

                bottomAppBar,

                  
            ]
        )