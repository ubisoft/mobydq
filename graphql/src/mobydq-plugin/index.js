const { makeWrapResolversPlugin } = require("graphile-utils");

// Create custom resolver to test data source
const triggerTestDataSourceContainer = () => {
    return async (resolve, source, args, context, resolveInfo) => {
        // Let resolver execute against database
        const result = await resolve();

        // Capture parameters to run Docker container
        const authorization = context.authorization;
        const dataSourceId = result.data["@dataSource"]["id"];

        // Instantiate Docker
        var Docker = require("dockerode");
        var docker = new Docker({ socketPath: "/var/run/docker.sock" });

        // Run Docker container
        /*docker.run(
            "mobydq-scripts",
            ["python", "run.py", authorization, "test_data_source", dataSourceId],
            process.stdout,
            { HostConfig: { NetworkMode: "mobydq_network" } },
            function(err, data, container) {
                console.info("Container running");
            }
        );*/
        docker.createContainer(
            { Image: "mobydq-scripts", Tty: false, name: "mobydq-test-data-source-" + dataSourceId, HostConfig: { NetworkMode: "mobydq_network" } },
            function(err, container) {
                container.start();
            }
        );

        return result;
    };
};

// Register custom resolvers
module.exports = makeWrapResolversPlugin({
    Mutation: {
        testDataSource: triggerTestDataSourceContainer()
    }
});
