import ApolloClient from 'apollo-boost';
import UrlBuilder from '../Base/UrlBuilder';
import SessionUser from '../../actions/Auth/SessionUser';

function getSessionToken() {
  return SessionUser.sessionToken;
}

// When the user either isn't set yet or he is anonymous, it should return a new ApolloClient without the header Auth.
/*export default !SessionUser.user || SessionUser.user.role === 'anonymous' ? new ApolloClient({ 'uri': UrlBuilder.getDefault().graphQl() }) : new ApolloClient({
  'uri': UrlBuilder.getDefault().graphQl(),
  'headers': {
    'Authorization': `Bearer ${getSessionToken()}`
  }
});*/
export default new ApolloClient({
  'uri': UrlBuilder.getDefault().graphQl(),
  'headers': {
    'Authorization': `Bearer ${getSessionToken()}`
  }
});
