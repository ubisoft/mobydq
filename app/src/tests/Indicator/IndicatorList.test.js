import React from 'react';
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';
import { MockedProvider } from 'react-apollo/test-utils';

import IndicatorRepository from './../../repository/IndicatorRepository';
import IndicatorList from '../../Components/Indicator/IndicatorList';
import Indicator from "../../Components/Indicator/Indicator";

describe('IndicatorList unit test', () => {
  let wrapper;
  let query = IndicatorRepository.getListPage(1, 10);

  let mocks = [
  {
    request: {
      query: query
    },
    result: {
       data: {
        allIndicators: {
          nodes: [
            {
              id: 1,
              name: "dq_example_completeness_indicator",
              indicatorTypeId: 1,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            },
            {
              id: 2,
              name: "dq_example_freshness_indicator",
              indicatorTypeId: 2,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            },
            {
              id: 3,
              name: "dq_example_latency_indicator",
              indicatorTypeId: 3,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            },
            {
              id: 4,
              name: "dq_example_validity_indicator",
              indicatorTypeId: 4,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            }
          ]
        }
      }
    },
  },
];

  beforeEach(() => {
    wrapper = shallow(
      <MockedProvider mocks={mocks} addTypename={true}>
        <IndicatorList/>
      </MockedProvider>
    )
  });

  it('renders', () => {
    expect(wrapper.length).toEqual(1);
  });

  it('loads the table properly', () => {
     expect(wrapper).toEqual(4);
     expect(wrapper.find('th').length).toEqual(7);
     expect(wrapper.find('td').length).toEqual(28);
     expect(wrapper.find('th').at(0)).toEqual('Id');
     expect(wrapper.find('td').at(0)).toEqual('1');
     expect(wrapper.find('td').at(11)).toEqual('1');
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('IndicatorList unit test', () => {
  let wrapper;
  let query = IndicatorRepository.getListPage(1, 10);

  let mocks = [
  {
    request: {
      query: query
    },
    result: {
       data: {
        allIndicators: {
          nodes: [
            {
              id: 1,
              name: "dq_example_completeness_indicator",
              indicatorTypeId: 1,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            },
            {
              id: 2,
              name: "dq_example_freshness_indicator",
              indicatorTypeId: 2,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            },
            {
              id: 3,
              name: "dq_example_latency_indicator",
              indicatorTypeId: 3,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            },
            {
              id: 4,
              name: "dq_example_validity_indicator",
              indicatorTypeId: 4,
              indicatorGroupId: 1,
              executionOrder: 1,
              flagActive: true,
              updatedDate: "2018-10-06T05:44:17.45341"
            }
          ]
        }
      }
    },
  },
];

  //todo figure out why enzyme mount hangs the tests
  beforeEach(() => {
    wrapper = shallow(
      <MockedProvider mocks={mocks} addTypename={true}>
        <IndicatorList/>
      </MockedProvider>
    )
  });

  it('renders', () => {
    expect(wrapper.length).toEqual(1);
  });

  it('loads the table properly', () => {
     expect(wrapper).toEqual(4);
     expect(wrapper.find('th').length).toEqual(7);
     expect(wrapper.find('td').length).toEqual(28);
     expect(wrapper.find('th').at(0)).toEqual('Id');
     expect(wrapper.find('td').at(0)).toEqual('1');
     expect(wrapper.find('td').at(11)).toEqual('1');
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

