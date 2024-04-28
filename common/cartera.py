from bitcoinlib.wallets import wallet_delete_if_exists, wallet_create_or_open, wallet_exists, Wallet, WalletError
from bitcoinlib.keys import HDKey, Key, get_key_format, BKeyError
from bitcoinlib.services.mempool import MempoolClient
import string, json
#from mcode import generar_codigo_qr
import requests, json, time, threading
from enum import Enum





DEFAULT_DATABASE = "./common/bitcoinlib.sqlite"
DEFAULT_DATABASE_CACHE = "./common/bitcoinlib_cache.sqlite"
db_password="None"

URL_BTC_PRICE = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
URL_MEMPOOL_API = "https://mempool.space/api/"
NETWORK = "bitcoin"

def wallet_existe(wallet, db_uri=None, db_password=None):
    return wallet_exists(wallet, db_uri=None, db_password=None)


def cal_time(function):
    #por conversion se le coloca de nombre wrapper a la funcion anidada aunque no es obligatorio
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        stop = time.time() - start
        print('ended in :', stop)
        return result
    
    return wrapper

def btc_price():
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
    data = json.loads(response.text)
    return float(data['bpi']['USD']['rate'].replace(",", ""))

async def btc_price_control(saldo: float) -> str:
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
    data = json.loads(response.text)
    rate = float(data['bpi']['USD']['rate'].replace(",", ""))
    text ='{:.2f} USD'.format(float(saldo * rate))
    return text

class KeyFormat(Enum):
        bip38 = "wif_protected"
        bip39 = "mnemonic"
        address = "address"
        hdkey_private = "hdkey_private"
        hdkey_public ="hdkey_public"
        wif_compressed = "wif_compressed"

        
