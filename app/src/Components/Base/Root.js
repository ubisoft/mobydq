import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "react-apollo";
import BaseDataView from './BaseDataView'


function getCookieValue(a) {
  var b = document.cookie.match('(^|;)\\s*' + a + '\\s*=\\s*([^;]+)');
  return b ? b.pop() : '';
}


const client = new ApolloClient({
  uri: process.env.REACT_APP_FLASK_API_URL + 'graphql',
  headers: {
    'Authorization': 'Bearer ' + getCookieValue('token')
  }
  // options: { mode: 'no-cors' }
});
window.apiUrl = process.env.REACT_APP_FLASK_API_URL;

const Root = ({ store }) => (
  <ApolloProvider client={client}>
    <Provider store={store}>
      <BrowserRouter>
        <BaseDataView />
      </BrowserRouter>
    </Provider>
  </ApolloProvider>
)

Root.propTypes = {
  store: PropTypes.object.isRequired
}

export default Root
