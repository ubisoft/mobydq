import React from 'react';
import './../../styles/baseStyles';
import '../../index.css';
import Button from '@material-ui/core/Button';
import UrlBuilder from '../Base/UrlBuilder';

const googleOAuthUrl = UrlBuilder.getDefault().googleOAuth();

const Login = () => <React.Fragment>
  <div className="container">
    <div className="loginForm">
      <div className="loginFormHeader">
        <table>
          <tbody>
            <tr>
              <td>
                <div className="btnCloseFake" />
              </td>
              <td>
                <div className="btnMinimizeFake" />
              </td>
              <td>
                <div className="btnMaximizeFake" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div style={{ 'textAlign': 'center' }}>
        <a style={{ 'textDecoration': 'none' }} href={googleOAuthUrl}>
          <Button style={{ 'marginTop': '25%' }} variant="contained" color="secondary">
            Sign in with Google
          </Button>
        </a>
      </div>
    </div>
  </div>
</React.Fragment>;

export default Login;
