import React from 'react';
import { shallowWrap } from './../../setupTests';

import DataSourceForm from './../../Components/DataSource/DataSourceForm';

describe('DataSourceForm component unit test', () => {
  const touched = {
    'name': false,
    'dataSourceTypeId': false,
    'connectionString': false,
    'login': false,
    'password': false
  };
  const values = {
    'name': '',
    'dataSourceTypeId': '',
    'connectionString': '',
    'login': '',
    'password': ''
  };
  const errors = {
    'name': null,
    'dataSourceTypeId': null,
    'connectionString': null,
    'login': null,
    'password': null
  };
  const data = {
    'allDataSourceTypes': {
      'nodes': [
        {
          'id': 1,
          'value': 'mock data source'
        }
      ]
    }
  };

  const wrapper = shallowWrap(<DataSourceForm data={data} initialFieldValues={null} touched={touched} values={values} errors={errors} handleBlur={jest.fn()} handleChange={jest.fn()} handleSubmit={jest.fn()} isSubmitting={false}/>);
  it('matches snapshot', () => {
    expect(wrapper.dive()).toMatchSnapshot();
  });
});
