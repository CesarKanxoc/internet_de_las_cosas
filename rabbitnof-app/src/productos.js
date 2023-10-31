import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ProductStock() {
  const [stock, setStock] = useState(0);

  useEffect(() => {
    // Realiza una solicitud HTTP para obtener el stock inicial
    axios.get('http://192.168.213.87:5000/productos_stock')
      .then((response) => {
        setStock(response.data.producto_stock);
      })
      .catch((error) => {
        console.error('Error al obtener el stock: ' + error);
      });
  }, []);

  // Función para actualizar el stock
  const actualizarStock = () => {
    axios.post('http://192.168.213.87:5000/actualizar_stock')
      .then((response) => {
        if (response.data.success) {
          setStock(response.data.nuevo_stock);
          console.log('Stock actualizado exitosamente.');
        } else {
          console.error('Error al actualizar el stock: No se pudo obtener la notificación.');

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
