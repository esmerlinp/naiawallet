import nfc

# Establece una conexión con el lector NFC
clf = nfc.ContactlessFrontend('usb')

def read_card(tag):
    # Obtiene el ID de la tarjeta
    id = tag.uid

    # Obtiene el tipo de la tarjeta
    nt = tag.ndef.type

    # Lee los datos de la tarjeta
    if nt == nfc.ndef.Type.NDEF:
        for record in tag.ndef.records:
            print(record.payload.decode('utf-8'))
    else:
        print('Tarjeta no compatible con NDEF')

while True:
    # Espera a que se detecte una tarjeta
    tag = clf.connect()

    # Lee la tarjeta
    if tag:
        read_card(tag)
        
