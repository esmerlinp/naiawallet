import flet as ft
from flet import ViewPopEvent, View, RouteChangeEvent
from common.cartera import Cartera, DEFAULT_DATABASE
from views.transactiondetail_view import trans_detail
from views.send_view import send_view
from views.receive_view import receive_view
from views.transactions_view import transaction_view
from views.main_view import main_view
from views.service_view import service_view
from views.signup_view import create
from bitcoinlib.wallets import  wallet_exists
from views.paymentinfo_view import paymentInfo
from views.settings_view import settings_view
from views.signup import signup
from views.fee import fee
from views.import_view import importar, bip38_import


#passphrases = "divorce frame wonder arrange gold chalk south original ceiling submit arena settle"
passphrases = None
offline_tansactions = False
#mwallet = None
CURRENT_WALLET = "bitcoin"




def main(page: ft.Page):
    page.title = "NAIA WALLET"
    print("Initial route:", page.route)

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )
        
    #VISTAS
    def route_change(e: RouteChangeEvent):
        
        page.views.clear()
        troute = ft.TemplateRoute(page.route) 

        mwallet = None
        if wallet_exists(CURRENT_WALLET, DEFAULT_DATABASE): 
            mwallet = Cartera(network="testnet")

        #VISTA PRINCIPAL

        page.views.append(
            signup(page) if not wallet_exists(CURRENT_WALLET, DEFAULT_DATABASE) else main_view(mwallet, page)
        )  


        if page.route == "/load":
            page.views.append(
                #load(page)
                signup(page)
            )  

        if page.route == "/crear":
            page.views.append(
                #load(page)
                create(page)
            )  
            

        if page.route == "/main":
            page.views.append(
                main_view(mwallet, page)
           )
    



        #VISTA TRANSACIONES

        if page.route == "/transacciones":
            page.views.append(
                transaction_view(page, mwallet)
            )

        if page.route == "/fee":
            page.views.append(
                fee(page, mwallet),
            )

        
        #VISTA PARA RECIBIR BTC
        if page.route == "/recibir":
            #VISTA DE PAGO RECIBIR
            page.views.append(
                receive_view(mwallet, page)
            )
        if page.route == "/importar":
            #VISTA DE PAGO RECIBIR
            page.views.append(
                importar(page)
            )


        #VISTA PARA ENVIAR BTC
        if page.route == "/enviar":
            page.views.append(
                 #VISTA DE ENVIAR BTC   
                send_view(mwallet, page, offline=offline_tansactions)
            )
        
        
        #VISTA DETALLE DE TRANSACCION

        if troute.match("/transaccions/:txid/:output_n"):
             page.views.append(
                trans_detail(mwallet, troute.txid, troute.output_n)
            )
             
        if troute.match("/comprobante/:txid"):
             page.views.append(
                paymentInfo(mwallet, troute.txid)
            )
             
        if troute.match("/importar/password/:key/:istestnet/:witnessType"):
             page.views.append(
                bip38_import(troute.key, troute.istestnet,troute.witnessType, page)
            )


        if page.route == "/service":     
            page.views.append(
                service_view(page, mwallet)
            )

        if page.route == "/settings":     
            page.views.append(
                settings_view(page=page)
            )


        page.update()

    """    def view_pop(view):
        page.views.pop()
        if not page.route in ['/load', '/main', '/']:
            top_view = page.views[-1]
            page.go("/")
        else:
            top_view = page.views[0]
            page.go(top_view)
        #

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)"""
  

    def view_pop(e: ViewPopEvent)-> None:
        page.views.pop()
        top_vew: View = page.views[-1]
        page.go(top_vew.route)


    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)






ft.app(main)


