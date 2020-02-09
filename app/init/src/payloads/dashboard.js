export const queryGetNbIndicators = `query getNbIndicators {
    allNbIndicators {
        nodes {
            flagActive
            indicatorType
            nbIndicators
        }
    }
}`;

export const queryGetLastSessions = `query queryGetLastSessions($date: Datetime) {
    allSessionStatuses(orderBy: CREATED_DATE_ASC, filter: { createdDate: { greaterThanOrEqualTo: $date } }) {
        nodes {
            id
            indicatorId
            indicator
            indicatorType
            status
            createdDate
            qualityLevel
            durationMinutes
            duration {
                seconds
                minutes
                hours
                days
                months
                years
            }
        }
    }
}`;
