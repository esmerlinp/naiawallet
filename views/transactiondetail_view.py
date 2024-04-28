import flet as ft
from common.cartera import Cartera
from common.mservices import MService
from bitcoinlib.wallets import WalletTransaction
import pyperclip

def copy_address(e, value):
    pyperclip.copy(value)

def get_transaction(mwallet: Cartera, txid: str) -> dict:
    "return WalletTransaction"
    #mserv = MService()
    wtx = mwallet.transaction(txid=txid)
    
    tx = wtx.to_transaction().as_dict()
    return tx

def is_output_transaction(mwallet: Cartera, transaction: WalletTransaction) -> bool:

    if 'index_n' in transaction:
       return True
    else:
        return  False

    print("TTTTTTT ---> ", transaction)    
    direcciones_salida = [output['address'] for output in transaction["outputs"]]
    mis_direcciones = mwallet.addresslist()
    for addr in mis_direcciones:
        if addr in direcciones_salida:
            return True

    return False    
    #return mwallet.addresslist() in direcciones_salida

def trans_detail(mwallet: Cartera, txid: str, output_n=0):
    tx = get_transaction(mwallet, txid)
    
    
    is_output = is_output_transaction(mwallet, tx)
    #is_output = transaction["is_output"]
    #direcciones_salida = [output['address'] for output in transaction['outputs']]
    #transaction["is_output"] = is_output
    return output_view(tx) if is_output else input_view(tx)
    
    
    
    

def output_view(transaction):
    """Muestra detalle de una transacción saliente"""

    return ft.View(
        "/transactions",
        [
            ft.AppBar(title=ft.Text("Detalle de pago", theme_style=ft.TextThemeStyle.BODY_MEDIUM), center_title=True),
            ft.Column([
                ft.Row([ft.Text("Pagaste", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, size=18, color=ft.colors.GREY)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.Text(f"{(transaction['output_total'] - transaction['fee'])/100000000}", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, color=ft.colors.RED)], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Row([ft.Text(f"{transaction['status'].capitalize()}", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN, size=16)], alignment=ft.MainAxisAlignment.START),
                ft.Container(),
                ft.Row([ft.Text("Descripción", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, color=ft.colors.GREY)], alignment=ft.MainAxisAlignment.START),
                ft.Column(
                    [
                        ft.Text(f"Para", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREY),                                
                        ft.Row([
                            ft.Text(transaction["outputs"][0]["address"], theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),
                            #ft.Container(expand=True),
                            ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=15, tooltip="Copiar", on_click=lambda e, value=transaction["outputs"][0]["address"]: copy_address(e, value))
                        ]),                             

                    ], spacing=1    
                ),
                ft.Column([
                    ft.Text(f"Fecha", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREY),                                
                    ft.Text(f"{transaction['date']}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),                                

                ], spacing=1),


                ft.Row([
                        ft.Text(f"Monto\n{(transaction['output_total'] - transaction['fee'])/100000000} BTC", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),
                        ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=15, tooltip="Copiar", on_click=lambda e, value=((transaction['output_total'] - transaction['fee'])/100000000): copy_address(e, value)),
                    ]),                                
                ft.Row([
                        ft.Text(f"Fee\n{transaction['fee']} sats ", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),
                    ]),                                

                #ft.Row([ft.Text(f"Transacción Anterior\n{transaction['prev_txid']}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),
                #        ft.Container(expand=True),
                #        ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=15, tooltip="Copiar",)]),                                
                ft.Divider(),

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


                ft.CupertinoListTile(
                    #additional_info=ft.Text(f"{t['date']}", theme_style=ft.TextThemeStyle.BODY_SMALL),
                    #additional_info=ft.Text("Wed Jan 24", theme_style=ft.TextThemeStyle.BODY_SMALL),
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    #leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
                    title=ft.Text(f"Tansacción de {transaction['network']}",   theme_style=ft.TextThemeStyle.BODY_SMALL, weight=ft.FontWeight.BOLD, size=14, color=ft.colors.GREY),
                    subtitle=ft.Text(transaction["txid"]),
                    #trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
                    on_click=lambda e, value=transaction["txid"]: copy_address(e, value),
                    padding=0
                ) 
     
            ])
        ],
        scroll=ft.ScrollMode.HIDDEN
    )
    
def input_view(transaction):
    """Muestra detalle de una transacción entrante"""

    return ft.View(
        "/transactions",
        [
            ft.AppBar(title=ft.Text("Detalle de pago", theme_style=ft.TextThemeStyle.BODY_MEDIUM), center_title=True),
            ft.Column([
                ft.Row([ft.Text("Recibiste", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, size=18, color=ft.colors.GREY)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.Text(f"{transaction['inputs'][0]['value']/100000000}", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Row([ft.Text(f"{transaction['status'].capitalize()}", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN, size=16)], alignment=ft.MainAxisAlignment.START),
                ft.Container(),
                ft.Row([ft.Text("Descripción", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, color=ft.colors.GREY)], alignment=ft.MainAxisAlignment.START),
                ft.Column(
                    [
                        ft.Text(f"Desde", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREY),  
                        ft.Row([
                            ft.Text(transaction['inputs'][0]["address"], theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),
                            #ft.Container(expand=True),
                            ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=15, tooltip="Copiar", on_click=lambda e, value=transaction['inputs'][0]["address"]: copy_address(e, value))
                            ]),                                

                    ], spacing=1    
                ),
                ft.Column([
                    ft.Text(f"Fecha", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREY),                                
                    ft.Text(f"{transaction['date']}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=14),                                

                ], spacing=1),


                ft.Row([
                        ft.Text(f"Monto\n{transaction['inputs'][0]['value']/100000000}", theme_style=ft.TextThemeStyle.BODY_SMALL, size=12),
                        ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=15, tooltip="Copiar", on_click=lambda e, value=(str(transaction['inputs'][0]["value"]/100000000)): copy_address(e, value))
                    ]),                                
                               
                ft.Divider(),

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

                ft.CupertinoListTile(
                        #additional_info=ft.Text(f"{t['date']}", theme_style=ft.TextThemeStyle.BODY_SMALL),
                        #additional_info=ft.Text("Wed Jan 24", theme_style=ft.TextThemeStyle.BODY_SMALL),
                        bgcolor_activated=ft.colors.AMBER_ACCENT,
                        #leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
                        title=ft.Text(f"Tansacción de {transaction['network']}",   theme_style=ft.TextThemeStyle.BODY_SMALL, weight=ft.FontWeight.BOLD, size=14, color=ft.colors.GREY),
                        subtitle=ft.Text(transaction["txid"]),
                        #trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
                        on_click=lambda e, value=transaction["txid"]: copy_address(e, value),
                        padding=0
                    ) 

            ])
        ],
        scroll=ft.ScrollMode.HIDDEN
    )
    