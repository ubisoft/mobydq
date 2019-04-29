import React from 'react';
import Authentication from '../../actions/Auth/Authentication';

describe('invalid auth credentials unit test', () => {
  it('matches snapshot', () => {
    Authentication.getFreshBearerToken('someuser', 'somepassword').catch((error) => {
      expect(error).toMatchSnapshot();
    });
  });
});
