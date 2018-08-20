import React from 'react';
import { render } from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import BaseDataView from './Components/Base/BaseDataView'


render((
  <BrowserRouter>
    <BaseDataView/>
  </BrowserRouter>
), document.getElementById('root'));

