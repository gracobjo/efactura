import React, { useState } from 'react';
import FacturaForm from './components/FacturaForm';
import FacturaVerificar from './components/FacturaVerificar';
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
      </nav>

      <main className="main-content">
        {activeTab === 'crear' && <FacturaForm />}
        {activeTab === 'verificar' && <FacturaVerificar />}
      </main>

      <footer className="App-footer">
        <p>eFactura - API REST con Flask y Frontend React</p>
      </footer>
    </div>
  );
}

export default App; 