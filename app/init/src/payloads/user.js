export const queryGetAllUsers = `query getAllUsers($first: Int, $offset: Int, $orderBy: [UsersOrderBy!]){
    allUsers(first: $first offset: $offset orderBy: $orderBy) {
        nodes {
            id
            email
            role
            flagActive
        }
        totalCount
    }
}`;

export const queryGetUser = `query getUser($id: Int!) {
    userById(id: $id) {
        id
        email
        role
        flagActive
        userGroupMembershipsByUserId {
            nodes {
                id
                userGroupId
                userGroupByUserGroupId { name }
            }
        }
        createdDate
        updatedDate
        userByCreatedById { email }
        userByUpdatedById { email }
    }
}`;

export const mutationCreateUser = `mutation createUser($user: UserInput!) {
    createUser(input: {user: $user}) {
        user {
            id
        }
    }
}`;

export const mutationUpdateUser = `mutation updateUser($id: Int!, $userPatch: UserPatch!) {
    updateUserById(input: {id: $id, userPatch: $userPatch}) {
        user {
            id
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

export const mutationCreatePassword = `mutation createPassword($password: PasswordInput!) {
    createPassword(input: {password: $password}) {
        password {
            id
        }
    }
}`;

export const mutationUpdatePassword = `mutation updatePassword($userId: Int!, $passwordPatch: PasswordPatch!) {
    updatePasswordByUserId(input: {userId: $userId, passwordPatch: $passwordPatch}) {
        password {
            id
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

export const mutationSearchUser = `mutation searchUser($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchUser(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        users {
            id
            email
            role
            flagActive
        }
    }
}`;

export const mutationCreateUserGroupMembership = `mutation createUserGroupMembership($userGroupMembership: UserGroupMembershipInput!) {
    createUserGroupMembership(input: {userGroupMembership: $userGroupMembership}) {
        userGroupMembership {
            id
            userGroupId
            userGroupByUserGroupId { name }
        }
    }
}`;

export const mutationDeleteUserGroupMembership = `mutation deleteUserGroupMembership($id: Int!) {
    deleteUserGroupMembershipById(input: {id: $id}){
        userGroupMembership {
            id
        }
    }
}`;
