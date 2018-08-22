import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import BaseDataView from './BaseDataView'

const Root = ({ store }) => (
  <Provider store={store}>
    <BrowserRouter>
      <BaseDataView/>
    </BrowserRouter>
  </Provider>
)

Root.propTypes = {
  store: PropTypes.object.isRequired
}

export default Root