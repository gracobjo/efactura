from fpdf import FPDF
import qrcode
import os

IVA_PORCENTAJE = 0.21  # 21% de IVA

BASE_URL_VERIFICACION = "http://localhost:5000/verificar/"  # Cambia según despliegue


def generar_pdf(factura, id_factura):
    pdf_dir = os.path.join(os.getcwd(), 'instance', 'facturas')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"factura_{id_factura}.pdf")

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Datos del cliente
    pdf.cell(0, 10, f"Factura N°: {factura.numero}", ln=True)
    pdf.cell(0, 10, f"Fecha: {factura.fecha.strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(0, 10, f"Cliente: {factura.cliente.nombre}", ln=True)
    pdf.cell(0, 10, f"Identificación: {factura.cliente.identificacion}", ln=True)
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
        pdf.cell(40, 10, f"{item.precio_unitario:.2f}", 1)
        pdf.cell(40, 10, f"{item.subtotal():.2f}", 1, ln=True)

    pdf.ln(5)
    total = factura.calcular_total()
    iva = total * IVA_PORCENTAJE
    total_con_iva = total + iva
    pdf.cell(0, 10, f"IVA ({int(IVA_PORCENTAJE*100)}%): {iva:.2f}", ln=True)
    pdf.cell(0, 10, f"Total: {total_con_iva:.2f}", ln=True)

    # Generar código QR
    url_verificacion = f"{BASE_URL_VERIFICACION}{id_factura}"
    qr = qrcode.make(url_verificacion)
    qr_path = os.path.join(pdf_dir, f"qr_{id_factura}.png")
    qr.save(qr_path)

    # Insertar QR en el PDF
    pdf.image(qr_path, x=160, y=10, w=40)

    pdf.output(pdf_path)
    os.remove(qr_path)
    return pdf_path 