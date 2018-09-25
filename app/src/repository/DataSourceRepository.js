import gql from "graphql-tag";

class DataSourceRepository {
  static getListPage(pageNumber, pageSize) {
    return gql`
      {
        allDataSources {
          nodes{
            id
            name
            createdDate
            updatedDate
            connectionString
            login
            dataSourceTypeId
          }
        }
      }`
  }

  static getFormDropdownData() {
    return gql`
      {
        allIndicatorTypes {
          nodes {
            id
            name
          }
        }
        allIndicatorGroups {
          nodes {
            id
            name
          }
        }
      }`
  }

  static insert() {
    return gql`
      mutation addNewDataSource($dataSource: DataSourceInput!) {
        createDataSource(input: { dataSource: $dataSource }) {
          dataSource {
            id
            name
          }
        }
      }`
  }
}

export default DataSourceRepository;