export const queryGetAllIndicatorGroups = `query getAllIndicatorGroups($first: Int, $offset: Int, $orderBy: [IndicatorGroupsOrderBy!]){
    allIndicatorGroups(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            name
        }
        totalCount
    }
}`;

export const queryGetIndicatorGroup = `query getIndicatorGroup($id: Int!) {
    indicatorGroupById(id: $id) {
        id
        name
        createdDate
        updatedDate
        userByCreatedById { email }
        userByUpdatedById { email }
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

// Response labels must be formatted according to Treeselect requirements
export const queryGetIndicatorGroups = `query getAllIndicatorGroups {
    allIndicatorGroups(orderBy: NAME_ASC) {
        nodes {
            id
            label:name
        }
    }
}`;
