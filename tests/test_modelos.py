from app.models.factura import Cliente, Item, Factura

def test_item_subtotal():
    item = Item("Test", 3, 10.0)
    assert item.subtotal() == 30.0

def test_factura_total():
    cliente = Cliente("A", "B", "C")
    items = [Item("X", 2, 5.0), Item("Y", 1, 10.0)]
    factura = Factura(cliente, items)
    assert factura.calcular_total() == 20.0

def test_factura_generar_numero():
    cliente = Cliente("Test", "Address", "ID123")
    items = [Item("Product", 1, 10.0)]
    factura = Factura(cliente, items)
    assert factura.numero.startswith("FAC-")
    assert len(factura.numero) > 10

def test_factura_exportar_a_pdf():
    cliente = Cliente("Test", "Address", "ID123")
    items = [Item("Product", 1, 10.0)]
    factura = Factura(cliente, items)
    
    # El método exportar_a_pdf debe lanzar NotImplementedError
    try:
        factura.exportar_a_pdf("test.pdf")
        assert False, "Debería haber lanzado NotImplementedError"
    except NotImplementedError:
        assert True

def test_cliente_attributes():
    cliente = Cliente("Juan Pérez", "Calle 123", "12345678A")
    assert cliente.nombre == "Juan Pérez"
    assert cliente.direccion == "Calle 123"
    assert cliente.identificacion == "12345678A"

def test_item_attributes():
    item = Item("Producto Test", 5, 25.50)
    assert item.descripcion == "Producto Test"
    assert item.cantidad == 5
    assert item.precio_unitario == 25.50
    assert item.subtotal() == 127.50 