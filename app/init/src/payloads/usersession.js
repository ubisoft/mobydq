export const mutationAuthenticateUser = `mutation authenticateUser($userEmail: String!, $userPassword: String!) {
    authenticateUser(input: {userEmail: $userEmail, userPassword: $userPassword}) {
        token
    }
}`;

export const queryGetCurrentUser = `query getCurrentUser($email: String!) {
    userByEmail(email: $email) {
        email
        role
    }
}`;
