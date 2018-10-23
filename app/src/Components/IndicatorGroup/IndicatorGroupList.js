import React from 'react';

import { connect } from 'react-redux';
import { setIndicatorGroupPage, setIndicatorGroupRowsPerPage, setIndicatorGroupRowTotal } from './../../actions/indicatorGroupList';

import { Query } from 'react-apollo';
import IndicatorGroupRepository from './../../repository/IndicatorGroupRepository';

import ListTable from '../ListTable/ListTable';
import LinkButton from './../../Components/FormInput/LinkButton';

class IndicatorGroupList extends React.Component {
  render() {
    return (
      <Query
        query={IndicatorGroupRepository.getListPage()}
        variables={{ first: this.props.indicatorGroupRowsPerPage, offset: this.props.indicatorGroupPage * this.props.indicatorGroupRowsPerPage}}
        fetchPolicy={this.props.refetch ? 'cache-and-network' : 'cache-first'}
      >
        {({ loading, error, data }) => {
          if (loading) {
            return <p>Loading...</p>;
          }
          if (error) {
            return <p>Error ...</p>;
          }
          this.props.setIndicatorGroupRowTotal(data.allIndicatorGroups.totalCount)
          return (
            <div>
              <div style={{ 'float': 'left', 'marginLeft': '60px' }}>
                Indicator Groups
              </div>
              <div style={{ 'float': 'right' }}>
                <LinkButton disabled={false} label="Create" type="Create" color="primary"
                  variant="contained" to={'/indicator-group/new'}/>
              </div>
              <ListTable
                data={data.allIndicatorGroups.nodes}
                buttons={[{ 'function': 'edit', 'parameter': '/indicator-group' },
                          { 'function': 'delete', 'parameter': this._buildDeleteParam() }]}
                footerParams={this._buildFooterParam()}
              />
            </div>
          );
        }}
      </Query>
    );
  }

  _buildDeleteParam() {
    let deleteButtonParam = {
      page: this.props.indicatorGroupPage,
      rowTotal: this.props.indicatorGroupRowTotal,
      rowsPerPage: this.props.indicatorGroupRowsPerPage,
      setPage: this.props.setIndicatorGroupPage,
      repository: IndicatorGroupRepository
    };
    return deleteButtonParam;
  }

  _buildFooterParam() {
    let footerParam = {
      page: this.props.indicatorGroupPage,
      rowTotal: this.props.indicatorGroupRowTotal,
      rowsPerPage: this.props.indicatorGroupRowsPerPage,
      setPage: this.props.setIndicatorGroupPage,
      setRowsPerPage: this.props.setIndicatorGroupRowsPerPage
    };
    return footerParam;
  }
}

const mapStateToProps = (state) => ({
  'indicatorGroupPage': state.indicatorGroupPage,
  'indicatorGroupRowsPerPage': state.indicatorGroupRowsPerPage,
  'indicatorGroupRowTotal': state.indicatorGroupRowTotal
});

const mapDispatchToProps = (dispatch) => ({
  'setIndicatorGroupPage': (page) => dispatch(setIndicatorGroupPage(page)),
  'setIndicatorGroupRowsPerPage': (rowsPerPage) => dispatch(setIndicatorGroupRowsPerPage(rowsPerPage)),
  'setIndicatorGroupRowTotal': (rowTotal) => dispatch(setIndicatorGroupRowTotal(rowTotal))
});

export default connect(mapStateToProps, mapDispatchToProps)(IndicatorGroupList);

