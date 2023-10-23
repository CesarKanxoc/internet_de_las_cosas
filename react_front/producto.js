import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ProductStock() {
  const [stock, setStock] = useState(0);

  useEffect(() => {
    axios.get('/productos_stock')  // Cambia la URL según tu configuración
      .then((response) => {
        setStock(response.data.producto_stock);
      })
      .catch((error) => {
        console.error('Error al obtener el stock: ' + error);
      });
  }, []);

  return (
    <div>
      <h1>Stock de productos</h1>
      <p>Stock actual: {stock}</p>
    </div>
  );
}

export default ProductStock;