import gql from 'graphql-tag';

class DataSourceRepository {
  static getListPage(pageNumber, pageSize) { // eslint-disable-line no-unused-vars
    return gql`
      query dataSourceRange($first: Int!, $offset: Int!, $orderBy: [DataSourcesOrderBy!]) {
        allDataSources(first: $first, offset: $offset, orderBy: $orderBy) {
          totalCount
          nodes {
            id
            name
            dataSourceTypeId
            updatedDate
          }
        }
      }
    `;
  }

  static display() {
    return gql`
        query getDataSource($id: Int!) {
          dataSourceById(id: $id) {
            id
            name
            dataSourceTypeId
            connectionString
            login
            password
          }
        }
    `;
  }

  static getFormDropdownData() {
    return gql`
      {
        allDataSourceTypes {
          nodes {
            id
            name
          }
        }
      }
    `;
  }

  static insert() {
    return gql`
      mutation addNewDataSource($dataSource: DataSourceInput!) {
        createDataSource(input: {dataSource: $dataSource}) {
          dataSource {
            id
            name
          }
        }
      }
    `;
  }

  static update() {
    return gql`
      mutation updateDataSourceById($dataSourcePatch: DataSourcePatch!, $id: Int!) {
        updateDataSourceById(input: {dataSourcePatch: $dataSourcePatch, id: $id }) {
          dataSource {
            id
            name
          }
        }
      }
    `;
  }

  static delete() {
    return gql`
      mutation deleteDataSourceById($id: Int!) {
        deleteDataSourceById(input: {id: $id }) {
          dataSource {
            id
            name
          }
        }
      }
    `;
  }
}

export default DataSourceRepository;
