import React from 'react';

import { connect } from 'react-redux';
import { setDataSourcePage, setDataSourceRowsPerPage, setDataSourceRowTotal } from './../../actions/dataSourceList';

import { Query } from 'react-apollo';
import GraphQLError from './../Error/GraphQLError';

import DataSourceRepository from './../../repository/DataSourceRepository';
import ListTable from '../ListTable/ListTable';
import LinkButton from './../../Components/FormInput/LinkButton';


class DataSourceList extends React.Component {
  render() {
    return (
      <Query
        query={DataSourceRepository.getListPage()}
        variables={{ 'first': this.props.dataSourceRowsPerPage, 'offset': this.props.dataSourcePage * this.props.dataSourceRowsPerPage }}
        fetchPolicy={this.props.refetch ? 'cache-and-network' : 'cache-first'}
      >
        {({ loading, error, data }) => {
          if (loading) {
            return <p>Loading...</p>;
          }
          if (error) {
            return <GraphQLError error={error}/>;
          }
          this.props.setDataSourceRowTotal(data.allDataSources.totalCount);
          return (
            <div>
              <div style={{ 'float': 'left', 'marginLeft': '60px' }}>
                Data Sources
              </div>
              <div style={{ 'float': 'right' }}>
                <LinkButton disabled={false} label="Create" type="Create" color="primary"
                  variant="contained" to={'/data-source/new'}/>
              </div>
              <ListTable
                data={data.allDataSources.nodes}
                buttons={[
                  { 'function': 'edit', 'parameter': '/data-source' },
                  { 'function': 'delete', 'parameter': this._buildDeleteParam() }
                ]}
                footerParams={this._buildFooterParam()}
              />
            </div>
          );
        }}
      </Query>
    );
  }

  _buildDeleteParam() {
    return {
      'page': this.props.dataSourcePage,
      'rowTotal': this.props.dataSourceRowTotal,
      'rowsPerPage': this.props.dataSourceRowsPerPage,
      'setPage': this.props.setDataSourcePage,
      'repository': DataSourceRepository
    };
  }

  _buildFooterParam() {
    return {
      'page': this.props.dataSourcePage,
      'rowTotal': this.props.dataSourceRowTotal,
      'rowsPerPage': this.props.dataSourceRowsPerPage,
      'setPage': this.props.setDataSourcePage,
      'setRowsPerPage': this.props.setDataSourceRowsPerPage
    };
  }
}

const mapStateToProps = (state) => ({
  'dataSourcePage': state.dataSourcePage,
  'dataSourceRowsPerPage': state.dataSourceRowsPerPage,
  'dataSourceRowTotal': state.dataSourceRowTotal
});

const mapDispatchToProps = (dispatch) => ({
  'setDataSourcePage': (page) => dispatch(setDataSourcePage(page)),
  'setDataSourceRowsPerPage': (rowsPerPage) => dispatch(setDataSourceRowsPerPage(rowsPerPage)),
  'setDataSourceRowTotal': (rowTotal) => dispatch(setDataSourceRowTotal(rowTotal))
});

export default connect(mapStateToProps, mapDispatchToProps)(DataSourceList);

