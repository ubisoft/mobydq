import React from 'react';
import './../../styles/baseStyles';
import '../../index.css';
import LoginForm from './LoginForm';

const Login = () => <React.Fragment>
  <div className="container">
    <div style={{ 'paddingTop': '55px' }}>
      <LoginForm/>
    </div>
  </div>
</React.Fragment>

export default Login;
