import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Dashboard from './../Dashboard/Dashboard';
import Indicator from './../Indicator/Indicator';
import IndicatorGroup from './../IndicatorGroup/IndicatorGroup';
import Admin from './../Admin/Admin';
import DataSource from './../DataSource/DataSource';
import NotFoundComponent from '../Error/NotFoundComponent';
import Login from '../Login/Login';
import PrivateRoute from './PrivateRoute';

/**
 * You can find all possible permissions in the UserRolePermissions file
 * @see UserRolePermissions
 */

const Content = () => <main>
  <Switch>
    <PrivateRoute permissions={[] /* TBD for Dashboard */} exact path="/" component={Dashboard}/>
    <PrivateRoute permissions={['r_indicators']} path="/indicator" component={(props) => <Indicator {...props} />}/>
    <PrivateRoute permissions={['r_indicator_groups']} path="/indicator-group" component={IndicatorGroup}/>
    <PrivateRoute permissions={['r_data_sources']} path="/data-source" component={DataSource}/>
    <PrivateRoute permissions={['r_users']} path="/admin" component={Admin}/>
    { /* You can pass an error message to the login using <Redirect to={{ 'pathname': '/XX', 'state': { 'from': props.location, 'message': 'Your message' }}} />*/}
    <Route path="/login" render={(props) => <Login message={props.location.state ? props.location.state.message : '' }/>}/>
    <Route component={NotFoundComponent}/>
  </Switch>
</main>;


export default Content;
