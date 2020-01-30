export const queryGetBatchLog = `query getBatchLog($batchId: Int, $orderBy: [LogsOrderBy!]){
    allLogs(condition: {batchId: $batchId}, orderBy: $orderBy) {
        nodes {
            id
            createdDate
            fileName
            logLevel
            message
        }
    }
}`;

export const queryGetSessionLog = `query getSessionLog($sessionId: Int, $orderBy: [LogsOrderBy!]){
    allLogs(condition: {sessionId: $sessionId}, orderBy: $orderBy) {
        nodes {
            id
            createdDate
            fileName
            logLevel
            message
        }
    }
}`;

export const queryGetDataSourceLog = `query getDataSourceLog($dataSourceId: Int, $orderBy: [LogsOrderBy!]){
    allLogs(condition: {dataSourceId: $dataSourceId}, orderBy: $orderBy) {
        nodes {
            id
            createdDate
            fileName
            logLevel
            message
        }
    }
}`;
