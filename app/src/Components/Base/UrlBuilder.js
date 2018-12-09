

const BASE_URL = process.env.REACT_APP_FLASK_API_HOST;

class UrlBuilder {
  constructor(version) {
    const versionUrl = UrlBuilder._combineUrl('/mobydq/api', version);
    this._baseUrl = UrlBuilder._combineUrl(BASE_URL, versionUrl);
  }

  static getDefault() {
    return new UrlBuilder('v1');
  }

  graphQl() {
    return UrlBuilder._combineUrl(this._baseUrl, 'graphql');
  }

  githubOAuth() {
    return UrlBuilder._combineUrl(this._baseUrl, 'security/oauth/github');
  }

  googleOAuth() {
    return UrlBuilder._combineUrl(this._baseUrl, 'security/oauth/google');
  }

  static _combineUrl(oldLeft, oldRight) {
    let left = oldLeft;
    let right = oldRight;
    if (left && !left.endsWith('/')) {
      left += '/';
    }

    if (right && right.startsWith('/')) {
      right = right.substr(1);
    }

    return (left || '') + (right || '');
  }
}

export default UrlBuilder;
