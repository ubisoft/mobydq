import React from 'react';
import { render } from 'react-dom';
import Root from './Components/Base/Root'
import registerServiceWorker from './registerServiceWorker';
import configureStore from './store/configureStore'

const store = configureStore();

render( <Root store={store} />
, document.getElementById('root'));

