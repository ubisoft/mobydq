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
  },
  /* global error handler, but incapable of modifying the redux state
  * 'onError': ({ graphQLErrors, networkError, operation, forward }) => {
  *  if (networkError && networkError.statusCode === 401) {
  *    //disable expired cookie to force user to login next time
  *    document.cookie = 'token' + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;'
  *  }
  */
});