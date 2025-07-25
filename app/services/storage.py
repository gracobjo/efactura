from app import db
from app.models.factura import Factura, Cliente, Item
from datetime import datetime
from app.exceptions import StorageError, FacturaNotFoundError

# --- MODELOS SQLAlchemy ---
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import joinedload

class ClienteDB(db.Model):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    direccion = Column(String)
    identificacion = Column(String)
    facturas = relationship('FacturaDB', back_populates='cliente')

class FacturaDB(db.Model):
    __tablename__ = 'facturas'
    id = Column(Integer, primary_key=True)
    numero = Column(String, unique=True)
    fecha = Column(DateTime)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('ClienteDB', back_populates='facturas')
    items = relationship('ItemDB', back_populates='factura', cascade='all, delete-orphan')

class ItemDB(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    factura_id = Column(Integer, ForeignKey('facturas.id'))
    factura = relationship('FacturaDB', back_populates='items')

# --- FUNCIONES DE ALMACENAMIENTO ---
def guardar_factura(factura):
    """Guarda una factura en la base de datos"""
    try:
        # Guardar cliente (o buscar existente)
        cliente_db = ClienteDB.query.filter_by(identificacion=factura.cliente.identificacion).first()
        if not cliente_db:
            cliente_db = ClienteDB(
                nombre=factura.cliente.nombre,
                direccion=factura.cliente.direccion,
                identificacion=factura.cliente.identificacion
            )
            db.session.add(cliente_db)
            db.session.flush()  # Para obtener el id

        # Guardar factura
        factura_db = FacturaDB(
            numero=factura.numero,
            fecha=factura.fecha,
            cliente=cliente_db
        )
        db.session.add(factura_db)
        db.session.flush()

        # Guardar items
        for item in factura.items:
            item_db = ItemDB(
                descripcion=item.descripcion,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                factura=factura_db
            )
            db.session.add(item_db)

        db.session.commit()
        return factura_db.id
        
    except Exception as e:
        db.session.rollback()
        raise StorageError(f"Error guardando factura: {e}")

def obtener_factura(id_factura):
    """Obtiene una factura de la base de datos"""
    try:
        factura_db = db.session.get(FacturaDB, id_factura)
        if not factura_db:
            raise FacturaNotFoundError(f"Factura con ID {id_factura} no encontrada")
        
        # Reconstruir objetos de dominio
        cliente = Cliente(
            nombre=factura_db.cliente.nombre,
            direccion=factura_db.cliente.direccion,
            identificacion=factura_db.cliente.identificacion
        )
        
        items = [
            Item(
                descripcion=item.descripcion,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario
            ) for item in factura_db.items
        ]
        
        factura = Factura(
            cliente=cliente,
            items=items,
            fecha=factura_db.fecha,
            numero=factura_db.numero
        )
        
        return factura
        
    except FacturaNotFoundError:
        raise
    except Exception as e:
        raise StorageError(f"Error obteniendo factura: {e}")

def eliminar_factura(id_factura):
    """Elimina una factura de la base de datos"""
    try:
        factura_db = db.session.get(FacturaDB, id_factura)
        if not factura_db:
            raise FacturaNotFoundError(f"Factura con ID {id_factura} no encontrada")
        
        db.session.delete(factura_db)
        db.session.commit()
        
    except FacturaNotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        raise StorageError(f"Error eliminando factura: {e}")

def buscar_facturas(filtros=None):
    """Busca facturas con filtros opcionales"""
    try:
        query = db.session.query(FacturaDB).options(joinedload(FacturaDB.cliente))
        
        if filtros:
            # Aplicar filtros aquí si es necesario
            pass
        
        return query.all()
        
    except Exception as e:
        raise StorageError(f"Error buscando facturas: {e}") 