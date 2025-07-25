from fpdf import FPDF
import qrcode
import os
import tempfile
import json
import hashlib
from app.config import Config
from app.utils.formatters import formatear_euros, formatear_fecha

def generar_hash_factura(numero, nif, fecha):
    """Genera hash de verificación para la factura"""
    hash_input = f"{numero}|{nif}|{fecha}"
    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]

def generar_pdf(factura, id_factura):
    """Genera PDF de la factura con QR de verificación"""
    # Determinar directorio según entorno
    if os.environ.get('TESTING'):
        pdf_dir = tempfile.gettempdir()
    else:
        pdf_dir = Config.FACTURAS_FOLDER
    
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"factura_{id_factura}.pdf")

    # Datos para el QR
    numero = factura.numero
    fecha = formatear_fecha(factura.fecha)
    total = factura.calcular_total() * (1 + Config.IVA_PORCENTAJE)
    nif = factura.cliente.identificacion
    url_verificacion = f"{Config.BASE_URL_VERIFICACION}{id_factura}"
    hash_factura = generar_hash_factura(numero, nif, fecha)

    # Contenido del QR según BOE-A-2023-24840
    qr_data = {
        "emisor_nif": nif,
        "numero": numero,
        "fecha": fecha,
        "total": round(total, 2),
        "hash": hash_factura,
        "verificacion": url_verificacion
    }
    qr_content = json.dumps(qr_data, ensure_ascii=False)

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Encabezado
    pdf.cell(0, 10, f"Factura N°: {factura.numero}", ln=True)
    pdf.cell(0, 10, f"Fecha: {fecha}", ln=True)
    pdf.cell(0, 10, f"Cliente: {factura.cliente.nombre}", ln=True)
    pdf.cell(0, 10, f"Identificación: {nif}", ln=True)
    pdf.cell(0, 10, f"Dirección: {factura.cliente.direccion}", ln=True)
    pdf.ln(10)

    # Tabla de ítems
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(80, 10, "Descripción", 1)
    pdf.cell(30, 10, "Cantidad", 1)
    pdf.cell(40, 10, "Precio Unitario", 1)
    pdf.cell(40, 10, "Subtotal", 1, ln=True)
    pdf.set_font("Arial", size=12)
    
    for item in factura.items:
        pdf.cell(80, 10, str(item.descripcion), 1)
        pdf.cell(30, 10, str(item.cantidad), 1)
        pdf.cell(40, 10, formatear_euros(item.precio_unitario), 1)
        pdf.cell(40, 10, formatear_euros(item.subtotal()), 1, ln=True)

    pdf.ln(5)
    
    # Cálculo de totales
    total_sin_iva = factura.calcular_total()
    iva = total_sin_iva * Config.IVA_PORCENTAJE
    total_con_iva = total_sin_iva + iva

    # Desglose de totales
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Total sin IVA:", 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, formatear_euros(total_sin_iva), ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, f"IVA ({int(Config.IVA_PORCENTAJE*100)}%):", 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, formatear_euros(iva), ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Total con IVA:", 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, formatear_euros(total_con_iva), ln=True)

    pdf.ln(10)
    
    # Leyenda de verificación
    pdf.set_font("Arial", 'I', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, f"Factura verificable en {url_verificacion}", ln=True)
    pdf.set_text_color(0, 0, 0)

    # Generar e insertar QR
    qr = qrcode.make(qr_content)
    qr_path = os.path.join(pdf_dir, f"qr_{id_factura}.png")
    qr.save(qr_path)
    pdf.image(qr_path, x=160, y=10, w=40)

    pdf.output(pdf_path)
    os.remove(qr_path)  # Limpiar archivo temporal
    return pdf_path 