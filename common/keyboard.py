import flet as ft

def keyboard():
    return \
        ft.Container(content=ft.Column([
            ft.Row([
                ft.TextButton("1"),
                ft.Container(expand=True),
                ft.TextButton("2"),
                ft.Container(expand=True),
                ft.TextButton("3"),
            ], alignment=ft.MainAxisAlignment.CENTER),
        
            ft.Row([
                ft.TextButton("4"),
                ft.Container(expand=True),
                ft.TextButton("5"),
                ft.Container(expand=True),
                ft.TextButton("6"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.TextButton("7"),
                ft.Container(expand=True),
                ft.TextButton("8"),
                ft.Container(expand=True),
                ft.TextButton("9"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.TextButton("."),
                ft.Container(expand=True),
                ft.TextButton("0"),
                ft.Container(expand=True),
                #ft.TextButton("X"),
                ft.IconButton(icon=ft.icons.BACKSPACE),
            ], alignment=ft.MainAxisAlignment.START),
            
        ],alignment=ft.MainAxisAlignment.START))