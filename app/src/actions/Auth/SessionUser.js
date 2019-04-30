class SessionUser {
  static _KEY_USER_EMAIL = 'user.email';

  static _KEY_USER_ID = 'user.id';

  static _KEY_USER_ROLE = 'user.role';

  static _KEY_TOKEN = 'token';

  get sessionToken() {
    return sessionStorage.getItem(SessionUser._KEY_TOKEN);
  }

  set sessionToken(token) {
    sessionStorage.setItem(SessionUser._KEY_TOKEN, token);
  }

  get user() {
    const email = sessionStorage.getItem(SessionUser._KEY_USER_EMAIL);
    const id = sessionStorage.getItem(SessionUser._KEY_USER_ID);
    const role = sessionStorage.getItem(SessionUser._KEY_USER_ROLE);
    if (email === null || id === null || role === null) {
      return null;
    }
    return {
      email,
      id,
      role
    };
  }

  set user(user) {
    sessionStorage.setItem(SessionUser._KEY_USER_EMAIL, user.email);
    sessionStorage.setItem(SessionUser._KEY_USER_ID, user.id);
    sessionStorage.setItem(SessionUser._KEY_USER_ROLE, user.role);
  }

  logOut() {
    sessionStorage.removeItem(SessionUser._KEY_USER_EMAIL);
    sessionStorage.removeItem(SessionUser._KEY_USER_ID);
    sessionStorage.removeItem(SessionUser._KEY_USER_ROLE);
    sessionStorage.removeItem(SessionUser._KEY_TOKEN);
  }

  logInAsAnonymous() {
    this.sessionToken = '';
    this.user = {
      'name': 'anonymous',
      'email': 'anonymous',
      'role': 'anonymous'
    };
  }
}

export default new SessionUser();
