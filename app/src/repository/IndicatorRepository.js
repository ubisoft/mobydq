import gql from "graphql-tag";

class IndicatorRepository {
  static getListPage(pageNumber, pageSize) {
    return gql`{
      allIndicators{
        nodes {
          id
          name
          description
          executionOrder
          flagActive
          createdDate
          updatedDate
          indicatorTypeId
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

export default IndicatorRepository;