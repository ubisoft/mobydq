import gql from 'graphql-tag';
import UrlBuilder from '../Base/UrlBuilder';
import ApolloClient from 'apollo-boost';
import InvalidUserCredentials from '../../Exceptions/InvalidUserCredentials';
import DevLog from '../../actions/DevLog';

export default class Authentication {

  /**
   * Get a new Bearer token and save it as cookies
   */
  static async getAndSaveBearerToken(email, password) {
    const token = await this.getBearerToken(email, password);
    this.saveBearerToken(token);
    return token;
  }

  static async getBearerToken(userEmail, userPassword) {
    const GET_TOKEN = gql`
    mutation getToken($userEmail: String!, $userPassword: String!){
       authenticateUser(input: {userEmail: $userEmail, userPassword: $userPassword}) {
          token
       }
    }`;

    const variables = {
      userEmail,
      userPassword
    };

    DevLog.info(`Requesting auth-token: ${UrlBuilder.getDefault().graphQl()}`);

    // Use new client because Client.js already includes authentication that is not present at this point.
    const apolloClient = new ApolloClient({
      'uri': UrlBuilder.getDefault().graphQl()
    });

    const result = await apolloClient.mutate({
      'mutation': GET_TOKEN,
      variables
    });

    DevLog.info(result);

    if (!result.data.authenticateUser.token) {
      throw new InvalidUserCredentials();
    }

    return result.data.authenticateUser.token;
  }

  static saveBearerToken(token) {
    sessionStorage.setItem('token', token);
  }
}
