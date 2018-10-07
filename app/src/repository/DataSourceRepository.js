import gql from "graphql-tag";

class DataSourceRepository {
  static getListPage(pageNumber, pageSize) {
    return gql`
      {
        allDataSources {
          nodes {
            id
            name
            dataSourceTypeByDataSourceTypeId {
              name
            }
            connectivityStatus
            updatedDate
          }
        }
      }
    `
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
    `
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
    `
  }
}

export default DataSourceRepository;