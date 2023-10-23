import React, { useEffect, useState } from 'react';
import socketIOClient from 'socket.io-client';
import axios from 'axios';

function ProductStock() {
  const [stock, setStock] = useState(0);

  useEffect(() => {
    const socket = socketIOClient('http://192.168.1.74:8080/productos_stock');

    socket.on('connect', () => {
      console.log('Conectado al servidor de actualizaciones');
    });

    socket.on('stock_updated', (newStock) => {
      setStock(newStock);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // Función para actualizar el stock (simulación)
  const actualizarStock = () => {
    axios.post('http://192.168.1.74:8080/actualizar_stock')
      .then((response) => {
        if (response.data.success) {
          console.log('Stock actualizado exitosamente.');
        }
      })
      .catch((error) => {
        console.error('Error al actualizar el stock: ' + error);
      });
  };

  return (
    <div>
      <h1>Stock de productos</h1>
      <p>Stock actual: {stock}</p>
      <button onClick={actualizarStock}>Actualizar Stock</button>
    </div>
  );
}

export default ProductStock;