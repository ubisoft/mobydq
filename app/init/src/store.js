import Vue from "vue";
import Vuex from "vuex";
import * as Session from "./payloads/session";
import * as UserPayload from "./payloads/user";
import * as UserGroupPayload from "./payloads/usergroup";
import * as DataSourcePayload from "./payloads/datasource";
import * as DataSourceTypePayload from "./payloads/datasourcetype";

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    graphqlUrl: "/mobydq/api/v1/graphql",
    errorObject: {
      flag: false,
      message: ""
    },

    // Authenticate user
    mutationAuthenticateUser: Session.mutationAuthenticateUser,
    queryGetCurrentUser: Session.queryGetCurrentUser,
    currentUser: {
      isAuthenticated: false, // Used to customize UI display
      role: "anonymous", // Used to customize UI display
      userGroups: [
        {
          id: 0,
          name: ""
        }
      ],
      selectedUserGroup: {
        id: 0,
        name: ""
      }
    },

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
    mutationCreateDataSource: DataSourcePayload.mutationCreateDataSource,
    mutationUpdateDataSource: DataSourcePayload.mutationUpdateDataSource,
    mutationDeleteDataSource: DataSourcePayload.mutationDeleteDataSource,
    mutationSearchDataSource: DataSourcePayload.mutationSearchDataSource,

    // Data source types queries and mutations
    queryGetAllDataSourceTypes: DataSourceTypePayload.queryGetAllDataSourceTypes,
    queryGetDataSourceTypes: DataSourceTypePayload.queryGetDataSourceTypes
  }
});
