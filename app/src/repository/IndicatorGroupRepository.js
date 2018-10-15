import gql from 'graphql-tag';

class IndicatorGroupRepository {
  static getListPage(pageNumber, pageLength) { // eslint-disable-line no-unused-vars
    return gql`
      {
        allIndicatorGroups {
          nodes {
            id
            name
            updatedDate
          }
        }
      }
    `
  }

  static getFormDropdownData() {
    return gql`
      {
        allIndicatorGroups {
          nodes {
            id
            name
          }
        }
      }
    `
  }

  static display() {
    return gql`
        query getIndicatorGroup($id: Int!) {
          indicatorGroupById(id: $id) {
            id
            name
          }
        }
    `
  }

  static insert() {
    return gql`
      mutation addNewIndicatorGroup($indicatorGroup: IndicatorGroupInput!) {
        createIndicatorGroup(input: {indicatorGroup: $indicatorGroup}) {
          indicatorGroup {
            id
            name
            createdDate
            updatedDate
          }
        }
      }
    `
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
    `
  }
}

export default IndicatorGroupRepository;