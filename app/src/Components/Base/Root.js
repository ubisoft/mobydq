import React from 'react';
import PropTypes from 'prop-types';
import { Provider } from 'react-redux';
import { HashRouter } from 'react-router-dom';
import { ApolloProvider } from 'react-apollo';
import BaseDataView from './BaseDataView';
import Client from './Client';


const Root = ({ store }) => <ApolloProvider client={Client} store={store}>
  <Provider store={store}>
    <HashRouter>
      <BaseDataView />
    </HashRouter>
  </Provider>
</ApolloProvider>;


Root.propTypes = {
  'store': PropTypes.object.isRequired
};

export default Root;
