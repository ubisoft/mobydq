export const queryGetAllSessions = `query getAllSessions($first: Int, $offset: Int, $orderBy: [SessionsOrderBy!]){
    allSessions(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            status
            indicatorId
            indicatorByIndicatorId { name }
            updatedDate
            userByCreatedById { email }
        }
        totalCount
    }
}`;