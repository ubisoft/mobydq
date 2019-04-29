import Exception from './Exception';

export default class InvalidUserCredentials extends Exception {
  constructor() {
    super('invalid_user_credentials', 'The given credentials were not correct.');
  }
}
