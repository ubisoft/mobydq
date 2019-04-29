import React from 'react';
import Authentication from '../../Components/Login/Authentication';

describe('invalid auth credentials unit test', () => {
  it('matches snapshot', () => {
    Authentication.getBearerToken('someuser', 'somepassword').catch((error) => {
      expect(error).toMatchSnapshot();
    });
  });
});
