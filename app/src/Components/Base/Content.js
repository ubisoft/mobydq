import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Dashboard from './../Dashboard/Dashboard';
import Indicator from './../Indicator/Indicator';
import IndicatorGroup from './../IndicatorGroup/IndicatorGroup';
import Admin from './../Admin/Admin';
import DataSource from './../DataSource/DataSource';
import NotFoundComponent from '../Error/NotFoundComponent'
import Login from '../Login/Login';

const Content = () => (
  <main>
    <Switch>
      <Route exact path='/' component={Dashboard} />
      <Route path='/indicator' component={(props) => (<Indicator {...props} />)} />
      <Route path='/indicator-group' component={IndicatorGroup} />
      <Route path='/data-source' component={DataSource} />
      <Route path='/admin' component={Admin} />
      <Route path='/login' component={Login} />
      <Route component={NotFoundComponent} />
    </Switch>
  </main>
)

export default Content