import ApolloClient from 'apollo-boost';
import UrlBuilder from '../Base/UrlBuilder';
import SessionUser from './Auth/SessionUser';

export default class Client {
  static getSessionToken() {
    return SessionUser.sessionToken;
  }

  // When the user either isn't set yet or he is anonymous, it should return a new ApolloClient without the header Auth.
  static getApolloClient() {
    if (SessionUser.sessionToken) {
      return this.getAuthApolloClient();
    }
    return this.getBasicApolloClient();
  }

  /**
   * ApolloClient without auth header for public users
   * @returns {DefaultClient<any>}
   */
  static getBasicApolloClient() {
    return new ApolloClient({ 'uri': UrlBuilder.getDefault().graphQl() });
  }

  static getAuthApolloClient() {
    return new ApolloClient({
      'uri': UrlBuilder.getDefault().graphQl(),
      'headers': {
        'Authorization': `Bearer ${this.getSessionToken()}`
      }
    });
  }
}

