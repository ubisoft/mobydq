export const mutationKillBatch = `mutation killBatch($batchId: Int!) {
    killExecuteBatch (input: {batchId: $batchId}) {
        batch {
            id
            status
        }
    }
}`;
