import gql from 'graphql-tag';

class IndicatorGroupRepository {
  static getListPage() { // eslint-disable-line no-unused-vars
    return gql`
        query indicatorGroupRange($first: Int!, $offset: Int!) {
          allIndicatorGroups(first: $first, offset: $offset) {
            totalCount
            nodes {
              id
              name
              updatedDate
            }
          }
        }
    `;
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
    `;
  }

  static display() {
    return gql`
        query getIndicatorGroup($id: Int!) {
          indicatorGroupById(id: $id) {
            id
            name
          }
        }
    `;
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
    `;
  }

  static update() {
    return gql`
      mutation updateIndicatorGroupById($indicatorGroupPatch: IndicatorGroupPatch!, $id: Int!) {
        updateIndicatorGroupById(input: {indicatorGroupPatch: $indicatorGroupPatch, id: $id }) {
          indicatorGroup {
            id
            name
          }
        }
      }
    `;
  }

  static delete() {
    return gql`
      mutation deleteIndicatorGroupById($id: Int!) {
        deleteIndicatorGroupById(input: {id: $id }) {
          indicatorGroup {
            id
            name
          }
        }
      }
    `;
  }
}

export default IndicatorGroupRepository;
