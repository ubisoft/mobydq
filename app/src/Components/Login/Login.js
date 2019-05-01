import React from 'react';
import './../../styles/baseStyles';
import '../../index.css';
import LoginForm from './LoginForm';

/**
 * Login page
 */
class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      'message': props.message ? props.message : ''
    };
  }

  render() {
    return (
      <div className="container">
        <div style={{
          'paddingTop': '60px',
          'transform': 'translateX(30%)'
        }}>
          <LoginForm message={ this.props.message } />
        </div>
      </div>
    );
  }
}

export default Login;
