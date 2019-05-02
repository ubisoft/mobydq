import React from 'react';
import { Button, Input, withStyles } from '@material-ui/core';
import { styles } from '../../styles/baseStyles';
import FormGroup from '@material-ui/core/FormGroup';
import FormLabel from '@material-ui/core/FormLabel';
import Authentication from '../../Authentication/Authentication';
import { Redirect } from 'react-router';
import DevLog from '../../actions/DevLog';
import SessionUser from '../../Authentication/SessionUser';

class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      'message': this.props.message ? this.props.message : '',
      'email': '',
      'password': '',
      'redirect': false
    };
  }

  _onChangeEmail(changeEvent) {
    this.setState({
      'email': changeEvent.target.value
    });
  }

  _onChangePassword(changeEvent) {
    this.setState({
      'password': changeEvent.target.value
    });
  }

  // On enter pressed --> smoother login
  _handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      this._onButtonPressed();
    }
  };

  _onButtonPressed() {
    Authentication.authenticateSessionUser(this.state.email, this.state.password).then((result) => {
      DevLog.log(result);

      this.setState({
        'redirect': true
      });
    }).catch((error) => {
      this.setState({
        'message': error.message
      });
    });
  }

  _onContinueAnonymous() {
    DevLog.info('Clicked on continue anonymously');
    SessionUser.logInAsAnonymous();
    this.setState({
      'redirect': true
    });
  }

  // Todo sticky email
  render() {
    if (this.state.redirect) {
      return <Redirect to="/"/>;
    }
    return (
      <div className="container" style={{ 'paddingTop': '-15px' }}>
        <div style={{
          'textAlign': 'center',
          'alignItems': 'center',
          'width': '300px'
        }}>
          <div className="background-box" style={{
            'display': 'inline-block',
            'padding': '20px'
          }}>
            <h2>Login</h2>
            <p style={{
              'color': 'red'
            }}>{this.state.message}</p>
            <div style={{
              'textAlign': 'left',
              'alignItems': 'left'
            }}>
              <FormGroup>
                <section className="section">
                  <table>
                    <tbody>
                      <tr>
                        <td><FormLabel className="label">Email: </FormLabel></td>
                        <td>
                          <Input
                            className="input"
                            name="email"
                            placeholder="Enter your email"
                            autoFocus
                            onChange={(evt) => this._onChangeEmail(evt)}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td><FormLabel className="label">Password: </FormLabel></td>
                        <td>
                          <Input
                            className="input"
                            type="password"
                            name="password"
                            placeholder="Your password"
                            onChange={(evt) => this._onChangePassword(evt)}
                            onKeyDown={this._handleKeyDown}
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </section>
                <Button onClick={() => this._onButtonPressed()} style={{ 'marginTop': '10%' }} variant="contained"
                        color="secondary">
                  Sign in
                </Button>
              </FormGroup>
              <br/>
              <a href="#" onClick={() => this._onContinueAnonymous()}>Continue anonymously...</a>
            </div>
          </div>
        </div>
      </div>);
  }
}

export default withStyles(styles)(LoginForm);
