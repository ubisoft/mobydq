const http = require("http");
const { postgraphile } = require("postgraphile");

http.createServer(
    postgraphile(process.env.GRAPHQL_DATABASE_URL, "base", {
        graphiql: true,
        enhanceGraphiql: true,
        pgDefaultRole: "anonymous",
        jwtSecret: process.env.GRAPHQL_SECRET_KEY,
        jwtPgTypeIdentifier: "base.token",
        appendPlugins: [require("postgraphile-plugin-connection-filter")],
        enableCors: true
    })
).listen(process.env.GRAPHQL_PORT);
