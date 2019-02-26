import React from 'react';

import { Query } from 'react-apollo';
import { GraphQLError } from './../Error/GraphQLError';

import ListTable from '../ListTable/ListTable';
import AddIcon from '@material-ui/icons/Add';
import Fab from '@material-ui/core/Fab/Fab';

class ListContainer extends React.Component {
  renderForm(data) {
    this.props.setRowTotal(data[this.props.dataObjectName].totalCount);
    return <div>
      <div style={{ 'float': 'left', 'marginLeft': '50px' }}>
        {this.props.tableHeader}
      </div>
      <div style={{ 'float': 'right' }}>
        <Fab color="secondary" to={this.props.newLink} variant="round">
          <AddIcon />
        </Fab>
      </div>
      <ListTable
        data={data[this.props.dataObjectName].nodes}
        buttons={this.props.buttons}
        {...this.props}
      />
    </div>;
  }

  render() {
    return (
      <Query
        query={this.props.repository.getListPage()}
        variables={{ 'first': this.props.rowsPerPage, 'offset': this.props.page * this.props.rowsPerPage, 'orderBy': this.props.sortColumn }}
        fetchPolicy={this.props.refetch ? 'cache-and-network' : 'cache-first'}
      >
        {({ loading, error, data }) => {
          if (loading) {
            // Check if we already have data object so we would not remove the old data before we get the new one.
            if (Object.keys(data).length) {
              return this.renderForm(data);
            }
            return <p>Loading...</p>;
          }
          if (error) {
            return <GraphQLError error={error} />;
          }
          return this.renderForm(data);
        }}
      </Query>
    );
  }
}

export default ListContainer;
