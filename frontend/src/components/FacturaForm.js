import React, { useState } from 'react';
import { facturaAPI } from '../api';

const FacturaForm = () => {
  const [formData, setFormData] = useState({
    cliente: {
      nombre: '',
      direccion: '',
      identificacion: ''
    },
    items: [
      {
        descripcion: '',
        cantidad: 1,
        precio_unitario: 0
      }
    ]
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleClienteChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      cliente: {
        ...prev.cliente,
        [field]: value
      }
    }));
  };

  const handleItemChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const addItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { descripcion: '', cantidad: 1, precio_unitario: 0 }]
    }));
  };

  const removeItem = (index) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const pdfBlob = await facturaAPI.crearFactura(formData);
      
      // Crear URL para descargar el PDF
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'factura.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setMessage('¡Factura creada exitosamente! El PDF se ha descargado.');
      setFormData({
        cliente: { nombre: '', direccion: '', identificacion: '' },
        items: [{ descripcion: '', cantidad: 1, precio_unitario: 0 }]
      });
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || 'Error al crear la factura'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="factura-form">
      <h2>Crear Nueva Factura</h2>
      <form onSubmit={handleSubmit}>
        <div className="cliente-section">
          <h3>Datos del Cliente</h3>
          <div className="form-group">
            <label>Nombre:</label>
            <input
              type="text"
              value={formData.cliente.nombre}
              onChange={(e) => handleClienteChange('nombre', e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Dirección:</label>
            <input
              type="text"
              value={formData.cliente.direccion}
              onChange={(e) => handleClienteChange('direccion', e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Identificación:</label>
            <input
              type="text"
              value={formData.cliente.identificacion}
              onChange={(e) => handleClienteChange('identificacion', e.target.value)}
              required
            />
          </div>
        </div>

        <div className="items-section">
          <h3>Ítems de la Factura</h3>
          {formData.items.map((item, index) => (
            <div key={index} className="item-row">
              <div className="form-group">
                <label>Descripción:</label>
                <input
                  type="text"
                  value={item.descripcion}
                  onChange={(e) => handleItemChange(index, 'descripcion', e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Cantidad:</label>
                <input
                  type="number"
                  min="1"
                  value={item.cantidad}
                  onChange={(e) => handleItemChange(index, 'cantidad', parseInt(e.target.value))}
                  required
                />
              </div>
              <div className="form-group">
                <label>Precio Unitario:</label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={item.precio_unitario}
                  onChange={(e) => handleItemChange(index, 'precio_unitario', parseFloat(e.target.value))}
                  required
                />
              </div>
              {formData.items.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeItem(index)}
                  className="remove-btn"
                >
                  Eliminar
                </button>
              )}
            </div>
          ))}
          <button type="button" onClick={addItem} className="add-btn">
            Agregar Ítem
          </button>
        </div>

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Creando...' : 'Crear Factura'}
        </button>
      </form>

      {message && (
        <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default FacturaForm; 