class Cartera(Wallet):
    """
    Esta clase representa la cartera del usuario.
    Permite realizar transaciones, consultar balance, crear o importar nuevas carteras
    
    """
 
    @cal_time
    def __init__(self, name= "bitcoin", network="bitcoin", witness_type="segwit", keys=None, passwd= None):
        """
        Crea o importa una nueva cartera bitcoin.
        Nota:  Direcciones legacy no soportadas.

        :param name: especifica el nombre de la cartera, por defecto la principal es bitcoin.
        :type  name: str

        :param network: indica la red  puede ser bitcoin o testnet.
        :type  network: str.

        :param witness_type: tipo de dirección puedes elegir entre segwit ó  p2sh-segwit. Defecto es segwit.
        :type  witness_type: str

        :param keys: si vas a importar/recuperar una billetera, indica la frase semilla, clave bip38, address, clave publica xpub o privada xprv. Si es None crea una nueva billetera.
        :type  keys: str.

        :param passwd: si la keys es bip38 debe indicar la password de desencriptado.
        :type  passwd: str.
        """
        if keys:
            print(network)
            try:
                passphrases = keys
                format_key_obj = get_key_format(keys)
                key_format = format_key_obj["format"]

                if key_format == KeyFormat.bip38.value:
                    encrypted_private_key = keys
                    witness_type = None
                    k = Key(import_key=encrypted_private_key, password=passwd, network=network)
                    passphrases = k.wif()


                wallet_create_or_open(name, 
                            keys=passphrases, 
                            network=network, 
                            witness_type=witness_type, 
                            db_uri=DEFAULT_DATABASE, 
                            db_cache_uri=DEFAULT_DATABASE_CACHE
                        )
                self.scan()
 
            except BKeyError as e:
                raise e
            except WalletError as e:
                raise e
                
        else:
            super().__init__(wallet="bitcoin", db_uri=DEFAULT_DATABASE, db_cache_uri=DEFAULT_DATABASE_CACHE)    
            self.scan()
   
        self.running = False
        self.bloque_actual = 0
        self.callback = None
        

    @property
    def format_key(self):
        """
        Obtiene el formato  de una key.
        """
        format_key_obj = get_key_format(self.addresslist()[0])
        return f"{format_key_obj['format']} witness_type: {format_key_obj['witness_types']}"


    @property
    def saldo(self):
        return self.balance(as_string=True)
    
    @property
    def network_name(self):
        return self.networks(as_dict=True)[0]['name']
    
    @property
    def btc_usd(self):
        response = requests.get(URL_BTC_PRICE)
        data = json.loads(response.text)
        btc_usd = data['bpi']['USD']['rate']
        return btc_usd
    
    @property
    def btc_usd_float(self):
        response = requests.get(URL_BTC_PRICE)
        data = json.loads(response.text)
        btc_usd_float = data['bpi']['USD']['rate_float']
        return btc_usd_float
    
    def estimatefee(self, blocks=3)->int:
        mempool = MempoolClient(network=NETWORK, base_url=URL_MEMPOOL_API, denominator=1)
        fee = mempool.estimatefee(blocks)
        return int(fee)
    

    def start_background_task(self, callback):
        """Inicia tareas en backgroud"""
        self.running = True
        self.callback = callback
        thread = threading.Thread(target=self.background_task)
        thread.daemon = True
        thread.start()

    def background_task(self, time_secons = 20): 
        """Mantiene balances actualizados de la mempool en un hilo separado"""  
        while self.running:
            #Obtiene Balance en usd de un btc

            response = requests.get(URL_BTC_PRICE)
            data = json.loads(response.text)
            btc_usd_float = data['bpi']['USD']['rate_float']
            btc_usd = data['bpi']['USD']['rate']

            #MEMPOOL DATA
            mempool = MempoolClient(network=NETWORK, base_url=URL_MEMPOOL_API, denominator=1)
            estimates = mempool.compose_request('v1/fees', 'recommended')
            fee_rate = {"high": estimates['fastestFee'], "medium": estimates['halfHourFee'], "low": estimates['hourFee'], "minimum": estimates['minimumFee']}
            bloque_actual = mempool.blockcount()
            self.callback(
                btc_usd= btc_usd, 
                btc_usd_float= btc_usd_float,  
                bloque_actual= bloque_actual,
                rate_high =  estimates['fastestFee'],
                rate_medium =  estimates['halfHourFee'],
                rate_low =  estimates['hourFee'],
                rate_min =  estimates['minimumFee'],
            )
            time.sleep(time_secons)

   
    def stop_background_task(self):
        """Detiene tareas en backgroud"""
        self.page = None
        self.running = False


    @classmethod
    def encrypt_passphrase(passphrase, desplazamiento):
        if not passphrase is None:
            abc = string.ascii_lowercase
            lenght = len(abc)

            passphrase_arr = passphrase.split()
            passphrase_encrypt = []
            for palabra in passphrase_arr:
                word_endrypt = []
                #si el desplazamiento excede la longito del abecedario lo hace hacia atras.
                for letter in palabra:
                    if (desplazamiento + abc.index(letter)) > lenght:
                        word_endrypt.append(abc[abc.index(letter) - desplazamiento])
                        
                    else:
                        word_endrypt.append(abc[abc.index(letter) + desplazamiento])
            

                #print("".join(passphrase_encrypt))  
                passphrase_encrypt.append("".join(word_endrypt))

            return " ".join(passphrase_encrypt)
        else:
            return None
            
    @classmethod 
    def desencrypt_passphrase(passphrase, desplazamiento):
        if not passphrase is None:
            abc = string.ascii_lowercase
            lenght = len(abc) -1

            passphrase_arr = passphrase.split()
            passphrase_encrypt = []
            for palabra in passphrase_arr:
                word_endrypt = []
                #si el desplazamiento excede la longito del abecedario lo hace hacia atras.
                for letter in palabra:
                    
                    if (desplazamiento + abc.index(letter)) == lenght:
                        indice = abs(desplazamiento + abc.index(letter))
                        word_endrypt.append(abc[indice])
                        print()
                        
                    else:
                        print(abs(desplazamiento - abc.index(letter)))
                        indice = abs(desplazamiento - abc.index(letter))
                        word_endrypt.append(abc[indice])
            

                
                passphrase_encrypt.append("".join(word_endrypt))
            
            return " ".join(passphrase_encrypt)
        else:
            return None
   
    @classmethod    
    def num_encrypt_passphrase(passphrase, desplazamiento):
        if not passphrase is None:
            abc = string.ascii_lowercase
            lenght = len(abc)
            desplazamiento = desplazamiento + 1
            passphrase_arr = passphrase.split()
            passphrase_encrypt = []
            for palabra in passphrase_arr:
                word_endrypt = []
                #si el desplazamiento excede la longito del abecedario lo hace hacia atras.
                for letter in palabra:
                    num = abc.index(letter) + desplazamiento
                    if num < 10:
                        str_num = f'0{num}'
                        word_endrypt.append(str_num)
                    else:
                        str_num = f'{num}'
                        word_endrypt.append(str_num)

            

                #print("".join(passphrase_encrypt))  
                passphrase_encrypt.append("".join(word_endrypt))

            return " ".join(passphrase_encrypt)
        else:
            return None 
   
    @classmethod
    def num_desencrypt_passphrase(passphrase, desplazamiento):
        if not passphrase is None:
            abc = string.ascii_lowercase
            #lenght = len(abc) -1
            desplazamiento = desplazamiento + 1

            passphrase_arr = passphrase.split()
            passphrase_encrypt = []
            for palabra in passphrase_arr:
                word_endrypt = []
                #si el desplazamiento excede la longito del abecedario lo hace hacia atras.
                #for letter in palabra:
                for i in range(0, len(palabra), 2):
                    dos_caracteres = palabra[i:i+2]
                    print(dos_caracteres)        
                    
                    indice =   int(dos_caracteres) - desplazamiento
                    word_endrypt.append(abc[indice])
            

                
                passphrase_encrypt.append("".join(word_endrypt))
            
            return " ".join(passphrase_encrypt)
        else:
            return None       

    

