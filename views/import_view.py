import flet as ft
from common.cartera import Cartera, KeyFormat
from bitcoinlib.keys import  get_key_format, BKeyError
from bitcoinlib.wallets import WalletError
import time, pyperclip


def importar(page: ft.Page):
    paste_button = ft.IconButton(icon=ft.icons.QR_CODE_SCANNER_SHARP, icon_color="blue400", icon_size=20, on_click= lambda e:paper_paste_to(e),  tooltip="pegar desde portapapeles")
    key_text = ft.CupertinoTextField(text_size=16, placeholder_text="",multiline=True, suffix=paste_button, min_lines=4 , text_align=ft.TextAlign.START, autofocus=True,on_focus=lambda e: clean_error(e))
    network_switch = ft.Switch(adaptive=True, label="testnet", value=False, label_style=ft.TextThemeStyle.BODY_SMALL)
    p2sh_switch = ft.Switch(adaptive=True, label="p2sh", value=False, label_style=ft.TextThemeStyle.BODY_SMALL)

    import_button = ft.CupertinoButton(text="IMPORTAR", disabled_color=ft.colors.GREY, on_click=lambda e, key=key_text.value: load(e,key))
    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2, visible=False)
    error_text = ft.Text("", color=ft.colors.RED,)

    def paper_paste_to(e):
        key_text.value = pyperclip.paste()
        key_text.update()  


    def clean_error(e):
        error_text.value=""
        error_text.update()

    def load(e, key):

        try:
            pr.visible = True
            error_text.visible = False
            error_text.value = ""
            import_button.disabled =  pr.visible
            page.update()
            #{"format": key_format,"networks": networks,"is_private": is_private,"script_types": script_types,"witness_types": witness_types,"multisig": multisig}
            format_key_obj = get_key_format(key_text.value)
            key_format = format_key_obj["format"]
            if key_format == KeyFormat.bip38.value:
                page.go(f"/importar/password/{key_text.value}/{network_switch.value}/{p2sh_switch.value}")
            else:
                network = "testnet" if network_switch.value else "bitcoin"
                witness_type = "segwit" if not p2sh_switch.value else "p2sh-segwit"
                #Cartera(keys=key_text.value)
                Cartera(keys=key_text.value, witness_type=witness_type)
                page.go("/")
    


        except BKeyError as e:
            error_text.value = e
            error_text.visible = True
        except WalletError as e:
            error_text.value = e
            error_text.visible = True
        finally:
            pr.visible = False
            import_button.disabled =  pr.visible
            page.update()    

    return \
        ft.View(
            "/importar",
            [   
                ft.Container(expand=True),
                ft.Row([ft.Icon(name=ft.icons.MAP_ROUNDED, size=40)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.Text("Frases semillas o clave privada", theme_style=ft.TextThemeStyle.BODY_SMALL, size=12, color=ft.colors.GREY)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([key_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.Text("Ingresa tus frases semilla, claves privadas/públicas o bip38. Nosotros nos encargamos del resto.", theme_style=ft.TextThemeStyle.BODY_SMALL, color=ft.colors.GREY, size=12)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([import_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([pr], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([error_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(expand=True),
                ft.Row([network_switch, p2sh_switch], alignment=ft.MainAxisAlignment.CENTER)
                
            ], vertical_alignment=ft.MainAxisAlignment.CENTER
        )


def bip38_import(key:str, istestnet:bool, witness_type:str, page: ft.Page):
    paste_button = ft.IconButton(icon=ft.icons.QR_CODE_SCANNER_SHARP, icon_color="blue400", icon_size=20, on_click= lambda e:paper_paste_to(e),  tooltip="pegar desde portapapeles")
    passwd_text = ft.CupertinoTextField(text_size=12, placeholder_text="Ingresa la contraseña", suffix=paste_button, password=True, on_focus=lambda e: clean_error(e))
    import_button = ft.CupertinoButton(text="COMPLETAR", disabled_color=ft.colors.GREY, on_click=lambda e, key=passwd_text.value: load(e))
    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2, visible=False)
    error_text = ft.Text("", color=ft.colors.RED,)


    def paper_paste_to(e):
        passwd_text.value = pyperclip.paste()
        passwd_text.update()  

    def clean_error(e):
        error_text.value=""
        error_text.update()

    def load(e):
        pr.visible = True
        error_text.visible = False
        error_text.value = ""
        import_button.disabled =  pr.visible
        pr.update()
        try:
            #{"format": key_format,"networks": networks,"is_private": is_private,"script_types": script_types,"witness_types": witness_types,"multisig": multisig}
            Cartera(keys=key, passwd=passwd_text.value, network="bitcoin" if not istestnet else "testnet", witness_type=witness_type)
            page.go("/")

        except BKeyError as e:
            error_text.value = e
            error_text.visible = True
        finally:
            pr.visible = False
            import_button.disabled =  pr.visible
            page.update()    
    

    return \
        ft.View("/importar/password",
                [
                    
                    ft.Row([ft.Icon(name=ft.icons.MAP_ROUNDED, size=40)], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([passwd_text], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text("Ingresa tus frases semilla, claves privadas/públicas o bip38. Nosotros nos encargamos del resto.", theme_style=ft.TextThemeStyle.BODY_SMALL, color=ft.colors.GREY, size=10)], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([import_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([pr], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([error_text], alignment=ft.MainAxisAlignment.CENTER),
                ], vertical_alignment=ft.MainAxisAlignment.CENTER
            )