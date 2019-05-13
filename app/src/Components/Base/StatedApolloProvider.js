import React from 'react';
import { ApolloProvider } from 'react-apollo';
import Client from './Client';
import DevLog from '../../actions/DevLog';

/**
 * Because the Apollo client gets changed when the user logs in, it must get a new instance on setState.
 */
export default class StatedApolloProvider extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      'apolloClient': Client.getApolloClient()
    };
    this.replaceApolloClient = this.replaceApolloClient.bind(this);
  }

  // Login must be able to change the apollo client, might want to change that to react flux way. (Haven't done that before no clue)
  replaceApolloClient() {
    DevLog.info('Changing apolloClient');
    this.setState({
      'apolloClient': Client.getApolloClient()
    });
  }

  render() {
    return (
      <ApolloProvider client={this.state.apolloClient} store={this.props.store}>
        {this.props.children}
      </ApolloProvider>);
  }
}
