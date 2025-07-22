from app import create_app, db
from app.models.factura import Cliente, Item, Factura
from app.services import storage

app = create_app()
app.app_context().push()

# Ejemplo de clientes e ítems
def poblar():
    clientes = [
        Cliente("Juan Pérez", "Calle Falsa 123", "12345678A"),
        Cliente("Ana Gómez", "Av. Siempre Viva 742", "87654321B"),
    ]

    facturas = [
        Factura(
            cliente=clientes[0],
            items=[
                Item("Producto A", 2, 100.0),
                Item("Producto B", 1, 50.0)
            ]
        ),
        Factura(
            cliente=clientes[1],
            items=[
                Item("Servicio X", 3, 200.0),
                Item("Producto C", 5, 20.0)
            ]
        ),
        Factura(
            cliente=clientes[0],
            items=[
                Item("Producto D", 1, 300.0)
            ]
        ),
    ]

    for factura in facturas:
        storage.guardar_factura(factura)

    print("Base de datos poblada con datos de ejemplo.")

if __name__ == "__main__":
    poblar() 