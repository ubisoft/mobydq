export const queryGetAllSessions = `query getAllSessions($first: Int, $offset: Int, $orderBy: [SessionsOrderBy!]){
    allSessions(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            status
            indicatorId
            indicatorByIndicatorId { name }
            batchId
            batchByBatchId {
                status
                indicatorGroupId
            }
            updatedDate
            userByCreatedById { email }
        }
        totalCount
    }
}`;

export const mutationSearchSession = `mutation searchSession($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchSession(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        sessions {
            id
            status
            indicatorId
            indicatorByIndicatorId { name }
            batchId
            batchByBatchId {
                status
                indicatorGroupId
            }
            updatedDate
            userByCreatedById { email }
        }
    }
}`;
