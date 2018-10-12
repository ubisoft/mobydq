import React from 'react';
import PropTypes from 'prop-types';
import './../../styles/baseStyles';
import Button from '@material-ui/core/Button';

const Login = ({
                   ...props
               }) => {
    return (
        <React.Fragment>
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
                    <div style={{textAlign: "center"}}>
                        <a style={{textDecoration: "none"}} href="http://google.ch">
                            <Button style={{marginTop: "25%"}} variant="contained" color="secondary">
                                Sign in with Google
                            </Button>
                        </a>
                    </div>
                </div>
            </div>
        </React.Fragment>
    );
};

export default Login;

