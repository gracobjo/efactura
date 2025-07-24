import React, { useState } from 'react';
import { facturaAPI } from '../api';

const FacturaVerificar = () => {
  const [idFactura, setIdFactura] = useState('');
  const [factura, setFactura] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!idFactura.trim()) {
      setError('Por favor ingresa un ID de factura');
      return;
    }

    setLoading(true);
    setError('');
    setFactura(null);

    try {
      const data = await facturaAPI.verificarFactura(idFactura);
      setFactura(data);
    } catch (error) {
      setError(error.response?.data?.message || 'Error al verificar la factura');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="factura-verificar">
      <h2>Verificar Factura</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>ID de Factura:</label>
          <input
            type="text"
            value={idFactura}
            onChange={(e) => setIdFactura(e.target.value)}
            placeholder="Ingresa el ID de la factura"
            required
          />
        </div>
        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Verificando...' : 'Verificar'}
        </button>
      </form>

      {error && (
        <div className="message error">
          {error}
        </div>
      )}

      {factura && (
        <div className="factura-info">
          <h3>Información de la Factura</h3>
          <div className="info-grid">
            <div className="info-item">
              <strong>Número:</strong> {factura.numero}
            </div>
            <div className="info-item">
              <strong>Fecha:</strong> {factura.fecha}
            </div>
            <div className="info-item">
              <strong>Cliente:</strong> {factura.cliente.nombre}
            </div>
            <div className="info-item">
              <strong>Identificación:</strong> {factura.cliente.identificacion}
            </div>
            <div className="info-item">
              <strong>Total:</strong> {factura.total}
            </div>
            <div className="info-item">
              <strong>IVA:</strong> {factura.iva}
            </div>
            <div className="info-item">
              <strong>Total con IVA:</strong> {factura.total_con_iva}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FacturaVerificar; 