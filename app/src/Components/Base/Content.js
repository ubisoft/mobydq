import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Dashboard from './../Dashboard/Dashboard';
import Indicator from './../Indicator/Indicator';
import IndicatorGroup from './../IndicatorGroup/IndicatorGroup';
import UserGroup from './../UserGroup/UserGroup';
import Admin from './../Admin/Admin';
import DataSource from './../DataSource/DataSource';
import NotFoundComponent from '../Error/NotFoundComponent';
import Login from '../Login/Login';
import PrivateRoute from './PrivateRoute';

const Content = () => <main>
  <Switch>
    <PrivateRoute permissions={['TBD for postgraphile']} exact path="/" component={Dashboard} />
    <PrivateRoute permissions={['TBD for postgraphile']} path="/indicator" component={(props) => <Indicator {...props} />} />
    <PrivateRoute permissions={['TBD for postgraphile']} path="/indicator-group" component={IndicatorGroup} />
    <PrivateRoute permissions={['TBD for postgraphile']} path="/data-source" component={DataSource} />
    <PrivateRoute permissions={['TBD for postgraphile']} path="/user-group" component={UserGroup} />
    <PrivateRoute permissions={['TBD for postgraphile']} path="/admin" component={Admin} />
    <Route path="/login" component={Login} />
    <Route component={NotFoundComponent} />
  </Switch>
</main>;


export default Content;
