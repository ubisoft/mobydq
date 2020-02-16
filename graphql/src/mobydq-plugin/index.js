const { makeWrapResolversPlugin } = require("graphile-utils");

// Create custom resolver to test data source
const runTestDataSourceContainer = () => {
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
            process.stdout,
            { name: "mobydq-test-data-source-" + dataSourceId, HostConfig: { AutoRemove: true, NetworkMode: "mobydq_network" } }, // Start options
            function(err, data, container) {
                // Do nothing
            }
        );

        return result;
    };
};

// Create custom resolver to execute batch of indicators
const runExecuteBatchContainer = () => {
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
            process.stdout,
            { name: "mobydq-batch-" + batchId, HostConfig: { AutoRemove: true, NetworkMode: "mobydq_network" } },
            function(err, data, container) {
                // Do nothing
            }
        );

        return result;
    };
};

// Create custom resolver to kill container
const killContainer = (containerName, objectId) => {
    return async (resolve, source, args, context, resolveInfo) => {
        // Instantiate Docker
        var Docker = require("dockerode");
        var docker = new Docker({ socketPath: "/var/run/docker.sock" });

        // Get Docker container
        const id = args.input[objectId];
        var container = docker.getContainer(containerName + id);

        // Test if container exists
        container.inspect(function(err, data) {
            if (data) {
                // Kill Docker container (container has autoremove set to true, no need to remove manually)
                container.kill(function(err, data) {
                    if (err) {
                        console.error(err);
                    }
                });
            } else if (err) {
                console.error(err);
            }
        });

        const result = await resolve();
        return result;
    };
};

// Register custom resolvers
module.exports = makeWrapResolversPlugin({
    Mutation: {
        testDataSource: runTestDataSourceContainer(),
        killTestDataSource: killContainer("mobydq-test-data-source-", "dataSourceId"),
        executeBatch: runExecuteBatchContainer(),
        killBatch: killContainer("mobydq-batch-", "batchId")
    }
});
