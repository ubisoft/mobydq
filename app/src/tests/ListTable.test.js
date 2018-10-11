import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import ListTable from '../Components/ListTable/ListTable';



test('renders without crashing with normal data object', () => {
  const data =
  [
    {
      createdDate: "2018-08-24T06:05:01.608821",
      description: "Example of completeness indicator",
      executionOrder: 1,
      flagActive: true,
      id: 1,
      indicatorTypeId: 1,
      name: "dq_example_completeness_indicator",
      updatedDate: "2018-08-24T06:05:01.608821",
      __typename: "Indicator",
    },
    {
      createdDate: "2018-08-24T06:05:01.608821",
      description: "Example of completeness indicator",
      executionOrder: 1,
      flagActive: true,
      id: 2,
      indicatorTypeId: 1,
      name: "dq_example_completeness_indicator",
      updatedDate: "2018-08-24T06:05:01.608821",
      __typename: "Indicator",
    },
  ];

  const buttons = [{"name": "edit", "function": null}, {"name": "King", "function": null}];
  const wrapper = shallow(
    <ListTable data={data} buttons={buttons}/>
  );


  expect(wrapper).toMatchSnapshot();

});

test('renders without crashing with normal data object and no action buttons', () => {
  const data =
  [
    {
      createdDate: "2018-08-24T06:05:01.608821",
      description: "Example of completeness indicator",
      executionOrder: 1,
      flagActive: true,
      id: 1,
      indicatorTypeId: 1,
      name: "dq_example_completeness_indicator",
      updatedDate: "2018-08-24T06:05:01.608821",
      __typename: "Indicator",
    },
    {
      createdDate: "2018-08-24T06:05:01.608821",
      description: "Example of completeness indicator",
      executionOrder: 1,
      flagActive: true,
      id: 2,
      indicatorTypeId: 1,
      name: "dq_example_completeness_indicator",
      updatedDate: "2018-08-24T06:05:01.608821",
      __typename: "Indicator",
    },
  ];

  const wrapper = shallow(
    <ListTable data={data}/>
  );

  expect(wrapper).toMatchSnapshot();

});

test('renders without crashing with empty object', () => {
  const data = "not an array";

  const wrapper = shallow(
    <ListTable data={[]}/>
  );

  expect(wrapper).toMatchSnapshot();
});

// it('renders without crashing with incorrect data object (to fix Test should fail on this)', () => {
//   const data = "not an array";
//
//   const component = renderer.create(
//     <ListTable data={data}/>
//   );
//
//   let tree = component.toJSON();
//
//   expect(tree).toMatchSnapshot();
// });
//

