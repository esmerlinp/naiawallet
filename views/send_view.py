import flet as ft
from common.cartera import Cartera, btc_price
from common.mservices import MService
import pyperclip, time, datetime
#import pyzbar.pyzbar as pyzbar 
import cv2
from bitcoinlib.services.mempool import MempoolClient


def send_view(mwallet: Cartera, page: ft.Page, offline=False):
    """ Vista para realizar pagos.
    """
    pool = MempoolClient(mwallet.network_name, '''https://mempool.space/api/''', 1)
   
    #Open Camera
    def opencamera(e):
        cap = cv2.VideoCapture(0)
        qr_found = False

        while not qr_found:
            ret, frame = cap.read()
            if ret:
                #decode_qr(frame)
                qr_found = True


    #FUNCIONES
    def pay(e):
        pr.visible = True
        page.update()

        #if offline:
        #    mwallet.utxo_add('16QaHuFkfuebXGcYHmehRXBBX7RG9NbtLg', 100000000, '748799c9047321cb27a6320a827f1f69d767fe889c14bf11f27549638d566fe4', 0)
        #tx = mwallet.transaction_create(output_arr=[(to.value, f"{monto.value} tBTC")],network="testnet")
        #tx.sign(None)
        #tx.fee_per_kb = int(float(tx.fee) / float(tx.vsize) * 1000)
        #print(tx.fee_per_kb)
        #resultado.value = tx.fee_per_kb
        #page.update()
        transaction = mwallet.send_to(to_address=to.value, amount=float(monto.value) * 100000000 , fee=fee.value, offline=offline, locktime=int(_fechaTimeStamp) if _fechaTimeStamp > 0 else 0) 
        if transaction[0]:
            page.go(f"/comprobante/{transaction[1]}")
        else:
            pr.visible = False
            resultado.value = str(transaction[1])
            page.update()

         

    def paper_paste_to(e):
        to.value = pyperclip.paste()
        to.update()  


    #estimate_fee = MService(network=mwallet.networks(as_dict=True)[0]['name']).estimate_fee()
    estimate_fee = int(pool.estimatefee(3)) / 1000

    estimate_fee_text = ft.Text(f"{estimate_fee} sat/vB", color=ft.colors.ORANGE)
    fecha = ft.Text(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))    
    _fechaTimeStamp = 0

    #COMPONENTES
    b_paste = ft.IconButton(icon=ft.icons.COPY, icon_color="blue400", icon_size=20, on_click= paper_paste_to,  tooltip="Pegar Dirección")
    b_camera = ft.IconButton(icon=ft.icons.QR_CODE_SCANNER_SHARP, icon_color="blue400", icon_size=20, on_click= paper_paste_to,  tooltip="Escanear QR")
    to = ft.CupertinoTextField(placeholder_text="Dirección destino", text_size=14, suffix=b_camera, bgcolor=ft.colors.GREY_200)
    nota = ft.CupertinoTextField(placeholder_text="Nota personal", text_size=14, min_lines=2, bgcolor=ft.colors.GREY_200)
    monto_usd = ft.Text("0.00 USD$\t", color=ft.colors.GREY, theme_style=ft.TextThemeStyle.BODY_SMALL, size=12)


    monto = ft.CupertinoTextField(placeholder_text="0.01 BTC (Monto)", 
                                  suffix=monto_usd,
                                  placeholder_style=ft.TextStyle(color="grey"), 
                                  keyboard_type=ft.KeyboardType.EMAIL, 
                                  text_size=14, border=ft.border.all(2, ft.colors.BLACK), 
                                  bgcolor=ft.colors.GREY_200, 
                                  on_change=lambda e: on_change_amount(e))
    fee = ft.CupertinoTextField(placeholder_text="0.0000 sats", 
                                suffix=ft.Text("SATS\t", color=ft.colors.GREY, theme_style=ft.TextThemeStyle.BODY_SMALL, size=12),
                                placeholder_style=ft.TextStyle(color="grey"), 
                                keyboard_type=ft.KeyboardType.EMAIL, text_size=14, border=ft.border.all(2, ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
    resultado = ft.Text("", color=ft.colors.RED_200, height=200)
    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

    def slider_changed(e):
        print(e.data)
        estimate_fee = 0
        if int(e.data) == 1:
            estimate_fee = int(pool.estimatefee(3)) / 1000

        elif int(e.data) == 2:
            estimate_fee = int(pool.estimatefee(1)) / 1000

        else:
            estimate_fee = int(pool.estimatefee(8)) / 1000

        estimate_fee_text.value = f"{int(estimate_fee)} sat/VB"
        fee.value = int(estimate_fee) * 140


        page.update()

    
    pr.visible = False
    continuar = ft.CupertinoFilledButton(
                            content=ft.Text("Continuar"),
                            opacity_on_click=0.3,
                            on_click=pay
                            )
    
    #######################################################################
    def change_date(e):
        _fechaTimeStamp = date_picker.value.timestamp()
        fecha.value = f'{date_picker.value.strftime("%Y-%m-%d %H:%M:%S")} / {_fechaTimeStamp}'
        page.update()

    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")

    date_picker = ft.DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 10, 1),
    )

    page.overlay.append(date_picker)
    #######################################################################
    #to.value = "tb1qa5kd8s4f8gc7ptjcwgmluqm2s54kgntex0aw9j"
    #monto.value = "0.0001"


    def on_change_amount(e):
        if monto.value:
            m = float(monto.value)
            if m > 0:
                monto_usd.value = "{:.2f}".format(m * btc_price()) + " USD$\t"
                monto_usd.update()    
            
    return \
            ft.View(
                "/enviar",
                [ 
                    ft.AppBar(title=ft.Text("Realizar Pago", theme_style=ft.TextThemeStyle.BODY_MEDIUM), center_title=True),
                    ft.Container(expand=True),

                    ft.Row(
                        [
                            ft.Text(mwallet.saldo, theme_style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),

                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Text('{:.2f} USD$'.format(float(mwallet.saldo.split(" ")[0]) * btc_price()), theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                            

                    ft.Row(
                        [
                            to,
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),


                    ft.Divider(),
                    ft.Row(
                        [ ft.Text("Prioridad")],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            ft.CupertinoSlidingSegmentedButton(
                                selected_index=1,
                                thumb_color=ft.colors.BLUE_400,
                                on_change=lambda e: slider_changed(e),
                                padding=ft.padding.symmetric(0, 10),
                                controls=[
                                    ft.Text("baja"),
                                    ft.Text("media"),
                                    ft.Text("alta"),
                                ],
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Row(
                        [
                            monto
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            fee,
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    
                    ft.Row(
                        [
                            ft.Text("Comisión estimada"),
                            ft.Text("/"),
                           estimate_fee_text,
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),


                    ft.Row(
                        [
                            ft.TextButton(text="Aplicar en fecha", icon=ft.icons.CALENDAR_MONTH_ROUNDED, on_click=lambda _: date_picker.pick_date()),
                            ft.Text("/"),
                            fecha,
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    
                    
                        
                    ft.Container(),

                    ft.Row(
                        [
                            continuar,
                            
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Container(),
                    
                    ft.Row(
                        [
                            pr, ft.Text("Wait for the completion..." if pr.visible else ""),
                            
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Container(expand=True),
                    
                    ft.Row(
                        [
                            resultado,
                            
                        ], alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(expand=True)

                ],
            )
        
    