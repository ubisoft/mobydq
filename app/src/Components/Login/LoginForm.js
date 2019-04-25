import React from 'react';
import { Button, Input, withStyles } from '@material-ui/core';
import { styles } from '../../styles/baseStyles';
import FormGroup from '@material-ui/core/FormGroup';
import FormLabel from '@material-ui/core/FormLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import { GraphQLSchema } from 'graphql';

class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    // Next we establish our state
    this.state = {
      'message': this.props.message ? this.props.message : '',
      // Todo make name "sticky"
      'name': '',
      'password': ''
    };
  }

  onChangeName(changeEvent) {
    this.setState({
      'name': changeEvent.target.value
    });
  }

  onChangePassword(changeEvent) {
    this.setState({
      'password': changeEvent.target.value
    });
  }

  onButtonPressed(username, password) {
    console.log('yoboi');
    let schema = new GraphQLSchema({
      mutation {
        authenticateUser(
          input: {
            userEmail: username,
            userPassword: this.state.password
          })
      }
      /*authenticateUser(input: {userEmail: this.state., userPassword: "admin"}) {
        clientMutationId
        token
      }*/
    });
  }

  // The render function, where we actually tell the browser what it should show
  render() {
    return (
      <div className="container" style={{ 'padding-top': '-1%' }}>
        <div style={{
          'textAlign': 'center',
          'align-items': 'center'
        }}>
          <div className="background-box" style={{
            'display': 'inline-block',
            'padding': '2%'
          }}>
            <h2>Login</h2>
            <p style={{ 'color': 'red' }}>{this.state.message}</p>
            <div style={{
              'textAlign': 'left',
              'align-items': 'left'
            }}>
              <FormGroup>
                <section className="section">
                  <FormLabel className="label">Username: </FormLabel>
                  <Input className="input" name="name" placeholder="Enter your username..."
                         autoFocus onChange={() => this.onChangeName}/>
                  <br/>
                  <br/>
                  <FormLabel className="label">Password: </FormLabel>
                  <Input className="input" type="password" name="password" onChange={() => this.onChangePassword}/>
                </section>
                <Button action={() => this.onButtonPressed()} style={{ 'marginTop': '10%' }} variant="contained"
                        color="secondary">
                  Sign in
                </Button>
              </FormGroup>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(LoginForm);
