import ApolloClient from 'apollo-boost';
import UrlBuilder from '../Base/UrlBuilder';


// TODO Re-use with PrivateRoute.js
function getCookieValue(key) {
  const valueMatch = document.cookie.match(`(^|;)\\s*${key}\\s*=\\s*([^;]+)`);
  return valueMatch ? valueMatch.pop() : '';
}

export default new ApolloClient({
  'uri': UrlBuilder.getDefault().graphQl(),
  'headers': {
    'Authorization': `Bearer ${getCookieValue('token')}`
  }
});
