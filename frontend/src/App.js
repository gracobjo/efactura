import React, { useState } from 'react';
import FacturaForm from './components/FacturaForm';
import FacturaVerificar from './components/FacturaVerificar';
import FacturaMigrar from './components/FacturaMigrar';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('crear');

  return (
    <div className="App">
      <header className="App-header">
        <h1>eFactura - Sistema de Facturación Electrónica</h1>
      </header>
      
      <nav className="nav-tabs">
        <button 
          className={`tab ${activeTab === 'crear' ? 'active' : ''}`}
          onClick={() => setActiveTab('crear')}
        >
          Crear Factura
        </button>
        <button 
          className={`tab ${activeTab === 'verificar' ? 'active' : ''}`}
          onClick={() => setActiveTab('verificar')}
        >
          Verificar Factura
        </button>
        <button 
          className={`tab ${activeTab === 'migrar' ? 'active' : ''}`}
          onClick={() => setActiveTab('migrar')}
        >
          Migrar PDFs
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'crear' && <FacturaForm />}
        {activeTab === 'verificar' && <FacturaVerificar />}
        {activeTab === 'migrar' && <FacturaMigrar />}
      </main>

      <footer className="App-footer">
        <p>eFactura - API REST con Flask y Frontend React</p>
      </footer>
    </div>
  );
}

export default App; 