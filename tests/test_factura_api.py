import json

def test_crear_y_verificar_factura(client):
    # Crear factura
    factura_data = {
        "cliente": {
            "nombre": "Test User",
            "direccion": "Test Street",
            "identificacion": "TEST12345"
        },
        "items": [
            {"descripcion": "Producto Test", "cantidad": 2, "precio": 50.0}
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
    assert "100,00 EUR" in data["total"]

def test_busqueda_avanzada(client):
    # Crear dos facturas
    for i in range(2):
        factura_data = {
            "cliente": {
                "nombre": f"Cliente {i}",
                "direccion": "Calle",
                "identificacion": f"ID{i}12345"
            },
            "items": [
                {"descripcion": "Prod", "cantidad": 1, "precio": 10.0 + i}
            ]
        }
        client.post("/factura", data=json.dumps(factura_data), content_type="application/json")

    # Buscar por nombre parcial
    response = client.get("/facturas?cliente_nombre=Cliente 1")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["cliente"]["nombre"] == "Cliente 1"

def test_crear_factura_datos_faltantes(client):
    # Test sin datos de cliente
    factura_data = {
        "items": [
            {"descripcion": "Producto", "cantidad": 1, "precio": 10.0}
        ]
    }
    response = client.post("/factura", data=json.dumps(factura_data), content_type="application/json")
    assert response.status_code == 400
    assert "Datos del cliente requeridos" in response.get_json()["message"]

    # Test sin items
    factura_data = {
        "cliente": {
            "nombre": "Test",
            "direccion": "Test",
            "identificacion": "TEST12345"
        }
    }
    response = client.post("/factura", data=json.dumps(factura_data), content_type="application/json")
    assert response.status_code == 400
    assert "Lista de items requerida" in response.get_json()["message"]

def test_verificar_factura_no_existe(client):
    response = client.get("/verificar/999")
    assert response.status_code == 404
    assert "no encontrada" in response.get_json()["message"]

def test_busqueda_con_filtros_avanzados(client):
    # Crear factura para testing
    factura_data = {
        "cliente": {
            "nombre": "Cliente Filtro",
            "direccion": "Dirección",
            "identificacion": "FILTRO12345"
        },
        "items": [
            {"descripcion": "Producto", "cantidad": 1, "precio": 100.0}
        ]
    }
    client.post("/factura", data=json.dumps(factura_data), content_type="application/json")

    # Test filtro por identificación
    response = client.get("/facturas?cliente_identificacion=FILTRO12345")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["cliente"]["identificacion"] == "FILTRO12345"

def test_descargar_pdf_factura(client):
    # Crear factura primero
    factura_data = {
        "cliente": {
            "nombre": "Test PDF",
            "direccion": "Test Address",
            "identificacion": "PDF12345"
        },
        "items": [
            {"descripcion": "Producto PDF", "cantidad": 1, "precio": 25.0}
        ]
    }
    client.post("/factura", data=json.dumps(factura_data), content_type="application/json")

    # Descargar PDF
    response = client.get("/factura/1/pdf")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"

def test_descargar_pdf_factura_no_existe(client):
    response = client.get("/factura/999/pdf")
    assert response.status_code == 404

def test_eliminar_factura(client):
    # Crear factura primero
    factura_data = {
        "cliente": {
            "nombre": "Test Delete",
            "direccion": "Test Address",
            "identificacion": "DEL12345"
        },
        "items": [
            {"descripcion": "Producto Delete", "cantidad": 1, "precio": 30.0}
        ]
    }
    client.post("/factura", data=json.dumps(factura_data), content_type="application/json")

    # Eliminar factura
    response = client.delete("/factura/1")
    assert response.status_code == 200
    assert "eliminada correctamente" in response.get_json()["message"]

def test_eliminar_factura_no_existe(client):
    response = client.delete("/factura/999")
    assert response.status_code == 404 