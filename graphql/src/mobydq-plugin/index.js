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
        docker.run(
            "mobydq-scripts",
            ["python", "run.py", authorization, "test_data_source", dataSourceId.toString()],
            [process.stdout, process.stderr],
            { name: "mobydq-test-data-source-" + dataSourceId, tty: false, HostConfig: { NetworkMode: "mobydq_network" } },
            function(err, data, container) {
                container.remove();
            }
        );

        return result;
    };
};

// Create custom resolver to execute batch of indicators
const triggerExecuteBatchContainer = () => {
    return async (resolve, source, args, context, resolveInfo) => {
        // Let resolver execute against database
        const result = await resolve();

        // Capture parameters to run Docker container
        const authorization = context.authorization;
        const batchId = result.data["@batch"]["id"];

        // Instantiate Docker
        var Docker = require("dockerode");
        var docker = new Docker({ socketPath: "/var/run/docker.sock" });

        // Run Docker container
        docker.run(
            "mobydq-scripts",
            ["python", "run.py", authorization, "execute_batch", batchId.toString()],
            [process.stdout, process.stderr],
            { name: "mobydq-batch-" + batchId, tty: false, HostConfig: { NetworkMode: "mobydq_network" } },
            function(err, data, container) {
                container.remove();
            }
        );

        return result;
    };
};

// Register custom resolvers
module.exports = makeWrapResolversPlugin({
    Mutation: {
        testDataSource: triggerTestDataSourceContainer(),
        executeBatch: triggerExecuteBatchContainer()
    }
});
