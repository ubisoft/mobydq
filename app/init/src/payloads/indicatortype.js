export const queryGetAllIndicatorTypes = `query getAllIndicatorTypes($first: Int, $offset: Int, $orderBy: [IndicatorTypesOrderBy!]){
    allIndicatorTypes(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            name
        }
        totalCount
    }
}`;

export const queryGetIndicatorType = `query getIndicatorType($id: Int!) {
    indicatorTypeById(id: $id) {
        id
        name
        createdDate
        updatedDate
        userByCreatedById { email }
        userByUpdatedById { email }
    }
}`;

export const mutationCreateIndicatorType = `mutation createIndicatorType($indicatorType: IndicatorTypeInput!) {
    createIndicatorType(input: {indicatorType: $indicatorType}) {
        indicatorType {
            id
        }
    }
}`;

export const mutationUpdateIndicatorType = `mutation updateIndicatorType($id: Int!, $indicatorTypePatch: IndicatorTypePatch!) {
    updateIndicatorTypeById(input: {id: $id, indicatorTypePatch: $indicatorTypePatch }) {
        indicatorType {
            id
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

export const mutationDeleteIndicatorType = `mutation deleteIndicatorType($id: Int!) {
    deleteIndicatorTypeById(input: {id: $id}) {
        indicatorType {
            id
        }
    }
}`;

export const mutationSearchIndicatorType = `mutation searchIndicatorType($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchIndicatorType(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        indicatorTypes {
            id
            name
        }
    }
}`;

// Response labels must be formatted according to Treeselect requirements
export const queryGetIndicatorTypes = `query getAllIndicatorTypes {
    allIndicatorTypes(orderBy: NAME_ASC) {
        nodes {
            id
            label:name
        }
    }
}`;
