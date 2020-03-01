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

export const queryGetAllNotifications = `query getAllNotifications($orderBy: [NotificationsOrderBy!]) {
    allNotifications(orderBy: $orderBy, condition: { flagRead: false }) {
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

export const mutationMarkNotificationsAsRead = `mutation markNotificationsAsRead($id: Int!) {
    updateNotificationById(input: { id: $id, notificationPatch: { flagRead: true } }) {
        notification {
            id
        }
    }
}`;
