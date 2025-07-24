import React, { useState } from 'react';

const FacturaMigrar = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [facturasMigradas, setFacturasMigradas] = useState([]);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
    setMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setMessage('Por favor selecciona al menos un archivo PDF');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch('http://localhost:5000/migrar-facturas', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
        setFacturasMigradas(data.facturas_migradas);
        setFiles([]);
        // Limpiar el input de archivos
        e.target.reset();
      } else {
        setMessage(`Error: ${data.message}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async (idFactura, filename) => {
    try {
      const response = await fetch(`http://localhost:5000/factura/${idFactura}/pdf`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `factura_migrada_${idFactura}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Error descargando PDF:', error);
    }
  };

  return (
    <div className="factura-migrar">
      <h2>🔄 Migrar Facturas PDF</h2>
      
      <div className="migrar-intro">
        <p>
          Sube facturas PDF existentes para convertirlas al nuevo formato electrónico 
          con código QR y cumplimiento del reglamento de facturación electrónica.
        </p>
        <ul>
          <li>✅ Soporta múltiples archivos PDF</li>
          <li>✅ Extrae automáticamente datos del cliente y totales</li>
          <li>✅ Genera nuevos PDFs con código QR</li>
          <li>✅ Cumple con el reglamento de facturación electrónica</li>
        </ul>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Seleccionar archivos PDF: <span className="required">*</span></label>
          <input
            type="file"
            multiple
            accept=".pdf"
            onChange={handleFileChange}
            required
            className="file-input"
          />
          <div className="file-info">
            {files.length > 0 && (
              <div className="selected-files">
                <h4>Archivos seleccionados ({files.length}):</h4>
                <ul>
                  {files.map((file, index) => (
                    <li key={index}>
                      📄 {file.name} ({(file.size / 1024).toFixed(1)} KB)
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        <button type="submit" disabled={loading || files.length === 0} className="submit-btn">
          {loading ? '🔄 Migrando facturas...' : '🚀 Migrar Facturas'}
        </button>
      </form>

      {message && (
        <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}

      {facturasMigradas.length > 0 && (
        <div className="facturas-migradas">
          <h3>✅ Facturas Migradas Exitosamente</h3>
          <div className="migradas-grid">
            {facturasMigradas.map((factura, index) => (
              <div key={index} className="factura-migrada-card">
                <div className="factura-header">
                  <h4>📄 {factura.archivo_original}</h4>
                  <span className="factura-id">ID: {factura.id_factura_nueva}</span>
                </div>
                <div className="factura-details">
                  <p><strong>Número:</strong> {factura.numero_factura}</p>
                  <p><strong>Total:</strong> {factura.total}</p>
                </div>
                <div className="factura-actions">
                  <button
                    onClick={() => downloadPDF(factura.id_factura_nueva, factura.archivo_original)}
                    className="download-btn"
                  >
                    📥 Descargar PDF Nuevo
                  </button>
                  <a
                    href={`http://localhost:5000/verificar/${factura.id_factura_nueva}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="verify-btn"
                  >
                    🔍 Verificar
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FacturaMigrar; 