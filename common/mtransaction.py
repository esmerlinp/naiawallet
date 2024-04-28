from bitcoinlib.transactions import Transaction, Input, Output
from bitcoinlib.keys import Key, HDKey
from bitcoinlib.wallets import WalletTransaction

def create():
    txid = "8105d5ad3132389b1a6d8e4aa6a3d649f625645579b1812b9dbe56e46ca70eab"
    vout=1
    address = "2NAYqQuLbKLcLaGqPAijehMeUuAvMvN5wab"
 
    input_arr = [Input(prev_txid=txid, output_n=vout, network="testnet")]
    output_arr = [Output(value=100, address=address, network="testnet")]
   
    #add inputs
    tx = Transaction(inputs=input_arr, outputs=output_arr, network="testnet")
    k = HDKey("uprv94bya7mj1uyyRwtf9d1Hptyq2o8MNb8ht6Mm1fh4fcqp47kRbeSyFCVwHa9Y6N3QPvT4KVwtFSsMikup3D9MwJJjvjv5tbc4fZbr6u1u4n7",  network="testnet")
    tx.sign(keys=k)
    tx.fee_per_kb = 50
    fee = tx.calculate_fee()
    tx.estimate_size()
    print(tx.as_json())
    #print(tx.as_dict())
   
if __name__=="__main__":
    create()