import qrcode
from PIL import Image

data = "This is some text to be encoded in the QR code."

def generar_codigo_qr(data, name="qr_code.png"):
    qr = qrcode.QRCode(
        version=1,  # Adjust version for complexity (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level (L, M, Q, H)
        box_size=10,  # Size of each box in pixels
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(name)

#generar_codigo_qr("This is some text to be encoded in the QR code.", "qr_code2.png")