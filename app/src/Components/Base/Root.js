import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "react-apollo";
import BaseDataView from './BaseDataView'


const client = new ApolloClient({
  uri: process.env.REACT_APP_API_URL,
// options: { mode: 'no-cors' }
});

const Root = ({ store }) => (
  <ApolloProvider client={client}>
    <Provider store={store}>
      <BrowserRouter>
        <BaseDataView/>
      </BrowserRouter>
    </Provider>
  </ApolloProvider>
)

Root.propTypes = {
  store: PropTypes.object.isRequired
}

export default Root
