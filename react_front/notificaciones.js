import React, { useEffect, useState } from 'react';
import socketIOClient from 'socket.io-client';

function Notifications() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const socket = socketIOClient('http://127.0.0.1:5000/productos_stock');  // Cambia la URL según tu configuración

    socket.on('message', (data) => {
      setMessage(data);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div>
      <h1>Notificaciones</h1>
      <p>{message}</p>
    </div>
  );
}

export default Notifications;