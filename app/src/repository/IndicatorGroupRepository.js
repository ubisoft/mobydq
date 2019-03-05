import gql from 'graphql-tag';

class IndicatorGroupRepository {
  static getListPage() { // eslint-disable-line no-unused-vars
    return gql`
        query indicatorGroupRange($first: Int!, $offset: Int!, $orderBy: [IndicatorGroupsOrderBy!]) {
          allIndicatorGroups(first: $first, offset: $offset, orderBy: $orderBy) {
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
        allUserGroups {
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
            userGroupId
            createdDate
            userByCreatedById { email }
            updatedDate
            userByUpdatedById { email }
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
          }
        }
      }
    `;
  }

  static delete() {
    return gql`
      mutation deleteIndicatorGroupById($id: Int!) {
        deleteIndicatorGroupById(input: { id: $id }) {
          indicatorGroup {
            id
          }
        }
      }
    `;
  }

  static execute() {
    return gql`
      mutation executeBatch($id: Int!) {
        executeBatch(input: { indicatorGroupId: $id }) {
          batch {
            id
            status
          }
        }
      }
    `;
  }
}

export default IndicatorGroupRepository;
