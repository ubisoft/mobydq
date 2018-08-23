import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "react-apollo";
import BaseDataView from './BaseDataView'


const client = new ApolloClient({
  uri: "http://192.168.99.100:5433/graphql",
opts: { mode: 'no-cors' }
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