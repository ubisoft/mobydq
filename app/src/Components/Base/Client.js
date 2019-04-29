import ApolloClient from 'apollo-boost';
import UrlBuilder from '../Base/UrlBuilder';
import SessionUser from '../../actions/Auth/SessionUser';

function getSessionToken() {
  return SessionUser.sessionToken;
}

export default new ApolloClient({
  'uri': UrlBuilder.getDefault().graphQl(),
  'headers': {
    'Authorization': `Bearer ${getSessionToken()}`
  }
});
