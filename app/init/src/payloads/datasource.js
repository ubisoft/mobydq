export const queryGetAllDataSources = `query getAllDataSources($first: Int, $offset: Int, $orderBy: [DataSourcesOrderBy!]){
    allDataSources(first: $first, offset: $offset, orderBy: $orderBy) {
        nodes {
            id
            name
            dataSourceTypeByDataSourceTypeId { name }
          	connectivityStatus
        }
        totalCount
    }
}`;

export const queryGetDataSource = `query getDataSource($id: Int!) {
    dataSourceById(id: $id) {
        id
        name
        dataSourceTypeId
        connectionString
        login
        connectivityStatus
        createdDate
        updatedDate
        userByCreatedById { email }
        userByUpdatedById { email }
    }
}`;

export const mutationCreateDataSource = `mutation createDataSource($dataSource: DataSourceInput!) {
    createDataSource(input: {dataSource: $dataSource}) {
        dataSource {
            id
        }
    }
}`;

export const mutationUpdateDataSource = `mutation updateDataSource($id: Int!, $dataSourcePatch: DataSourcePatch!) {
    updateDataSourceById(input: {id: $id, dataSourcePatch: $dataSourcePatch }) {
        dataSource {
            id
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

export const mutationDeleteDataSource = `mutation deleteDataSource($id: Int!) {
    deleteDataSourceById(input: {id: $id}){
        dataSource {
            id
        }
    }
}`;

export const mutationSearchDataSource = `mutation searchDataSource($searchKeyword: String, $sortAttribute: String, $sortOrder: String) {
    searchDataSource(input: {searchKeyword: $searchKeyword, sortAttribute: $sortAttribute, sortOrder: $sortOrder}) {
        dataSources {
            id
            name
            dataSourceTypeByDataSourceTypeId { name }
          	connectivityStatus
        }
    }
}`;

export const mutationTestDataSource = `mutation testDataSource($dataSourceId: Int!) {
    testDataSource(input: {dataSourceId: $dataSourceId}){
        dataSource {
            id
            connectivityStatus
            updatedDate
            userByUpdatedById { email }
        }
    }
}`;

// Response labels must be formatted according to Treeselect requirements
export const queryGetDataSources = `query getAllDataSources {
    allDataSources(orderBy: NAME_ASC) {
        nodes {
            id:name
            label:name
        }
    }
}`;

export const subscriptionGetDataSourceUpdates = `subscription getDataSourceUpdates {
    listen(topic: "dataSource") {
        relatedNode {
            ... on DataSource {
                id
                name
                dataSourceTypeId
                dataSourceTypeByDataSourceTypeId { name }
                connectionString
                login
                connectivityStatus
                createdDate
                updatedDate
                userByCreatedById { email }
                userByUpdatedById { email }
            }
        }
    }
}`;
