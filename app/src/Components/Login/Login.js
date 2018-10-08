import React from 'react';
import {styles} from './../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

class Login extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            tableContent: this.props.tableContent,
        }
    }

    login()
    {
        alert("Login :-)");
    }

    render() {
        return (
            <React.Fragment>
                <div className="container">
                    <div className="loginForm">
                        <div className="loginFormHeader">
                            <table>
                                <td>
                                    <div className="btnCloseFake"></div>
                                </td>
                                <td>
                                    <div className="btnMinimizeFake"></div>
                                </td>
                                <td>
                                    <div className="btnMaximizeFake"></div>
                                </td>
                            </table>
                        </div>
                        <div style={{textAlign: "center"}}>
                        <Button style={{marginTop: "25%"}} onClick={this.login} variant="contained" color="secondary">
                            Sign in with Google
                        </Button>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        )
    }
}

export default withStyles(styles)(Login);
