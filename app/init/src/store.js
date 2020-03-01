import Vue from "vue";
import Vuex from "vuex";
import * as UserPayload from "./payloads/user";
import * as UserGroupPayload from "./payloads/usergroup";
import * as UserSession from "./payloads/usersession";
import * as DataSourcePayload from "./payloads/datasource";
import * as DataSourceTypePayload from "./payloads/datasourcetype";
import * as IndicatorGroupPayload from "./payloads/indicatorgroup";
import * as IndicatorPayload from "./payloads/indicator";
import * as IndicatorTypePayload from "./payloads/indicatortype";
import * as LogPayload from "./payloads/log";
import * as NotificationPayload from "./payloads/notification";
import * as ParameterPayload from "./payloads/parameter";
import * as SessionPayload from "./payloads/session";
import * as BatchPayload from "./payloads/batch";
import * as DashboardPayload from "./payloads/dashboard";

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    graphqlUrl: "/graphql",

    // Error message
    errorObject: {
      flag: false,
      message: ""
    },

    // Session
    currentUser: {
      isAuthenticated: false, // Used to customize UI display
      role: "anonymous" // Used to customize UI display
    },

    // Websocket
    websocket: {
      isConnected: false,
      message: ""
    },

    // Authenticate user
    mutationAuthenticateUser: UserSession.mutationAuthenticateUser,
    queryGetCurrentUser: UserSession.queryGetCurrentUser,

    // Users queries and mutations
    queryGetAllUsers: UserPayload.queryGetAllUsers,
    queryGetUser: UserPayload.queryGetUser,
    mutationCreateUser: UserPayload.mutationCreateUser,
    mutationUpdateUser: UserPayload.mutationUpdateUser,
    mutationCreatePassword: UserPayload.mutationCreatePassword,
    mutationUpdatePassword: UserPayload.mutationUpdatePassword,
    mutationSearchUser: UserPayload.mutationSearchUser,
    mutationCreateUserGroupMembership: UserPayload.mutationCreateUserGroupMembership,
    mutationDeleteUserGroupMembership: UserPayload.mutationDeleteUserGroupMembership,

    // User groups queries and mutations
    queryGetAllUserGroups: UserGroupPayload.queryGetAllUserGroups,
    queryGetUserGroup: UserGroupPayload.queryGetUserGroup,
    queryGetUserUserGroups: UserGroupPayload.queryGetUserUserGroups, // Data for user groups drodpdown in user form
    mutationCreateUserGroup: UserGroupPayload.mutationCreateUserGroup,
    mutationUpdateUserGroup: UserGroupPayload.mutationUpdateUserGroup,
    mutationSearchUserGroup: UserGroupPayload.mutationSearchUserGroup,

    // Data sources queries and mutations
    queryGetAllDataSources: DataSourcePayload.queryGetAllDataSources,
    queryGetDataSource: DataSourcePayload.queryGetDataSource,
    queryGetDataSources: DataSourcePayload.queryGetDataSources, // Data for data sources drodpdown in parameter form
    mutationCreateDataSource: DataSourcePayload.mutationCreateDataSource,
    mutationUpdateDataSource: DataSourcePayload.mutationUpdateDataSource,
    mutationDeleteDataSource: DataSourcePayload.mutationDeleteDataSource,
    mutationSearchDataSource: DataSourcePayload.mutationSearchDataSource,
    mutationTestDataSource: DataSourcePayload.mutationTestDataSource,
    subscriptionGetDataSourceUpdates: DataSourcePayload.subscriptionGetDataSourceUpdates,

    // Data source types queries and mutations
    queryGetAllDataSourceTypes: DataSourceTypePayload.queryGetAllDataSourceTypes,
    queryGetDataSourceTypes: DataSourceTypePayload.queryGetDataSourceTypes,

    //Indicator groups queries and mutations
    queryGetAllIndicatorGroups: IndicatorGroupPayload.queryGetAllIndicatorGroups,
    queryGetIndicatorGroup: IndicatorGroupPayload.queryGetIndicatorGroup,
    queryGetIndicatorGroups: IndicatorGroupPayload.queryGetIndicatorGroups, // Data for indicator groups drodpdown in indicator form
    mutationCreateIndicatorGroup: IndicatorGroupPayload.mutationCreateIndicatorGroup,
    mutationUpdateIndicatorGroup: IndicatorGroupPayload.mutationUpdateIndicatorGroup,
    mutationDeleteIndicatorGroup: IndicatorGroupPayload.mutationDeleteIndicatorGroup,
    mutationSearchIndicatorGroup: IndicatorGroupPayload.mutationSearchIndicatorGroup,
    mutationExecuteIndicatorGroup: IndicatorGroupPayload.mutationExecuteIndicatorGroup,

    //Indicator queries and mutations
    queryGetAllIndicators: IndicatorPayload.queryGetAllIndicators,
    queryGetIndicator: IndicatorPayload.queryGetIndicator,
    mutationCreateIndicator: IndicatorPayload.mutationCreateIndicator,
    mutationUpdateIndicator: IndicatorPayload.mutationUpdateIndicator,
    mutationDeleteIndicator: IndicatorPayload.mutationDeleteIndicator,
    mutationSearchIndicator: IndicatorPayload.mutationSearchIndicator,
    mutationExecuteIndicator: IndicatorPayload.mutationExecuteIndicator,
    mutationDuplicateIndicator: IndicatorPayload.mutationDuplicateIndicator,
    queryGetIndicatorSessions: IndicatorPayload.queryGetIndicatorSessions,

    //Indicator types queries and mutations
    queryGetIndicatorTypes: IndicatorTypePayload.queryGetIndicatorTypes, // Data for indicator types drodpdown in indicator form

    // Logs queries and mutations
    queryGetBatchLog: LogPayload.queryGetBatchLog,
    queryGetSessionLog: LogPayload.queryGetSessionLog,
    queryGetDataSourceLog: LogPayload.queryGetDataSourceLog,

    // Notifications queries and mutations
    subscriptionGetNotification: NotificationPayload.subscriptionGetNotification,
    queryGetAllNotifications: NotificationPayload.queryGetAllNotifications,
    mutationMarkAllNotificationsAsRead: NotificationPayload.mutationMarkAllNotificationsAsRead,
    mutationMarkNotificationsAsRead: NotificationPayload.mutationMarkNotificationsAsRead,

    //Indicator parameters queries and mutations
    mutationCreateParameter: ParameterPayload.mutationCreateParameter,
    mutationUpdateParameter: ParameterPayload.mutationUpdateParameter,
    mutationDeleteParameter: ParameterPayload.mutationDeleteParameter,
    queryGetParameterTypes: ParameterPayload.queryGetParameterTypes, // Data for indicator parameter types drodpdown in indicator parameter form

    //Sessions queries
    queryGetAllSessions: SessionPayload.queryGetAllSessions,
    mutationSearchSession: SessionPayload.mutationSearchSession,
    subscriptionGetSessionUpdates: SessionPayload.subscriptionGetSessionUpdates,

    //Batches queries
    mutationKillBatch: BatchPayload.mutationKillBatch,
    subscriptionGetBatchUpdates: BatchPayload.subscriptionGetBatchUpdates,

    //Dashboard queries
    queryGetNbIndicators: DashboardPayload.queryGetNbIndicators,
    queryGetLastSessions: DashboardPayload.queryGetLastSessions
  },
  mutations: {
    setErrorObject(state, errorObject) {
      state.errorObject = errorObject;
    },
    setCurrentUser(state, currentUser) {
      state.currentUser = currentUser;
    },

    // Mutations triggered by websocket events
    SOCKET_ONOPEN(state, event) {
      Vue.prototype.$socket = event.currentTarget;
      state.websocket.isConnected = true;

      // Define connection payload and activate connection
      let init = { type: "connection_init", payload: {} };
      Vue.prototype.$socket.sendObj(init);

      // Define listener payload and activate listener for notifications
      let payloadNotification = { id: "notification", type: "start", payload: { query: state.subscriptionGetNotification } };
      Vue.prototype.$socket.sendObj(payloadNotification);

      // Define listener payload and activate listener for data source updates
      let payloadDataSource = { id: "dataSource", type: "start", payload: { query: state.subscriptionGetDataSourceUpdates } };
      Vue.prototype.$socket.sendObj(payloadDataSource);

      // Define listener payload and activate listener for batch updates
      let payloadBatch = { id: "batch", type: "start", payload: { query: state.subscriptionGetBatchUpdates } };
      Vue.prototype.$socket.sendObj(payloadBatch);

      // Define listener payload and activate listener for session updates
      let payloadSession = { id: "session", type: "start", payload: { query: state.subscriptionGetSessionUpdates } };
      Vue.prototype.$socket.sendObj(payloadSession);
    },
    SOCKET_ONCLOSE(state) {
      state.websocket.isConnected = false;
    },
    SOCKET_ONERROR() {},
    SOCKET_ONMESSAGE(state, message) {
      state.websocket.message = message; // Default handler called for all methods
    },
    SOCKET_RECONNECT() {},
    SOCKET_RECONNECT_ERROR() {}
  }
});