if __name__=="__main__":
    w = Cartera()
    def callback(**kargs):
        print(kargs)


    w.start_background_task(callback=callback)

    time.sleep(90)

    #ekey="6PYSe3MbZz92MoaVpGkFYKysHCdq4HhuLga2miDcabHJPMoQscAFcYULnW"
    #passws = "LA8DFLQ4EDXA"
    #to = "2MzfRKesV4qfoyLvvn3Nu3ivuWYAKw6R5WB"
    #monto = 0.0001
    #trx = send_btc(ekey, passws, to, monto, network="testnet", offline=True)
    #print(trx)  

"""--------------------------------------------------------------------------------------------------------------------------------------------
Address:                 2MuH1mUwkgaxM8A2MubLTijWjrrgsx74mSY
Extended Private Key:             uprv8tXDerPXZ1QsWBrN8ecwLigCFPbfQi1UCzZHYrJQm4528V1tx9BT69nfmiqD5K8n53ZgT63nZB6ewXFxgjcvYv6q4CMSvu2WmgjjMrhNcj1
Extended Public Key:              upub5EpxsEqThiZ1UBDuQYL5e4hTuPoXi1jNGAgfrK6aQvDEKstpNwY5D6NX7wfL9FL1tm63kXLrpLsHhivUYFY8mPiRsvzjWfp93jKFNrfPMzQ
BIP38 Encrypted WIF: 6PYVzf1Df2Qb9e7GxRhxaV3HXUpQ9RYXxsy5moDSTbCXqW2kJSdB9xorVH
BIP38 Encrypted PASS: D6PWKIN6H1FM
BIP38 Decrypted WIF: uprv94bya7mj1uyyPKHGCnHH68ixkkUb
--------------------------------------------------------------------------------------------------------------------------------------------"""
