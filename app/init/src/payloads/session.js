export const queryGetAllSessions = `query getAllSessions($first: Int, $offset: Int, $orderBy: [SessionsOrderBy!]){
    allSessions(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            batchId
            id
            indicatorByIndicatorId {
                name
                indicatorGroupByIndicatorGroupId { name }
            }
            status
            createdDate
            updatedDate
            userByCreatedById { email }
        }
        totalCount
    }
}`;