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
        precio: 0
      }
    ]
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [focusedField, setFocusedField] = useState('');

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

  const getFieldHelp = (field) => {
    const helpTexts = {
      'cliente.nombre': 'Ingresa el nombre completo del cliente (ej: Juan Pérez)',
      'cliente.direccion': 'Ingresa la dirección completa del cliente (ej: Calle Mayor 123, Madrid)',
      'cliente.identificacion': 'Ingresa el DNI/NIF del cliente (ej: 12345678A)',
      'item.descripcion': 'Describe el producto o servicio (ej: Desarrollo web, Consultoría)',
      'item.cantidad': 'Número de unidades o horas del servicio',
      'item.precio': 'Precio por unidad en euros (ej: 50.00)'
    };
    return helpTexts[field] || '';
  };

  const addItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { descripcion: '', cantidad: 1, precio: 0 }]
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
        items: [{ descripcion: '', cantidad: 1, precio: 0 }]
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
      <div className="form-intro">
        <p>Completa los datos del cliente y los productos/servicios para generar la factura.</p>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="cliente-section">
          <h3>📋 Datos del Cliente</h3>
          <div className="form-group">
            <label>Nombre completo: <span className="required">*</span></label>
            <input
              type="text"
              placeholder="Ej: Juan Pérez García"
              value={formData.cliente.nombre}
              onChange={(e) => handleClienteChange('nombre', e.target.value)}
              onFocus={() => setFocusedField('cliente.nombre')}
              onBlur={() => setFocusedField('')}
              required
            />
            {focusedField === 'cliente.nombre' && (
              <div className="help-text">{getFieldHelp('cliente.nombre')}</div>
            )}
          </div>
          <div className="form-group">
            <label>Dirección completa: <span className="required">*</span></label>
            <input
              type="text"
              placeholder="Ej: Calle Mayor 123, 28001 Madrid"
              value={formData.cliente.direccion}
              onChange={(e) => handleClienteChange('direccion', e.target.value)}
              onFocus={() => setFocusedField('cliente.direccion')}
              onBlur={() => setFocusedField('')}
              required
            />
            {focusedField === 'cliente.direccion' && (
              <div className="help-text">{getFieldHelp('cliente.direccion')}</div>
            )}
          </div>
          <div className="form-group">
            <label>DNI/NIF: <span className="required">*</span></label>
            <input
              type="text"
              placeholder="Ej: 12345678A"
              value={formData.cliente.identificacion}
              onChange={(e) => handleClienteChange('identificacion', e.target.value)}
              onFocus={() => setFocusedField('cliente.identificacion')}
              onBlur={() => setFocusedField('')}
              required
            />
            {focusedField === 'cliente.identificacion' && (
              <div className="help-text">{getFieldHelp('cliente.identificacion')}</div>
            )}
          </div>
        </div>

        <div className="items-section">
          <h3>🛍️ Productos/Servicios</h3>
          <div className="items-intro">
            <p>Agrega los productos o servicios que vas a facturar. Puedes agregar múltiples ítems.</p>
          </div>
          {formData.items.map((item, index) => (
            <div key={index} className="item-row">
              <div className="item-header">
                <h4>Ítem {index + 1}</h4>
                {formData.items.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeItem(index)}
                    className="remove-btn"
                    title="Eliminar este ítem"
                  >
                    🗑️ Eliminar
                  </button>
                )}
              </div>
              <div className="form-group">
                <label>Descripción: <span className="required">*</span></label>
                <input
                  type="text"
                  placeholder="Ej: Desarrollo web, Consultoría, Producto X"
                  value={item.descripcion}
                  onChange={(e) => handleItemChange(index, 'descripcion', e.target.value)}
                  onFocus={() => setFocusedField('item.descripcion')}
                  onBlur={() => setFocusedField('')}
                  required
                />
                {focusedField === 'item.descripcion' && (
                  <div className="help-text">{getFieldHelp('item.descripcion')}</div>
                )}
              </div>
              <div className="form-group">
                <label>Cantidad: <span className="required">*</span></label>
                <input
                  type="number"
                  min="1"
                  placeholder="1"
                  value={item.cantidad}
                  onChange={(e) => handleItemChange(index, 'cantidad', parseInt(e.target.value))}
                  onFocus={() => setFocusedField('item.cantidad')}
                  onBlur={() => setFocusedField('')}
                  required
                />
                {focusedField === 'item.cantidad' && (
                  <div className="help-text">{getFieldHelp('item.cantidad')}</div>
                )}
              </div>
              <div className="form-group">
                <label>Precio por unidad (€): <span className="required">*</span></label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="0.00"
                  value={item.precio}
                  onChange={(e) => handleItemChange(index, 'precio', parseFloat(e.target.value))}
                  onFocus={() => setFocusedField('item.precio')}
                  onBlur={() => setFocusedField('')}
                  required
                />
                {focusedField === 'item.precio' && (
                  <div className="help-text">{getFieldHelp('item.precio')}</div>
                )}
                <div className="subtotal">
                  Subtotal: {(item.cantidad * item.precio).toFixed(2)} €
                </div>
              </div>
            </div>
          ))}
          <button type="button" onClick={addItem} className="add-btn">
            ➕ Agregar otro ítem
          </button>
        </div>

        <div className="total-section">
          <div className="total-calculator">
            <h4>💰 Resumen de la Factura</h4>
            <div className="total-breakdown">
              <div className="total-row">
                <span>Subtotal:</span>
                <span>{formData.items.reduce((sum, item) => sum + (item.cantidad * item.precio), 0).toFixed(2)} €</span>
              </div>
              <div className="total-row">
                <span>IVA (21%):</span>
                <span>{(formData.items.reduce((sum, item) => sum + (item.cantidad * item.precio), 0) * 0.21).toFixed(2)} €</span>
              </div>
              <div className="total-row total-final">
                <span><strong>Total:</strong></span>
                <span><strong>{(formData.items.reduce((sum, item) => sum + (item.cantidad * item.precio), 0) * 1.21).toFixed(2)} €</strong></span>
              </div>
            </div>
          </div>
        </div>

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? '🔄 Generando factura...' : '📄 Generar Factura PDF'}
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