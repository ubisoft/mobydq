import ApolloClient from 'apollo-boost';
import UrlBuilder from '../Base/UrlBuilder';
import SessionUser from '../../Authentication/SessionUser';
import DevLog from '../../actions/DevLog';

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
    DevLog.log('Get basic apollo client.');
    return new ApolloClient({ 'uri': UrlBuilder.getDefault().graphQl() });
  }

  static getAuthApolloClient() {
    DevLog.log('Get authenticated apollo client.');
    return new ApolloClient({
      'uri': UrlBuilder.getDefault().graphQl(),
      'headers': {
        'Authorization': `Bearer ${this.getSessionToken()}`
      }
    });
  }
}

