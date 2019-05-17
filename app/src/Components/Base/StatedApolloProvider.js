import React from 'react';
import { ApolloProvider } from 'react-apollo';
import Client from './Client';

/**
 * Because the Apollo client gets changed when the user logs in, it must get a new instance on setState.
 */
export default class StatedApolloProvider extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      'apolloClient': Client.getApolloClient()
    };
  }

  render() {
    return (
      <ApolloProvider client={this.state.apolloClient} store={this.props.store}>
        {this.props.children}
      </ApolloProvider>);
  }
}
