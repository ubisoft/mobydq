import gql from "graphql-tag";

class IndicatorRepository {
  static getIndicatorListByPage(pageNumber, pageLength) {
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
}

export default IndicatorRepository;