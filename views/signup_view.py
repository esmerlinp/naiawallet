import flet as ft
from common.cartera import Cartera
import pyperclip
from bitcoinlib.mnemonic import Mnemonic

def create(page: ft.Page):
    """Vista que carga/crea billeteras."""
    seed = Mnemonic().generate(strength=128).split(" ")
    print(" ".join(seed))
    def paper_paste_to(e):
        """Pega el contenido del portapapeles a frases semilla"""
        passphrases.value = pyperclip.paste()
        passphrases.update()

    def generate_passphrases(e):
        """Genera frases semilla"""
        passphrases.value = Mnemonic().generate()
        passphrases.update() 






    def crear_wallet(e):
        """Crea una billetera"""

        pr.visible = True
        continuar.visible = False
        text_error.visible = False
        passphrases.visible=False
        generar_phrasses.visible=False
        text_error.value = ""
        page.update()
        try:
            Cartera(keys=" ".join(seed))
            
            page.go("/main")
        except Exception as e:
            pr.visible = False
            continuar.visible = True
            text_error.value = e
            text_error.visible = True
            passphrases.visible=True
            generar_phrasses.visible=True
            
        page.update()
            #continuar.update()
            #text_error.update()
            
                

    

    paste_button = ft.IconButton(icon=ft.icons.QR_CODE_SCANNER_SHARP, icon_color="blue400", icon_size=20, on_click= paper_paste_to,  tooltip="Escanear QR")
    passphrases = ft.TextField(label="Frases semillas o clave privada", multiline=True, text_align=ft.TextAlign.START, border_width=0.3, min_lines=4, suffix=paste_button,  autofocus=True, text_size=12, cursor_height=10)

    generar_phrasses = ft.TextButton(
                            text="Generar Frases Semilla",
                            on_click=generate_passphrases,
                        )
    continuar = ft.CupertinoFilledButton(
                            content=ft.Text("CREAR"),
                            opacity_on_click=0.3,
                            on_click=crear_wallet
                            )
    
    continuar.visible = True
    



    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)
    pr.visible = False
    text_error = ft.Text("", color=ft.colors.RED, visible=False)

    #seed_control = ft.Column(controls=[])
    seed_control =[
        ft.Column([
                ft.TextField(
                    label=str(i +1),
                    border=ft.InputBorder.NONE,
                    value=w,
                    password=True,
                    can_reveal_password=True,
                    #disabled=True
                    
                ), 
                ft.Divider()
            ]) for i, w in enumerate(seed)
    ]


    return \
        ft.View(
            "/crear",
            [
                ft.AppBar(title=ft.Text("Sign Up")),
                ft.Column(
                    seed_control, 
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        generar_phrasses,
                    ], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),



                ft.Row(
                    [
                        continuar,
                    ], alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Row(
                    [
                        pr,
                    ], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        text_error,
                    ], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(),
            ],
            scroll=ft.ScrollMode.HIDDEN,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )