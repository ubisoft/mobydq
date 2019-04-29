import gql from 'graphql-tag';

class UserGroupRepository {
  static getListPage(pageNumber, pageSize) { // eslint-disable-line no-unused-vars
    return gql`
      query userGroupRange($first: Int!, $offset: Int!, $orderBy: [UserGroupsOrderBy!]) {
        allUserGroups(first: $first, offset: $offset, orderBy: $orderBy) {
          totalCount
          nodes {
            id
            name
            createdDate
            updatedDate
            createdById
            updatedById
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
      }
    `;
  }

  static display() {
    return gql`
        query getUserGroup($id: Int!) {
          userGroupById(id: $id) {
            id
            name
            createdDate
            updatedDate
            userByCreatedById { email }
            userByUpdatedById { email }
          }
        }
    `;
  }

  static insert() {
    return gql`
      mutation addNewUserGroup($userGroup: UserGroupInput!) {
        createUserGroup(input: {userGroup: $userGroup}) {
          userGroup {
            id
          }
        }
      }
    `;
  }

  static getUserGroupToUpdate(id) {
    return `${gql`
      {
        userGroupById(id:` + id}) {
            id
            name
            updatedDate
            updatedById
        }
      }
    `;
  }

  static update() {
    return gql`
      mutation updateUserGroupById($userGroupPatch: UserGroupPatch!, $id: Int!) {
        updateIndicatorById(input: {userGroupPatch: $userGroupPatch, id: $id }) {
          userGroup {
            id
          }
        }
      }
    `;
  }

  static delete() {
    return gql`
      mutation deleteUserGroupById($id: Int!) {
        deleteUserGroupById(input: {id: $id }) {
          userGroup {
            id
          }
        }
      }
    `;
  }
}

export default UserGroupRepository;
