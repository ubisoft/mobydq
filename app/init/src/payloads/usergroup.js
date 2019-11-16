export const queryGetAllUserGroups = `query getAllUserGroups($first: Int, $offset: Int, $orderBy: [UserGroupsOrderBy!]){
    allUserGroups(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            name
        }
        totalCount
    }
}`;

export const queryGetUserGroup = `query getUserGroup($id: Int!) {
    userGroupById(id: $id) {
        id
        name
        createdDate
        updatedDate
        userByCreatedById { email }
        userByUpdatedById { email }
    }
}`;

// Query to get the list of user groups for the dropdown list in user form
// Response labels must be formatted according to Treeselect requirements
export const queryGetUserUserGroups = `query getAllUserGroups {
    allUserGroups(orderBy: NAME_ASC) {
        nodes {
            id
            label:name
        }
    }
}`;

export const mutationCreateUserGroup = `mutation createUserGroup($userGroup: UserGroupInput!) {
    createUserGroup(input: {userGroup: $userGroup}) {
        userGroup {
            id
        }
    }
}`;

export const mutationUpdateUserGroup = `mutation updateUserGroup($id: Int!, $userGroupPatch: UserGroupPatch!) {
    updateUserGroupById(input: {id: $id, userGroupPatch: $userGroupPatch }) {
        userGroup {
            id
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

export const mutationSearchUserGroup = `mutation searchUserGroup($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchUserGroup(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        userGroups {
            id
            name
        }
    }
}`;
