import React from 'react';
import './../../styles/baseStyles';
import '../../index.css';
import LoginForm from './LoginForm';
//import Button from '@material-ui/core/Button';
//import UrlBuilder from '../Base/UrlBuilder';

//const githubOAuthUrl = UrlBuilder.getDefault().githubOAuth();
//const googleOAuthUrl = UrlBuilder.getDefault().googleOAuth();

const Login = () => <React.Fragment>
  <div className="container">
    <div style={{ 'paddingTop': '55px' }}>
      <LoginForm message={'Test'}/>
    </div>
  </div>
  {/* Disable Github and Google oauth
  <div className="container">
    <div style={{ 'textAlign': 'center' }}>
      <a style={{ 'textDecoration': 'none' }} href={githubOAuthUrl}>
        <Button style={{ 'marginTop': '10%' }} variant="contained" color="secondary">
          Sign in with Github
        </Button>
      </a>
    </div>
  </div>
  <div className="container">
    <div style={{ 'textAlign': 'center' }}>
      <a style={{ 'textDecoration': 'none' }} href={googleOAuthUrl}>
        <Button style={{ 'marginTop': '10px' }} variant="contained" color="secondary">
          Sign in with Google
        </Button>
      </a>
    </div>
  </div>
      */}
</React.Fragment>

export default Login;
