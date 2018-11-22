import React from 'react';
import { shallowWrap } from './../../setupTests';

import { MemoryRouter } from 'react-router-dom';

import { GraphQLError } from '../../Components/Error/GraphQLError';

describe('graphql error unit test', () => {
  const gqlError = {
    'graphQLErrors': [
      {
        'message': 'test message 1'
      },
      {
        'message': 'test message 2'
      }
    ],
    'message': 'a global error message'
  };

  let wrapper;

  beforeEach(() => {
    wrapper = shallowWrap(
      <GraphQLError
        error={gqlError}
      />
    );
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('network error unit test', () => {
  const networkError = {
    'networkError': {
      'statusCode': 401,
      'message': 'Unauthorised'
    },
    'graphQLErrors': []
  };

  let wrapper;

  beforeEach(() => {
    wrapper = shallowWrap(
      <GraphQLError
        error={networkError}
      />
    );
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('error component functional test', () => {

  it('renders the graphql error', () => {
    const gqlError = {
      'graphQLErrors': [
        {
          'error': 'error message 1'
        },
        {
          'error': 'error message 2'
        }
      ],
      'message': 'a global error message'
    };
    const wrapper = mount(<div><GraphQLError error={gqlError}/></div>);
    const errorMessage = <div>a global error message</div>;
    expect(wrapper.contains(errorMessage)).toEqual(true);
  });

  it('renders the generic network error', () => {
    const networkError = {
    'networkError': {
      'statusCode': 404,
      'message': 'Not found'
    },
    'graphQLErrors': []
  };
    const wrapper = mount(<div><GraphQLError error={networkError}/></div>);
    const errorMessage = <div>404: Not found</div>;
    expect(wrapper.contains(errorMessage)).toEqual(true);
  });
});


describe('error component functional test', () => {

  it('renders the graphql error', () => {
    const gqlError = {
      'graphQLErrors': [
        {
          'error': 'error message 1'
        },
        {
          'error': 'error message 2'
        }
      ],
      'message': 'a global error message'
    };
    const wrapper = mount(<div><GraphQLError error={gqlError}/></div>);
    const errorMessage = <div>a global error message</div>;
    expect(wrapper.contains(errorMessage)).toEqual(true);
  });

  it('renders the generic network error', () => {
    const networkError = {
    'networkError': {
      'statusCode': 404,
      'message': 'Not found'
    },
    'graphQLErrors': []
  };
    const wrapper = mount(<div><GraphQLError error={networkError}/></div>);
    const errorMessage = <div>404: Not found</div>;
    expect(wrapper.contains(errorMessage)).toEqual(true);
  });

  it('renders the 401 login error', () => {
    const networkError = {
    'networkError': {
      'statusCode': 401,
      'message': 'Unauthorised'
    },
    'graphQLErrors': []
  };
    const wrapper = mount(<div><MemoryRouter><GraphQLError error={networkError}/></MemoryRouter></div>);
    const errorMessage = 'Your session has expired'
    expect(wrapper.contains(errorMessage)).toEqual(true);
  });

  it('renders the unknown error message', () => {
    const networkError = {
    'someUnexpectedJson': 'message'
  };
    const wrapper = mount(<div><MemoryRouter><GraphQLError error={networkError}/></MemoryRouter></div>);
    const errorMessage = <div>No error. Something wrong happened...</div>;
    expect(wrapper.contains(errorMessage)).toEqual(true);
  });
});