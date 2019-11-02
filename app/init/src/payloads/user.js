export const queryGetAllUsers = `query getAllUsers($first: Int, $offset: Int, $orderBy: [SysUsersOrderBy!]){
    allSysUsers(first: $first offset: $offset orderBy: $orderBy) {
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
    sysUserById(id: $id) {
        id
        email
        role
        flagActive
        sysUserGroupMembershipsByUserId {
            nodes {
                id
                userGroupId
                sysUserGroupByUserGroupId { name }
            }
        }
        createdDate
        updatedDate
        sysUserByCreatedById { email }
        sysUserByUpdatedById { email }
    }
}`;

export const mutationCreateUser = `mutation createUser($sysUser: SysUserInput!) {
    createSysUser(input: {sysUser: $sysUser}) {
        sysUser {
            id
        }
    }
}`;

export const mutationUpdateUser = `mutation updateUser($id: Int!, $sysUserPatch: SysUserPatch!) {
    updateSysUserById(input: {id: $id, sysUserPatch: $sysUserPatch}) {
        sysUser {
            id
            updatedDate
            sysUserByUpdatedById { email }
        }
    }
}`;

export const mutationCreatePassword = `mutation createPassword($sysPassword: SysPasswordInput!) {
    createSysPassword(input: {sysPassword: $sysPassword}) {
        sysPassword {
            id
        }
    }
}`;

export const mutationUpdatePassword = `mutation updatePassword($userId: Int!, $sysPasswordPatch: SysPasswordPatch!) {
    updateSysPasswordByUserId(input: {userId: $userId, sysPasswordPatch: $sysPasswordPatch}) {
        sysPassword {
            id
            updatedDate
            sysUserByUpdatedById { email }
        }
    }
}`;

export const mutationSearchUser = `mutation searchUser($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchUser(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        sysUsers {
            id
            email
            role
            flagActive
        }
    }
}`;

export const mutationCreateUserGroupMembership = `mutation createUserGroupMembership($sysUserGroupMembership: SysUserGroupMembershipInput!) {
    createSysUserGroupMembership(input: {sysUserGroupMembership: $sysUserGroupMembership}) {
        sysUserGroupMembership {
            id
            userGroupId
            sysUserGroupByUserGroupId { name }
        }
    }
}`;

export const mutationDeleteUserGroupMembership = `mutation deleteUserGroupMembership($id: Int!) {
    deleteSysUserGroupMembershipById(input: {id: $id}){
        sysUserGroupMembership {
            id
        }
    }
}`;
