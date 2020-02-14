const http = require("http");
const { postgraphile } = require("postgraphile");

const postgraphileOptions = {
    pgDefaultRole: "anonymous",
    jwtSecret: process.env.GRAPHQL_SECRET_KEY,
    jwtPgTypeIdentifier: "base.token",
    pgStrictFunctions: true,
    enableCors: true,
    graphiql: true,
    enhanceGraphiql: true,
    allowExplain: process.env.ALLOW_EXPLAIN,
    appendPlugins: [require("postgraphile-plugin-connection-filter"), require("mobydq-plugin")],
    additionalGraphQLContextFromRequest(req) {
        return {
            // This is needed to pass authorization header to PostGraphile context
            authorization: req.headers.authorization
        };
    }
};

// Create Http server running PostGraphile
http.createServer(postgraphile(process.env.GRAPHQL_DATABASE_URL, "base", postgraphileOptions)).listen(process.env.GRAPHQL_PORT);
