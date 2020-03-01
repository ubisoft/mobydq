export const mutationKillBatch = `mutation killBatch($batchId: Int!) {
    killExecuteBatch (input: {batchId: $batchId}) {
        batch {
            id
            status
        }
    }
}`;

export const subscriptionGetBatchUpdates = `subscription getBatchUpdates {
    listen(topic: "batch") {
        relatedNode {
            ... on Batch {
                id
                status
              	sessionsByBatchId { totalCount }
            }
        }
    }
}`;
