import React from 'react';
import { shallow } from 'enzyme';
import { MockedProvider } from 'react-apollo/test-utils';

import IndicatorRepository from './../../repository/IndicatorRepository';
import IndicatorList from '../../Components/Indicator/IndicatorList';

describe('IndicatorList unit test', () => {
  let wrapper;
  const query = IndicatorRepository.getListPage(1, 10);

  const mocks = [
    {
      'request': {
        query
      },
      'result': {
        'data': {
          'allIndicators': {
            'nodes': [
              {
                'id': 1,
                'name': 'dq_example_completeness_indicator',
                'indicatorTypeId': 1,
                'indicatorGroupId': 1,
                'executionOrder': 1,
                'flagActive': true,
                'updatedDate': '2018-10-06T05:44:17.45341'
              },
              {
                'id': 2,
                'name': 'dq_example_freshness_indicator',
                'indicatorTypeId': 2,
                'indicatorGroupId': 1,
                'executionOrder': 1,
                'flagActive': true,
                'updatedDate': '2018-10-06T05:44:17.45341'
              },
              {
                'id': 3,
                'name': 'dq_example_latency_indicator',
                'indicatorTypeId': 3,
                'indicatorGroupId': 1,
                'executionOrder': 1,
                'flagActive': true,
                'updatedDate': '2018-10-06T05:44:17.45341'
              },
              {
                'id': 4,
                'name': 'dq_example_validity_indicator',
                'indicatorTypeId': 4,
                'indicatorGroupId': 1,
                'executionOrder': 1,
                'flagActive': true,
                'updatedDate': '2018-10-06T05:44:17.45341'
              }
            ]
          }
        }
      }
    }
  ];

  beforeEach(() => {
    wrapper = shallow(
      <MockedProvider mocks={mocks} addTypename={true}>
        <IndicatorList/>
      </MockedProvider>
    );
  });

  it('renders', () => {
    expect(wrapper).toHaveLength(1);
  });

  /*
   * It('loads the table properly', () => {
   *    expect(wrapper).toEqual(4);
   *    expect(wrapper.find('th').length).toEqual(7);
   *    expect(wrapper.find('td').length).toEqual(28);
   *    expect(wrapper.find('th').at(0)).toEqual('Id');
   *    expect(wrapper.find('td').at(0)).toEqual('1');
   *    expect(wrapper.find('td').at(11)).toEqual('1');
   * });
   */

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});
