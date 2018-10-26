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
  'uri': `${process.env.REACT_APP_FLASK_API_HOST}/mobydq/api/v1/graphql`,
  'headers': {
    'Authorization': `Bearer ${getCookieValue('token')}`
  }
  // Options: { mode: 'no-cors' }
});

const Root = ({ store }) => <ApolloProvider client={client}>
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
