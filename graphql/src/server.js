const http = require("http");
const { postgraphile } = require("postgraphile");

const postgraphileOptions = {
    graphiql: true,
    enhanceGraphiql: true,
    pgDefaultRole: "anonymous",
    jwtSecret: process.env.GRAPHQL_SECRET_KEY,
    jwtPgTypeIdentifier: "base.token",
    appendPlugins: [require("postgraphile-plugin-connection-filter"), require("mobydq-plugin")],
    enableCors: true,
    pgStrictFunctions: true,
    additionalGraphQLContextFromRequest(req) {
        return {
            authorization: req.headers.authorization // This is need to pass authorization header to PostGraphile context
        };
    }
};

// Create Http server running PostGraphile
http.createServer(postgraphile(process.env.GRAPHQL_DATABASE_URL, "base", postgraphileOptions)).listen(process.env.GRAPHQL_PORT);
