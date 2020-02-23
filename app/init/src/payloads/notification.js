export const subscriptionGetNotification = `subscription getNotifications {
    listen(topic: "notification") {
        relatedNode {
            ... on Notification {
                id
                message
                flagRead
                createdDate
                batchId
                dataSourceId
                dataSourceByDataSourceId { name }
                status
            }
        }
    }
}`;

export const queryGetAllNotifications = `query getAllNotifications($first: Int, $offset: Int, $orderBy: [NotificationsOrderBy!]) {
    allNotifications(first: $first, offset: $offset, orderBy: $orderBy, condition: { flagRead: false }) {
        nodes {
            id
            message
            flagRead
            createdDate
            batchId
            dataSourceId
            dataSourceByDataSourceId { name }
            status
        }
        totalCount
    }
}`;

export const mutationMarkAllNotificationsAsRead = `mutation markAllNotificationsAsRead {
    markAllNotificationsAsRead(input:{}) {
        notifications {
            id
        }
    }
}`;
