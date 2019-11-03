<template>
  <div>
    <h1 class="mt-5">Edit Data Source</h1>

    <form>
      <div class="form-row">
        <div class="col-md-4">
          <!-- Data Source Form -->
          <div class="form-group required">
            <label for="dataSourceName" class="col-form-label">
              Name:
            </label>
            <input
              class="form-control col-sm"
              id="dataSourceName"
              type="text"
              required="required"
              placeholder="Type data source name"
              v-model="dataSource.name"
            />
          </div>
          <div class="form-group required">
            <data-source-select-data-source-type
              v-model="dataSource.dataSourceTypeId"
              v-on:changeDataSourceType="getDataSourceType">
            </data-source-select-data-source-type>
          </div>
          <div class="form-group required">
            <label for="dataSourceConnectionString" class="col-form-label">
              Connection String:
            </label>
            <textarea
              class="form-control col-sm"
              id="dataSourceConnectionString"
              required="true"
              placeholder="Type data source connection string"
              rows="3"
              v-model="dataSource.connectionString"
            />
          </div>
          <div class="form-group">
            <label for="dataSourceLogin" class="col-form-label">
              Login:
            </label>
            <input
              class="form-control col-sm"
              id="dataSourceLogin"
              type="text"
              placeholder="Type data source login"
              v-model="dataSource.login"
            />
          </div>
          <div v-if="showPasswordField" class="form-group">
            <label for="dataSourcePassword" class="col-form-label">
              Password:
            </label>
            <input
              class="form-control col-sm"
              id="dataSourcePassword"
              type="password"
              placeholder="Type data source password"
              v-model="dataSource.password" />
          </div>
          <div class="form-group">
              Connectivity Status:
              <span class="badge badge-pill" v-bind:class="{ 'badge-success': connectivityStatusOK, 'badge-danger': connectivityStatusKO }" >
                  {{ dataSource.connectivityStatus }}
              </span>
              <span v-show="spinner" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          </div>

          <!-- Meta-Data -->
          <div>
            <data-source-meta-data
              v-if="dataSource.id"
              v-bind:id="dataSource.id"
              v-bind:createdDate="dataSource.createdDate"
              v-bind:createdBy="dataSource.userByCreatedById.email"
              v-bind:updatedDate="dataSource.updatedDate"
              v-bind:updatedBy="dataSource.userByUpdatedById.email"
            ></data-source-meta-data>
          </div>

          <!-- Button Menu -->
          <div class="mt-3">
            <data-source-button-save v-bind:dataSource="dataSource" v-bind:showPasswordField="showPasswordField"> </data-source-button-save>
            <data-source-button-reset-password v-on:resetPassword="resetPassword" v-bind:dataSourceId="dataSourceId"> </data-source-button-reset-password>
            <data-source-button-test-connectivity v-on:connectivityTestStatus="connectivityTestStatus" v-bind:dataSourceId="dataSourceId"> </data-source-button-test-connectivity>
            <data-source-button-close> </data-source-button-close>
            <data-source-button-delete v-if="dataSource.id" v-bind:dataSourceId="dataSource.id"> </data-source-button-delete>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import DataSourceSelectDataSourceType from "./DataSourceSelectDataSourceType.vue";
import DataSourceButtonSave from "./DataSourceButtonSave.vue";
import DataSourceButtonResetPassword from "./DataSourceButtonResetPassword.vue";
import DataSourceButtonTestConnectivity from "./DataSourceButtonTestConnectivity.vue";
import DataSourceButtonClose from "./DataSourceButtonClose.vue";
import DataSourceButtonDelete from "./DataSourceButtonDelete.vue";
import MetaDataCard from "../utils/MetaDataCard.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "data-source-select-data-source-type": DataSourceSelectDataSourceType,
    "data-source-meta-data": MetaDataCard,
    "data-source-button-save": DataSourceButtonSave,
    "data-source-button-reset-password": DataSourceButtonResetPassword,
    "data-source-button-test-connectivity": DataSourceButtonTestConnectivity,
    "data-source-button-close": DataSourceButtonClose,
    "data-source-button-delete": DataSourceButtonDelete
  },
  data: function() {
    return {
      dataSource: {},
      showPasswordField: false,
      spinner: false
    };
  },
  computed: {
    dataSourceId() {
      return this.$route.params.dataSourceId.toString();
    },
    connectivityStatusOK() {
      return this.dataSource.connectivityStatus == "Success";
    },
    connectivityStatusKO() {
      return this.dataSource.connectivityStatus == "Failed";
    }
  },
  created: function() {
    // If dataSourceId != new then get data for existing data source
    if (this.dataSourceId != "new") {
      let payload = {
        query: this.$store.state.queryGetDataSource,
        variables: {
          id: parseInt(this.dataSourceId)
        }
      };
      let headers = {};
      if (this.$session.exists()) {
        headers = { Authorization: "Bearer " + this.$session.get("jwt") };
      }
      this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
        function(response) {
          if (response.data.errors) {
            this.displayError(response);
          } else {
            this.dataSource = response.data.data.dataSourceById;
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    } else {
      this.showPasswordField = true;
    }
  },
  methods: {
    getDataSourceType(value) {
      // Get user group from child component
      if (value != null) {
        this.dataSource["dataSourceTypeId"] = value;
      } else {
        this.list["dataSourceTypeId"] = null;
      }
    },
    resetPassword(value) {
      this.showPasswordField = value;
    },
    connectivityTestStatus(value) {
      this.spinner = value.spinner;
      if (!value.spinner) {
        this.dataSource.connectivityStatus = value.connectivityStatus;
        this.dataSource.updatedDate = value.updatedDate;
        this.dataSource.userByUpdatedById.email = value.userByUpdatedById.email;
      }
    }
  }
};
</script>
