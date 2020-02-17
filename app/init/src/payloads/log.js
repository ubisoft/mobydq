export const queryGetBatchLog = `query getBatchLog($batchId: Int!, $orderBy: [LogsOrderBy!]){
    batchById(id: $batchId) {
        status
        indicatorGroupId
    	indicatorGroupByIndicatorGroupId { name }
        logsByBatchId(orderBy: $orderBy) {
      		nodes {
                id
                createdDate
                fileName
                logLevel
                message
            }
        }
    }
}`;

export const queryGetSessionLog = `query getSessionLog($sessionId: Int!, $orderBy: [LogsOrderBy!]){
    sessionById(id: $sessionId){
        status
        batchId
        indicatorId
    	indicatorByIndicatorId {
            name
            indicatorTypeByIndicatorTypeId {
                name
            }
        }
    	logsBySessionId(orderBy: $orderBy){
            nodes {
                id
                createdDate
                fileName
                logLevel
                message
            }
        }
    }
}`;

export const queryGetDataSourceLog = `query getDataSourceLog($dataSourceId: Int!, $orderBy: [LogsOrderBy!]){
    dataSourceById(id: $dataSourceId){
    	name
    	dataSourceTypeByDataSourceTypeId { name }
        logsByDataSourceId(orderBy: $orderBy){
            nodes {
                id
                createdDate
                fileName
                logLevel
                message
      	    }
        }
    }
}`;
