import json

def test_crear_y_verificar_factura(client):
    # Crear factura
    factura_data = {
        "cliente": {
            "nombre": "Test User",
            "direccion": "Test Street",
            "identificacion": "TEST123"
        },
        "items": [
            {"descripcion": "Producto Test", "cantidad": 2, "precio_unitario": 50.0}
        ]
    }
    response = client.post("/factura", data=json.dumps(factura_data), content_type="application/json")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"

    # Buscar la factura creada (debería ser la primera, id=1)
    response = client.get("/verificar/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["cliente"]["nombre"] == "Test User"
    assert data["total"] == 100.0

def test_busqueda_avanzada(client):
    # Crear dos facturas
    for i in range(2):
        factura_data = {
            "cliente": {
                "nombre": f"Cliente {i}",
                "direccion": "Calle",
                "identificacion": f"ID{i}"
            },
            "items": [
                {"descripcion": "Prod", "cantidad": 1, "precio_unitario": 10.0 + i}
            ]
        }
        client.post("/factura", data=json.dumps(factura_data), content_type="application/json")

    # Buscar por nombre parcial
    response = client.get("/facturas?cliente_nombre=Cliente 1")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["cliente"]["nombre"] == "Cliente 1" 