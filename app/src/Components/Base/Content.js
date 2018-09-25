import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Dashboard from './../Dashboard/Dashboard';
import Indicator from './../Indicator/Indicator';
import IndicatorGroup from './../IndicatorGroup/IndicatorGroup';
import Admin from './../Admin/Admin';
import DataSourceList from './../DataSource/DataSourceList';

const Content = () => (
  <main>
    <Switch>
      <Route exact path='/' component={Dashboard}/>
      <Route path='/indicator' component={ (props) => (<Indicator {...props} />)} />
      <Route path='/indicator-group' component={IndicatorGroup}/>
      <Route path='/data-sources' component={DataSourceList}/>
      <Route path='/admin' component={Admin}/>
    </Switch>
  </main>
)

export default Content