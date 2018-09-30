import React from 'react';
import ReactDOM from 'react-dom';
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
    const div = document.createElement('div');
    ReactDOM.render(<DataTable data={data}/>, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('renders without crashing with empty data object', () => {
  const data =
    [

    ];
  const div = document.createElement('div');
  ReactDOM.render(<DataTable data={data}/>, div);
  ReactDOM.unmountComponentAtNode(div);
});

//it('crashes when rendered without data', () => {
//  const div = document.createElement('div');
//  ReactDOM.render(<DataTable />, div);
//  ReactDOM.unmountComponentAtNode(div);
//});
