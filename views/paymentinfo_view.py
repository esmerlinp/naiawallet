import flet as ft
from common.cartera import Cartera
import datetime

def paymentInfo(mwallet:Cartera, txid:str):
    #txid = 'b3156881c6ec9e6f15e12d38a9bc1e4ed094071b22fe6db35d3547784f7d0056'
    mwallet.transactions_update()
    transaction = mwallet.transaction(txid=txid, output_n=0)
    print(transaction)



    return ft.View(
        "/comprobante",
        [
            ft.AppBar(title=ft.Text("Detalle de Pago", theme_style=ft.TextThemeStyle.BODY_MEDIUM), center_title=True),
            ft.Column([
                ft.Row([ft.Text("Pagaste", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, size=18, color=ft.colors.GREY)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.Text(f"{transaction['value']/100000000}", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, color=ft.colors.RED)], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Row([ft.Text(f"{transaction['status'].capitalize()}", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN, size=16)], alignment=ft.MainAxisAlignment.START),
                ft.Container(),
                ft.Row([ft.Text("Descripción", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, color=ft.colors.GREY)], alignment=ft.MainAxisAlignment.START),
                ft.Column(
                    [
                        ft.Text(f"Para", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREY),                                
                        ft.Text(transaction["address"], theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),                                

                    ], spacing=1    
                ),
                ft.Column([
                    ft.Text(f"Fecha", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREY),                                
                    ft.Text(f"{transaction['date']}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),                                

                ], spacing=1),


                ft.Row([ft.Text(f"Monto\n{transaction['value']/100000000} Fee incluido", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),

                        ft.Container(expand=True),
                        ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=15, tooltip="Copiar",)]),                                

                #ft.Row([ft.Text(f"Transacción Anterior\n{transaction['prev_txid']}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),
                #        ft.Container(expand=True),
                #        ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=15, tooltip="Copiar",)]),                                
                ft.Divider(),
                ft.Card(
                    content=ft.Container(

                        content=ft.Column(
                            [
                                ft.Column([
                                    ft.Column([
                                        ft.Text(f"Tamaño del bloque\t", theme_style=ft.TextThemeStyle.BODY_SMALL, weight=ft.FontWeight.BOLD, size=14, color=ft.colors.GREY),
                                        ft.Text(f"{transaction['block_height']}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=13),
                                    ], spacing=1),
                                    ft.Column([
                                        ft.Text(f"Confirmaciones\t", theme_style=ft.TextThemeStyle.BODY_SMALL, weight=ft.FontWeight.BOLD, size=14, color=ft.colors.GREY),
                                        ft.Text(f"{transaction['confirmations']}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=13),
                                    ], spacing=1),    

                                ], spacing=10),

                                ft.Column([
                                    ft.Text(f"Tansacción de {transaction['network_name']}", theme_style=ft.TextThemeStyle.BODY_SMALL, weight=ft.FontWeight.BOLD, size=14, color=ft.colors.GREY),
                                    ft.Text(f"{transaction['txid']}", height=100, theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),
                                ], spacing=1),

                            ]
                        )
                    ), expand=True

                )

            ])
        ]
    )
    
