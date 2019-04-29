class SessionUser {
  get sessionToken() {
    return sessionStorage.getItem('token');
  }

  set sessionToken(token) {
    sessionStorage.setItem('token', token);
  }

  get sessionUser() {
    return sessionStorage.getItem('user');
  }

  set sessionUser(user) {
    sessionStorage.setItem('user', user);
  }
}

export default new SessionUser();
