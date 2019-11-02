export const mutationAuthenticateUser = `mutation authenticateUser($userEmail: String!, $userPassword: String!) {
    authenticateUser(input: {userEmail: $userEmail, userPassword: $userPassword}) {
        sysToken
    }
}`;

export const queryGetCurrentUser = `query getCurrentUser($email: String!) {
    sysUserByEmail(email: $email) {
        email
        role
        sysUserGroupMembershipsByUserId{
            nodes {
                sysUserGroupByUserGroupId {
                    id
                    name
                }
            }
        }
    }
}`;
