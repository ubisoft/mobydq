import gql from 'graphql-tag';
import UrlBuilder from '../../Components/Base/UrlBuilder';
import ApolloClient from 'apollo-boost';
import InvalidUserCredentials from '../../Exceptions/InvalidUserCredentials';
import DevLog from '../DevLog';
import Client from '../../Components/Base/Client';
import SessionUser from '../Auth/SessionUser';

export default class Authentication {

  /**
   * Authenticate current user and save their tokens/data in the session storage
   * @param userEmail
   * @param password
   * @returns {Promise<SessionUser>}
   */
  static async authenticateSessionUser(userEmail, password) {
    const token = await this.getFreshBearerToken(userEmail, password);
    SessionUser.sessionToken = token;
    const user = await this.getUser(userEmail);
    SessionUser.sessionUser = user;
    return SessionUser;
  }

  /**
   * Request a new Session token
   * @param userEmail
   * @param userPassword
   * @returns {Promise<Token|*>}
   */
  static async getFreshBearerToken(userEmail, userPassword) {
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

  static async getUser(userEmail) {
    const GET_USER_ROLE = gql`
    query myusers ($userEmail: String!){
      userByEmail(email: $userEmail) {
        id
        email
        role
      }
    }`;

    DevLog.info(`Requesting user data: ${UrlBuilder.getDefault().graphQl()}`);

    const apolloClient = Client;

    const result = await apolloClient.query({
      'query': GET_USER_ROLE,
      'variables': { userEmail }
    });

    DevLog.log('Userdata: ', result.data.userByEmail);

    this.getPermissions();
    return result.data.userByEmail;
  }

  static async getPermissions() {
    const GET_PERMISSIONS = gql`
    query mygroups {
      allUserGroups{
        nodes {
          name
          id
        }
      }
    }`;

    DevLog.info(await Client.query({ 'query': GET_PERMISSIONS }));
  }
}
