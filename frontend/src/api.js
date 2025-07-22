import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const facturaAPI = {
  // Crear una nueva factura
  crearFactura: async (facturaData) => {
    try {
      const response = await api.post('/factura', facturaData, {
        responseType: 'blob', // Para recibir el PDF como blob
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Verificar una factura por ID
  verificarFactura: async (idFactura) => {
    try {
      const response = await api.get(`/verificar/${idFactura}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default api; 