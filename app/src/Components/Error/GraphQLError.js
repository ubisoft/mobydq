import React from 'react';
import { UnauthorizedError } from './UnauthorizedError';

export const GraphQLError = ({ error }) => {
  if (error && error.graphQLErrors.length > 0) {
    return <div>
      {error.graphQLErrors.statusCode + ': ' + error.graphQLErrors.result.message}
    </div>;
  }
  if (error && error.networkError) {
    switch (error.networkError.statusCode) {
      case 401:
        return <UnauthorizedError />;
      default:
        return <div>
          {error.networkError.statusCode + ': ' + error.networkError.result.message}
        </div>;
    }
  }
  return <div>No error. Something wrong happened...</div>;
}
