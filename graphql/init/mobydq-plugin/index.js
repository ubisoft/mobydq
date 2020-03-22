const { makeWrapResolversPlugin } = require("graphile-utils");

// Create custom resolver to test data source
const runTestDataSourceContainer = () => {
    return {
        // Get data source id from the database
        requires: {
            childColumns: [{ column: "id", alias: "$data_source_id" }],
        },
        async resolve(resolve, _source, _args, _context, _resolveInfo) {
            // Let resolver execute against database
            const result = await resolve();

            // Capture parameters to run Docker container
            const authorization = _context.authorization;
            const dataSourceId = result.data.$data_source_id;

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
        }
    };
};

// Create custom resolver to execute batch of indicators
const runExecuteBatchContainer = () => {
    return {
        // Get batch id from the database
        requires: {
            childColumns: [{ column: "id", alias: "$batch_id" }],
        },
        async resolve(resolve, _source, _args, _context, _resolveInfo) {
            // Let resolver execute against database
            const result = await resolve();

            // Capture parameters to run Docker container
            const authorization = _context.authorization;
            const batchId = result.data.$batch_id;

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
        }
    };
};

// Create custom resolver to kill container
const killContainer = (containerName, objectId) => {
    return async (resolve, source, args, context, resolveInfo) => {
        // Instantiate Docker
        var Docker = require("dockerode");
        var docker = new Docker({ socketPath: "/var/run/docker.sock" });

        // Get Docker container name based on data source or batch Id
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
        killExecuteBatch: killContainer("mobydq-batch-", "batchId")
    }
});
