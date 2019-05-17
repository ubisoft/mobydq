import React from 'react';
import PropTypes from 'prop-types';
import { Provider } from 'react-redux';
import { HashRouter } from 'react-router-dom';
import BaseDataView from './BaseDataView';
import StatedApolloProvider from './StatedApolloProvider';

/*
 * Import { ApolloProvider } from 'react-apollo';
 * import Client from './Client';
 *
 *
 * const Root = ({ store }) => <ApolloProvider client={Client.getApolloClient()} store={store}>
 * <Provider store={store}>
 * <HashRouter>
 * <BaseDataView/>
 * </HashRouter>
 * </Provider>
 * </ApolloProvider>;
 */

const Root = ({ store }) => <StatedApolloProvider store={store}>
  <Provider store={store}>
    <HashRouter>
      <BaseDataView/>
    </HashRouter>
  </Provider>
</StatedApolloProvider>;


Root.propTypes = {
  'store': PropTypes.object.isRequired
};

export default Root;
