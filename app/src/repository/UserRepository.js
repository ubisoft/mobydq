import gql from 'graphql-tag';


class UserRepository {
  static getListPage(pageNumber, pageSize) { // eslint-disable-line no-unused-vars
    return gql`
        query userRange($first: Int!, $offset: Int!, $orderBy: [UsersOrderBy!]) {
          allUsers(first: $first, offset: $offset, orderBy: $orderBy) {
            totalCount
            nodes {
              id
              email
              role
              flagActive
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
        query getUser($id: Int!) {
          userById(id: $id) {
          id
          email
          password
          role
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
    mutation addNewUser($user: UserInput!) {
      createUser(input: {user: $user}) {
        user{
          id
        }
      }
    }
    `;
  }

  // Todo not used, maybe remove?
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
      mutation updateUserById($userPatch: UserPatch!, $id: Int!) {
        updateIndicatorById(input: {userPatch: $userPatch, id: $id }) {
          user {
            id
          }
        }
      }
    `;
  }

  static delete() {
    return gql`
      mutation deleteUserById($id: Int!) {
        deleteUserById(input: {id: $id }) {
          user {
            id
          }
        }
      }
    `;
  }
}

export default UserRepository;
