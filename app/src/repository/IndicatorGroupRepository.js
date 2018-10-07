import gql from "graphql-tag";

class IndicatorGroupRepository {
  static getListPage(pageNumber, pageLength) {
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
}

export default IndicatorGroupRepository;