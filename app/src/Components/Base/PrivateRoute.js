import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, ...parentProps }) => (
    <Route {...parentProps} render={(props) => (
        isAuthenticated(parentProps)
            ? <Component {...props} />
            : <Redirect to={{
            pathname: '/login',
            state: { from: props.location }
        }} />
    )} />
);

function isAuthenticated(props){
    let cookieValue = getCookieValue('token');
    if(cookieValue !== null){
        let token = parseJwt(cookieValue);

        for(let i = 0; i < props.permissions.length; i++) {
            if(!token.role.includes(props.permissions[i])) {
                return false;
            }
        }

        return true;
    }
    return false;
}

function parseJwt(token) {
    let base64Token = token.split('.')[1];
    let base64 = base64Token.replace('-', '+').replace('_', '/');
    return JSON.parse(window.atob(base64));
}

function getCookieValue(a) {
    let b = document.cookie.match('(^|;)\\s*' + a + '\\s*=\\s*([^;]+)');
    return b ? b.pop() : '';
}


export default PrivateRoute