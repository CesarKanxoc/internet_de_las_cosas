import React, { useEffect, useState } from 'react';
import socketIOClient from 'socket.io-client';

function Notifications() {
  const [stock, setStock] = useState({ mensaje: '', valor: 0 });

  useEffect(() => {
    const socket = socketIOClient('http://192.168.1.72:5000/productos_stock');  // Cambia la URL según tu configuración

    socket.on('message', (data) => {
      const { mensaje, valor } = JSON.parse(data);
      setStock({ mensaje, valor });
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div>
      <h1>Notificaciones</h1>
      {stock.mensaje ? (
        <p>{stock.mensaje}: {stock.valor}</p>
      ) : (
        <p>No hay notificaciones</p>
      )}
    </div>
  );
}

export default Notifications;