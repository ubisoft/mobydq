import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import Dashboard from './../Dashboard/Dashboard';
import Indicator from './../Indicator/Indicator';
import IndicatorGroup from './../IndicatorGroup/IndicatorGroup';
import Admin from './../Admin/Admin';
import DataSource from './../DataSource/DataSource';
import NotFoundComponent from '../Error/NotFoundComponent'
import Login from '../Login/Login';

const PrivateRoute = ({ component: Component, ...rest }) => (
    <Route {...rest} render={(props) => (
        isAuthentificated(rest)
            ? <Component {...props} />
            : <Redirect to={{
            pathname: '/login',
            state: { from: props.location }
        }} />
    )} />
);

function isAuthentificated(props){
    let cookieValue = getCookieValue('token');
    if(cookieValue !== null && cookieValue.length > 5){
        let token = parseJwt(cookieValue);

        for(let a = 0; a < props.permissions.length; a++) {
            if(!token.role.includes(props.permissions[a])) {
                return false;
            }
        }
        return true;
    }
    return false;
}

function parseJwt (token) {
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace('-', '+').replace('_', '/');
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