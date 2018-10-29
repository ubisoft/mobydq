import React from 'react';
import { UnauthorisedError } from './UnauthorisedError';

class GraphQLError extends React.Component {
  render() {
    const error = this.props.error;
    if (error.graphQLErrors.length > 0) {
      return <div>
        {error.graphQLErrors.statusCode + ': ' + error.graphQLErrors.result.message}
      </div>;
    }
    if (error.networkError) {
      switch (error.networkError.statusCode) {
        case 401:
          return <UnauthorisedError/>;
        default:
          return <div>
            {error.networkError.statusCode + ': ' + error.networkError.result.message}
          </div>;
      }
    }
    return <div>No error. Something wrong happened...</div>;
  }
}

export default GraphQLError;
