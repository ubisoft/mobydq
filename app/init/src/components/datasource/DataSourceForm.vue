<template>
  <div>
    <h1 class="mt-5">Edit Data Source</h1>

    <form>
      <div class="form-row">
        <div class="col-11">
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
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
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
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
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
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
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
              v-model="dataSource.password"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>
          <div v-if="dataSource.id" class="form-group">
              Connectivity Status:
              <span class="badge badge-pill" v-bind:class="statusCssClass(dataSource.connectivityStatus)" >
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
            <data-source-button-test-connectivity v-bind:dataSourceId="dataSourceId"> </data-source-button-test-connectivity>
            <data-source-button-log v-bind:dataSourceId="dataSourceId"> </data-source-button-log>
            <data-source-button-close> </data-source-button-close>
            <data-source-button-delete v-bind:dataSourceId="dataSourceId"> </data-source-button-delete>
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
import DataSourceButtonLog from "./DataSourceButtonLog.vue";
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
    "data-source-button-log": DataSourceButtonLog,
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
      return parseInt(this.$route.params.dataSourceId);
    },
    isReadOnly() {
      let roles = ["advanced", "admin"];
      return !roles.includes(this.$store.state.currentUser.role);
    }
  },
  created: function() {
    this.getDataSource();

    // Capture updated data source via websocket listener
    this.$options.sockets.onmessage = function(data) {
      let message = JSON.parse(data.data);
      if (message.id == "dataSource" && message.type == "data") {
        let updatedDataSource = message.payload.data.listen.relatedNode;
        this.dataSource = updatedDataSource;

        // Display spinner
        if (updatedDataSource.connectivityStatus == "Running") {
          this.spinner = true;
        } else{
          this.spinner = false;
        }
      }
    }
  },
  methods: {
    getDataSource() {
      // If dataSourceId != new then get data for existing data source
      if (Number.isInteger(this.dataSourceId)) {
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
    getDataSourceType(value) {
      // Get data source type from child component
      if (value != null) {
        this.dataSource["dataSourceTypeId"] = value;
      } else {
        this.dataSource["dataSourceTypeId"] = null;
      }
    },
    resetPassword(value) {
      this.showPasswordField = value;
    }
  }
};
</script>
