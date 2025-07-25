import React, { useState } from 'react';
import FacturaForm from './components/FacturaForm';
import FacturaVerificar from './components/FacturaVerificar';
import FacturaMigrar from './components/FacturaMigrar';
import AccessibilityTest from './components/AccessibilityTest';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('crear');

  const handleKeyDown = (e) => {
    const tabs = ['crear', 'verificar', 'migrar'];
    const currentIndex = tabs.indexOf(activeTab);
    
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        const nextIndex = (currentIndex + 1) % tabs.length;
        setActiveTab(tabs[nextIndex]);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        const prevIndex = currentIndex === 0 ? tabs.length - 1 : currentIndex - 1;
        setActiveTab(tabs[prevIndex]);
        break;
      case 'Home':
        e.preventDefault();
        setActiveTab(tabs[0]);
        break;
      case 'End':
        e.preventDefault();
        setActiveTab(tabs[tabs.length - 1]);
        break;
      default:
        break;
    }
  };

  return (
    <div className="App">
      <AccessibilityTest />
      <header className="App-header">
        <h1>eFactura - Sistema de Facturación Electrónica</h1>
      </header>
      
      <nav className="nav-tabs" role="tablist" aria-label="Navegación principal de eFactura" onKeyDown={handleKeyDown}>
        <button 
          className={`tab ${activeTab === 'crear' ? 'active' : ''}`}
          onClick={() => setActiveTab('crear')}
          role="tab"
          aria-selected={activeTab === 'crear'}
          aria-controls="panel-crear"
          id="tab-crear"
          tabIndex={0}
        >
          Crear Factura
        </button>
        <button 
          className={`tab ${activeTab === 'verificar' ? 'active' : ''}`}
          onClick={() => setActiveTab('verificar')}
          role="tab"
          aria-selected={activeTab === 'verificar'}
          aria-controls="panel-verificar"
          id="tab-verificar"
          tabIndex={0}
        >
          Verificar Factura
        </button>
        <button 
          className={`tab ${activeTab === 'migrar' ? 'active' : ''}`}
          onClick={() => setActiveTab('migrar')}
          role="tab"
          aria-selected={activeTab === 'migrar'}
          aria-controls="panel-migrar"
          id="tab-migrar"
          tabIndex={0}
        >
          Migrar PDFs
        </button>
      </nav>

      <main className="main-content" role="main">
        <div 
          id="panel-crear" 
          role="tabpanel" 
          aria-labelledby="tab-crear"
          hidden={activeTab !== 'crear'}
        >
          {activeTab === 'crear' && <FacturaForm />}
        </div>
        <div 
          id="panel-verificar" 
          role="tabpanel" 
          aria-labelledby="tab-verificar"
          hidden={activeTab !== 'verificar'}
        >
          {activeTab === 'verificar' && <FacturaVerificar />}
        </div>
        <div 
          id="panel-migrar" 
          role="tabpanel" 
          aria-labelledby="tab-migrar"
          hidden={activeTab !== 'migrar'}
        >
          {activeTab === 'migrar' && <FacturaMigrar />}
        </div>
      </main>

      <footer className="App-footer">
        <p>eFactura - API REST con Flask y Frontend React</p>
      </footer>
    </div>
  );
}

export default App; 