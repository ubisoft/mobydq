import ApolloClient from 'apollo-boost';


// TODO Re-use with PrivateRoute.js
function getCookieValue(key) {
    const valueMatch = document.cookie.match(`(^|;)\\s*${key}\\s*=\\s*([^;]+)`);
    return valueMatch ? valueMatch.pop() : '';
}

export default new ApolloClient({
    'uri': `${process.env.REACT_APP_FLASK_API_HOST}/mobydq/api/v1/graphql`,
    'headers': {
        'Authorization': `Bearer ${getCookieValue('token')}`
    }
    // Options: { mode: 'no-cors' }
});
