export const queryGetAllIndicators = `query getAllIndicators($first: Int, $offset: Int, $orderBy: [IndicatorsOrderBy!]) {
    allIndicators(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            name
            indicatorGroupId
            indicatorTypeByIndicatorTypeId { name }
            indicatorGroupByIndicatorGroupId { name }
            flagActive
        }
        totalCount
    }
}`;

export const queryGetIndicator = `query getIndicator($id: Int!, $first: Int, $offset: Int, $orderBy: [SessionsOrderBy!]) {
    indicatorById(id: $id) {
        id
        name
        description
        indicatorTypeId
        indicatorGroupId
        executionOrder
        flagActive
        parametersByIndicatorId {
            nodes {
                id
                parameterTypeId
                parameterTypeByParameterTypeId { name }
                value
                createdDate
                updatedDate
                userByCreatedById { email }
                userByUpdatedById { email }
            }
        }
        createdDate
        updatedDate
        userByCreatedById { email }
        userByUpdatedById { email }
        sessionsByIndicatorId(first: $first, offset: $offset, orderBy: $orderBy) {
            nodes {
                id
                status
                nbRecords
                nbRecordsAlert
                nbRecordsNoAlert
                batchId
                batchByBatchId { status }
            }
        }
    }
}`;

export const mutationCreateIndicator = `mutation createIndicator($indicator: IndicatorInput!) {
    createIndicator(input: {indicator: $indicator}) {
        indicator {
            id
        }
    }
}`;

export const mutationUpdateIndicator = `mutation updateIndicator($id: Int!, $indicatorPatch: IndicatorPatch!) {
    updateIndicatorById(input: {id: $id, indicatorPatch: $indicatorPatch }) {
        indicator {
            id
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

export const mutationDeleteIndicator = `mutation deleteIndicator($id: Int!) {
    deleteIndicatorById(input: {id: $id}) {
        indicator {
            id
        }
    }
}`;

export const mutationSearchIndicator = `mutation searchIndicator($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchIndicator(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        indicators {
            id
            name
            indicatorGroupId
            indicatorTypeByIndicatorTypeId { name }
            indicatorGroupByIndicatorGroupId { name }
            flagActive
        }
    }
}`;

export const mutationExecuteIndicator = `mutation executeBatch($indicatorGroupId: Int!, $indicatorId: [Int]) {
    executeBatch(input: {indicatorGroupId: $indicatorGroupId, indicatorId: $indicatorId}) {
        batch {
            id
            status
            sessionsByBatchId {
                nodes {
                    id
                    status
                    nbRecords
                    nbRecordsAlert
                    nbRecordsNoAlert
                }
            }
        }
    }
}`;

export const mutationDuplicateIndicator = `mutation mutationDuplicateIndicator($indicatorId: Int, $newIndicatorName: String) {
    duplicateIndicator(input: {indicatorId: $indicatorId, newIndicatorName: $newIndicatorName}) {
        indicator {
            id
        }
    }
}`;

export const queryGetIndicatorSessions = `query getAllSessions($indicatorId: Int, $first: Int, $offset: Int, $orderBy: [SessionsOrderBy!]){
    allSessions(condition: {indicatorId: $indicatorId}, first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            status
            nbRecords
            nbRecordsAlert
            nbRecordsNoAlert
          	createdDate
          	updatedDate
            userByCreatedById { email }  
        }
    }
}`;
