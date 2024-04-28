import flet as ft
from common.cartera import Cartera
import pyperclip
import base64, time
from common.mcode import generar_codigo_qr


def receive_view(mwallet: Cartera, page: ft.Page):
    """ Vita QR para recibir fondos.
    """
    #generar_codigo_qr(mwallet.address)

    image_holder = ft.Image(
                                fit=ft.ImageFit.CONTAIN,
                                
                            )
    
    toast_msg = ft.Text("Copiado al portapapeles", theme_style=ft.TextThemeStyle.BODY_SMALL, visible=False)
    copy_btn = ft.CupertinoFilledButton(
                                        content=ft.Text("COPIAR"),
                                        opacity_on_click=0.3,
                                        padding=10,
                                        on_click=lambda e: copy_address(e)
                                    )
    share_btn = ft.CupertinoFilledButton(
                                        content=ft.Text("COMPARTIR"),
                                        opacity_on_click=0.3,
                                        padding=10,
                                        #on_click=lambda _: page.go("/recibir"),
                                    )
    address = mwallet.addresslist()[0]
    def copy_address(e):
        
        pyperclip.copy(address)
        toast_msg.visible = True
        toast_msg.update()

        time.sleep(2)
        toast_msg.visible = False
        toast_msg.update()


    with open("./qr_code.png", 'rb') as r:
        image_holder.src_base64 = base64.b64encode(r.read()).decode("utf-8")
        image_holder.visible=True
        page.update()

 
    return \
        ft.View(
                    "/recibir",
                    [   
                        ft.AppBar(title=ft.Text("Recibir", theme_style=ft.TextThemeStyle.BODY_MEDIUM)),
                        ft.Row(
                            [
                              image_holder,

                            ], 
                            alignment=ft.MainAxisAlignment.CENTER,
                           
                        ),
                        ft.Row(
                            [
                                ft.Text(address, theme_style=ft.TextThemeStyle.BODY_MEDIUM)
                            ],  alignment=ft.MainAxisAlignment.CENTER,
                        ),



                        ft.Row(
                                [
                                    share_btn,
                                    copy_btn,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ft.Row(
                            [
                                toast_msg,
                            ], alignment=ft.MainAxisAlignment.CENTER
                        )

                    ]
                )
           
    