import gql from 'graphql-tag';

class IndicatorRepository {
  static getListPage(pageNumber, pageSize) { // eslint-disable-line no-unused-vars
    return gql`
      {
        allIndicators {
          nodes {
            id
            name
            indicatorTypeId
            indicatorGroupId
            executionOrder
            flagActive
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
      }
    `
  }

  static display() {
    return gql`
        query getIndicator($id: Int!) {
          indicatorById(id: $id) {
            id
            name
            description
            indicatorTypeId
            indicatorGroupId
            executionOrder
            flagActive
            updatedDate
          }
        }
    `
  }

  static insert() {
    return gql`
      mutation addNewIndicator($indicator: IndicatorInput!) {
        createIndicator(input: {indicator: $indicator}) {
          indicator {
            id
            name
            description
          }
        }
      }
    `
  }

  static getIndicatorToUpdate(id) {
    return gql`
      {
        indicatorById(id:` + id + `) {
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
    `
  }

  static update() {
    return gql`
      mutation updateIndicator($id: Int!, $indicatorPatch: IndicatorPatch!) {
        updateIndicatorById(input: {id: $id, indicatorPatch: $indicatorPatch}) {
          indicator {
            id
          }
        }
      }
    `
  }
}

export default IndicatorRepository;