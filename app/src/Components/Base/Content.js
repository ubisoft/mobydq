import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import Dashboard from './../Dashboard/Dashboard';
import Indicator from './../Indicator/Indicator';
import IndicatorGroup from './../IndicatorGroup/IndicatorGroup';
import Admin from './../Admin/Admin';
import DataSource from './../DataSource/DataSource';
import NotFoundComponent from '../Error/NotFoundComponent'
import Login from '../Login/Login';

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

const Content = () => (
  <main>
    <Switch>
      <PrivateRoute permissions={['TBD for postgraphile']} exact path='/' component={Dashboard} />
      <PrivateRoute permissions={['TBD for postgraphile']} path='/indicator' component={(props) => (<Indicator {...props} />)} />
      <PrivateRoute permissions={['TBD for postgraphile']} path='/indicator-group' component={IndicatorGroup} />
      <PrivateRoute permissions={['TBD for postgraphile']} path='/data-source' component={DataSource} />
      <PrivateRoute permissions={['TBD for postgraphile']} path='/admin' component={Admin} />
      <Route path='/login' component={Login} />
      <Route component={NotFoundComponent} />
    </Switch>
  </main>
)

export default Content