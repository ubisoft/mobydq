import React from 'react';
import PropTypes from 'prop-types';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';
import BaseDataView from './BaseDataView';

// TODO Re-use with PrivateRoute.js
function getCookieValue(key) {
  const valueMatch = document.cookie.match(`(^|;)\\s*${key}\\s*=\\s*([^;]+)`);
  return valueMatch ? valueMatch.pop() : '';
}

const client = new ApolloClient({
  'uri': `${process.env.REACT_APP_FLASK_API_URL}graphql`,
  'headers': {
    'Authorization': `Bearer ${getCookieValue('token')}`
  },
  /* global error handler, but incapable of modifying the redux state
  * 'onError': ({ graphQLErrors, networkError, operation, forward }) => {
  *  if (networkError && networkError.statusCode === 401) {
  *    //disable expired cookie to force user to login next time
  *    document.cookie = 'token' + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;'
  *  }
  */
});
window.apiUrl = process.env.REACT_APP_FLASK_API_URL;

const Root = ({ store }) => <ApolloProvider client={client} store={store}>
  <Provider store={store}>
    <BrowserRouter>
      <BaseDataView />
    </BrowserRouter>
  </Provider>
</ApolloProvider>;


Root.propTypes = {
  'store': PropTypes.object.isRequired
};

export default Root;
