from app.models.factura import Cliente, Item, Factura

def test_item_subtotal():
    item = Item("Test", 3, 10.0)
    assert item.subtotal() == 30.0

def test_factura_total():
    cliente = Cliente("A", "B", "C")
    items = [Item("X", 2, 5.0), Item("Y", 1, 10.0)]
    factura = Factura(cliente, items)
    assert factura.calcular_total() == 20.0 