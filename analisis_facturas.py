import pandas as pd
import matplotlib.pyplot as plt
from app import create_app, db
from app.services.storage import FacturaDB, ClienteDB
from sqlalchemy.orm import joinedload

# Inicializar app y contexto
app = create_app()
app.app_context().push()

# Consultar todas las facturas y clientes
facturas = db.session.query(FacturaDB).options(joinedload(FacturaDB.cliente)).all()

data = []
for f in facturas:
    total = sum(item.cantidad * item.precio_unitario for item in f.items)
    data.append({
        'id': f.id,
        'numero': f.numero,
        'fecha': f.fecha,
        'cliente': f.cliente.nombre if f.cliente else 'Desconocido',
        'total': total
    })

df = pd.DataFrame(data)

if df.empty:
    print('No hay facturas en la base de datos.')
else:
    # Total facturado por mes
    df['mes'] = pd.to_datetime(df['fecha']).dt.to_period('M')
    total_mes = df.groupby('mes')['total'].sum()
    print('Total facturado por mes:')
    print(total_mes)

    # Facturación por cliente
    total_cliente = df.groupby('cliente')['total'].sum()
    print('\nFacturación por cliente:')
    print(total_cliente)

    # Gráfico de barras por cliente
    total_cliente.sort_values(ascending=False).plot(kind='bar', figsize=(10,5), title='Facturación por Cliente')
    plt.ylabel('Total Facturado')
    plt.tight_layout()
    plt.show() 