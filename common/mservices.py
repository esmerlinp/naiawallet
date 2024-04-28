#* Clase de servicio, obtiene información de billeteras de la cadena de bloques.


from bitcoinlib.services.services import Service , Cache
from common.cartera import DEFAULT_DATABASE_CACHE

class MService():
    def __init__(self, network="bitcoin"):
        #super().__init__(network=network, db_uri=DEFAULT_DATABASE_CACHE)
        self.service = Service(network=network)


    def get_balance(self, address:str):
        """ Obtiene el Balance BTC /TBTC de una direccion pública
        """
        return self.service.getbalance(address) / 100000000
    
    def get_info(self) -> dict:
        """ Obtiene el Balance BTC /TBTC de una direccion pública
        """
        return self.service.getinfo()
    

    def estimate_fee(self, priority="", blocks=3):
        """
        Estimate fee per kilobyte for a transaction for this network with expected confirmation within a certain
        amount of blocks

        :param blocks: Expected confirmation time in blocks. Default is 3.
        :type blocks: int
        :param priority: Priority for transaction: can be 'low', 'medium' or 'high'. Overwrites value supplied in 'blocks' argument
        :type priority: str

        :return int: Fee in the smallest network denominator (satoshi)
        """
        return self.service.estimatefee(priority=priority, blocks=blocks)    
    
    def get_utxos(self, address:str):
        return self.service.getutxos(address)    
    

    def gettransaction(self, txid:str):
        """
        Get a transaction by its transaction hash. Convert to Bitcoinlib Transaction object.

        :param txid: Transaction identification hash
        :type txid: str

        :return Transaction: A single transaction object
        """
        trx = self.service.gettransaction(txid) 
        return self.as_dict(tx=trx)
    
    def gettransactions(self, address:str):
        """
        Get all transactions for specified address.

        Sorted from old to new, so transactions with highest number of confirmations first.

        :param address: Address string
        :type address: str
        :param after_txid: Transaction ID of last known transaction. Only check for transactions after given tx id. Default: Leave empty to return all transaction. If used only provide a single address
        :type after_txid: str
        :param limit: Maximum number of transactions to return
        :type limit: int

        :return list: List of Transaction objects
        """

        tx_obj_arr = self.service.gettransactions(address) 
        tx_arr = []
        for tx_obj in tx_obj_arr:
            tx_arr.append(self.as_dict(tx=tx_obj))
        
        return tx_arr 
    


    def as_dict(self, tx):
            """
            Return Json dictionary with transaction information: Inputs, outputs, version and locktime

            :return dict:
            """
            inputs = []
            outputs = []
            for i in tx.inputs:
                inputs.append(i.as_dict())
            for o in tx.outputs:
                outputs.append(o.as_dict())
            return {
                'txid': tx.txid,
                'date': tx.date,
                'network': tx.network.name,
                'witness_type': tx.witness_type,
                'coinbase': tx.coinbase,
                'flag': None if not tx.flag else ord(tx.flag),
                'txhash': tx.txhash,
                'confirmations': tx.confirmations,
                'block_height': tx.block_height,
                'block_hash': tx.block_hash,
                'fee': tx.fee,
                'fee_per_kb': tx.fee_per_kb,
                'inputs': inputs,
                'outputs': outputs,
                'input_total': tx.input_total,
                'output_total': tx.output_total,
                'version': tx.version_int,
                'locktime': tx.locktime,
                'raw': tx.raw_hex(),
                'size': tx.size,
                'vsize': tx.vsize,
                'verified': tx.verified,
                'status': tx.status
            }


if __name__=="__main__":
      t =MService(network="bitcoin").getinfo()
      print(t)

