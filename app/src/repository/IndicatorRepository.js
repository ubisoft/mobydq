import gql from 'graphql-tag';

class IndicatorRepository {
  static getListPage(pageNumber, pageSize) { // eslint-disable-line no-unused-vars
    return gql`
      query indicatorRange($first: Int!, $offset: Int!, $orderBy: [IndicatorsOrderBy!]) {
        allIndicators(first: $first, offset: $offset, orderBy: $orderBy) {
          totalCount
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
    `;
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
    `;
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
    `;
  }

  static insert() {
    return gql`
      mutation addNewIndicator($indicator: IndicatorInput!) {
        createIndicator(input: {indicator: $indicator}) {
          indicator {
            id
          }
        }
      }
    `;
  }

  static getIndicatorToUpdate(id) {
    return `${gql`
      {
        indicatorById(id:` + id}) {
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
    `;
  }

  static update() {
    return gql`
      mutation updateIndicatorById($indicatorPatch: IndicatorPatch!, $id: Int!) {
        updateIndicatorById(input: {indicatorPatch: $indicatorPatch, id: $id }) {
          indicator {
            id
          }
        }
      }
    `;
  }

  static delete() {
    return gql`
      mutation deleteIndicatorById($id: Int!) {
        deleteIndicatorById(input: {id: $id }) {
          indicator {
            id
          }
        }
      }
    `;
  }
}

export default IndicatorRepository;
