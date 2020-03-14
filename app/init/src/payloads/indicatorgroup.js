export const queryGetAllIndicatorGroups = `query getAllIndicatorGroups($first: Int, $offset: Int, $orderBy: [IndicatorGroupsOrderBy!]){
    allIndicatorGroups(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            name
        }
        totalCount
    }
}`;

export const queryGetIndicatorGroup = `query getIndicatorGroup($id: Int!, $first: Int, $offset: Int, $orderBy: [BatchesOrderBy!]) {
    indicatorGroupById(id: $id) {
        id
        name
        createdDate
        updatedDate
        userByCreatedById { email }
        userByUpdatedById { email }
        indicatorsByIndicatorGroupId {
            nodes {
                id
                name
                indicatorTypeByIndicatorTypeId { name }
                flagActive
            }
        }
        batchesByIndicatorGroupId(first: $first, offset: $offset, orderBy: $orderBy) {
            nodes {
                id
                status
                sessionsByBatchId { totalCount }
            }
        }
    }
}`;

export const mutationCreateIndicatorGroup = `mutation createIndicatorGroup($indicatorGroup: IndicatorGroupInput!) {
    createIndicatorGroup(input: {indicatorGroup: $indicatorGroup}) {
        indicatorGroup {
            id
        }
    }
}`;

export const mutationUpdateIndicatorGroup = `mutation updateIndicatorGroup($id: Int!, $indicatorGroupPatch: IndicatorGroupPatch!) {
    updateIndicatorGroupById(input: {id: $id, indicatorGroupPatch: $indicatorGroupPatch }) {
        indicatorGroup {
            id
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

export const mutationDeleteIndicatorGroup = `mutation deleteIndicatorGroup($id: Int!) {
    deleteIndicatorGroupById(input: {id: $id}) {
        indicatorGroup {
            id
        }
    }
}`;

export const mutationSearchIndicatorGroup = `mutation searchIndicatorGroup($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchIndicatorGroup(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        indicatorGroups {
            id
            name
        }
    }
}`;

export const mutationExecuteIndicatorGroup = `mutation executeBatch($indicatorGroupId: Int!) {
    executeBatch(input: {indicatorGroupId: $indicatorGroupId}) {
        batch {
            id
            status
            sessionsByBatchId { totalCount }
        }
    }
}`;

// Response labels must be formatted according to Treeselect requirements
export const queryGetIndicatorGroups = `query getAllIndicatorGroups {
    allIndicatorGroups(orderBy: NAME_ASC) {
        nodes {
            id
            label:name
        }
    }
}`;
