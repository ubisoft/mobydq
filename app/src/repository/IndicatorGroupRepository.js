import gql from "graphql-tag";

class IndicatorGroupRepository {
  static getListPage(pageNumber, pageLength) {
    return gql`
      {
        allIndicatorGroups {
          nodes {
            id
            name
            createdDate
            updatedDate
          }
        }
      }
    `
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
      mutation addNewIndicator($indicator: IndicatorInput!) {
        createIndicator(input: { indicator: $indicator }) {
          indicator {
            id
            name
            description
          }
        }
      }`
  }
}

export default IndicatorGroupRepository;