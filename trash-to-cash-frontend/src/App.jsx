import React from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import './App.css';
import binImage from './assets/bin.png'; // make sure the image is here

function App() {
  return (
    <div className="container">
      <div className="left-panel">
        <h1>Trash to Cash</h1>
        <p>Recycle your waste. Earn rewards.<br />Save the planet.</p>
        <div className="trash-alone">
          <img src={binImage} alt="Recycle Bin" className="trash-image" />
        </div>
      </div>

      <div className="right-panel">
        <h2>Authentication</h2>
        <div className="forms">
          <div className="form-card">
            <LoginForm />
          </div>
          <div className="form-card">
            <RegisterForm />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
