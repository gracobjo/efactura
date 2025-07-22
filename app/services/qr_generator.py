import qrcode
import os

def generar_qr(id_factura, output_dir=None):
    base_url = "https://miapp.com/verificar/"
    url = f"{base_url}{id_factura}"
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), 'instance', 'facturas')
    os.makedirs(output_dir, exist_ok=True)
    qr_path = os.path.join(output_dir, f"qr_{id_factura}.png")
    qr = qrcode.make(url)
    qr.save(qr_path)
    return qr_path 