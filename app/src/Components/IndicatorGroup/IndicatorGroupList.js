import React from 'react';

import { connect } from 'react-redux';
import { setPage, setRowsPerPage, setRowTotal } from './../../actions/listTable';

import { Query } from 'react-apollo';
import IndicatorGroupRepository from './../../repository/IndicatorGroupRepository';

import ListTable from '../ListTable/ListTable';
import LinkButton from './../../Components/FormInput/LinkButton';

class IndicatorGroupList extends React.Component {
  constructor(){
    super();
  }
  render() {
    return (
      <Query
        query={IndicatorGroupRepository.getListPage()}
        variables={{ first: this.props.rowsPerPage, offset: this.props.page * this.props.rowsPerPage}}
        fetchPolicy={this.props.refetch ? 'cache-and-network' : 'cache-first'}
      >
        {({ loading, error, data }) => {
          if (loading) {
            return <p>Loading...</p>;
          }
          if (error) {
            return <p>Error ...</p>;
          }
          this.props.setRowTotal(data.allIndicatorGroups.totalCount)
          return (
            <div>
              <div style={{ 'float': 'left', 'marginLeft': '60px' }}>
                Indicator Groups
              </div>
              <div style={{ 'float': 'right' }}>
                <LinkButton disabled={false} label="Create" type="Create" color="primary"
                  variant="contained" to={'/indicator-group/new'}/>
              </div>
              <ListTable data={data.allIndicatorGroups.nodes} buttons={[{ 'function': 'edit', 'parameter': '/indicator-group' }, { 'function': 'delete', 'parameter': IndicatorGroupRepository }]}/>
            </div>
          );
        }}
      </Query>
    );
  }
}
//const IndicatorGroupList = (refetch, page, rowsPerPage) => ;

const mapStateToProps = (state) => ({
  'page': state.page,
  'rowsPerPage': state.rowsPerPage,
  'rowTotal': state.rowTotal
});

const mapDispatchToProps = (dispatch) => ({
  'setPage': (page) => dispatch(setPage(page)),
  'setRowsPerPage': (rowsPerPage) => dispatch(setRowsPerPage(rowsPerPage)),
  'setRowTotal': (rowTotal) => dispatch(setRowTotal(rowTotal))
});

export default connect(mapStateToProps, mapDispatchToProps)(IndicatorGroupList);

