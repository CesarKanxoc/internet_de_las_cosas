import React from 'react';
import './App.css';
import ProductStock from './producto';
import Notifications from './notificaciones';

function App() {
  return (
    <div className="App">
      <ProductStock />
      <Notifications />
    </div>
  );
}

export default App;