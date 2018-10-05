import React from 'react'
import renderer from 'react-test-renderer';

import DataTable from './../Components/Dashboard/DataTable';



it('renders without crashing with normal data object', () => {
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

  const component = renderer.create(
    <DataTable data={data}/>
  );

  let tree = component.toJSON();

  expect(tree).toMatchSnapshot();

});

it('renders without crashing with incorrect data object (to fix Test should fail on this)', () => {
  const data = "not an array";

  const component = renderer.create(
    <DataTable data={data}/>
  );

  let tree = component.toJSON();

  expect(tree).toMatchSnapshot();
});


