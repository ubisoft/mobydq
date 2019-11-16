export const queryGetAllDataSourceTypes = `query getAllDataSourceTypes {
    allDataSourceTypes(orderBy: NAME_ASC) {
        nodes {
            id
            name
        }
    }
}`;

// Response labels must be formatted according to Treeselect requirements
export const queryGetDataSourceTypes = `query getAllDataSourceTypes {
    allDataSourceTypes(orderBy: NAME_ASC) {
        nodes {
            id
            label:name
        }
    }
}`;