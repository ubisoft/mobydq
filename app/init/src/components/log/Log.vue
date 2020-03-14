<template>
  <div>
    <!-- Meta data for batch logs -->
    <p v-if="batchId">
      Batch Id: {{ batchId }}<br>
      Status: <span class="badge badge-pill" v-bind:class="statusCssClass(batchStatus)" >{{ batchStatus }}</span><br>
      Indicator Group: <router-link v-bind:to="'/indicatorgroups/' + indicatorGroupId">{{ indicatorGroup }}</router-link>
    </p>

    <!-- Meta data for session logs -->
    <p v-if="sessionId">
      Batch Id: {{ sessionId }}<br>
      Session Id: {{ sessionId }}<br>
      Status: <span class="badge badge-pill" v-bind:class="statusCssClass(sessionStatus)" >{{ sessionStatus }}</span><br>
      Indicator: <router-link v-bind:to="'/indicators/' + indicatorId">{{ indicator }}</router-link><br>
      Indicator Type: {{ indicatorType }}
    </p>

    <!-- Meta data for data source logs -->
    <p v-if="dataSourceId">
      Data Source: <router-link v-bind:to="'/datasources/' + dataSourceId">{{ dataSource }}</router-link><br>
      Data Source Type: {{ dataSourceType }}
    </p>

    <!-- Logs -->
    <pre class="mt-5">{{ logs }}</pre>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
  },
  data: function() {
    return {
      batchStatus: "",
      indicatorGroupId: "",
      indicatorGroup: "",
      sessionStatus: "",
      indicatorId: "",
      indicator: "",
      indicatorType: "",
      dataSource: "",
      dataSourceType: "",
      logs: ""
    };
  },
  computed: {
    batchId() {
      return parseInt(this.$route.params.batchId);
    },
    sessionId() {
      return parseInt(this.$route.params.sessionId);
    },
    dataSourceId() {
      return parseInt(this.$route.params.dataSourceId);
    },
  },
  methods: {
    getLog() {
      let payload = {
        variables: {
          orderBy: ["CREATED_DATE_ASC", "ID_ASC"]
        }
      };

      // Add object Id to payload and fetch query
      if (this.batchId) {
        payload['query'] = this.$store.state.queryGetBatchLog;
        payload['variables']['batchId'] = parseInt(this.batchId);
      }
      else if (this.sessionId) {
        payload['query'] = this.$store.state.queryGetSessionLog;
        payload['variables']['sessionId'] = parseInt(this.sessionId);
      }
      else if (this.dataSourceId) {
        payload['query'] = this.$store.state.queryGetDataSourceLog;
        payload['variables']['dataSourceId'] = parseInt(this.dataSourceId);
      }
      else {
        this.logs = 'No log found';
      }

      // Byuild http request
      if (payload['query']) {
        let headers = {};
        if (this.$session.exists()) {
          headers = { Authorization: "Bearer " + this.$session.get("jwt") };
        }
        this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
          function(response) {
            if (response.data.errors) {
              this.displayError(response);
            } else {
              // Fetch logs depending on object type
              let rawLogs = [];

              // Fetch logs for batch
              if (this.batchId) {
                this.batchStatus = response.data.data.batchById.status;
                this.indicatorGroupId = response.data.data.batchById.indicatorGroupId;
                this.indicatorGroup = response.data.data.batchById.indicatorGroupByIndicatorGroupId.name;
                rawLogs = response.data.data.batchById.logsByBatchId.nodes.map(function(log) {
                  return this.buildLogLine(log.id, log.createdDate, log.fileName, log.logLevel, log.message);
                }.bind(this));
              }

              // Fetch logs for session
              else if (this.sessionId) {
                this.sessionStatus = response.data.data.sessionById.status;
                this.indicatorId = response.data.data.sessionById.indicatorId;
                this.indicator = response.data.data.sessionById.indicatorByIndicatorId.name;
                this.indicatorType = response.data.data.sessionById.indicatorByIndicatorId.indicatorTypeByIndicatorTypeId.name;
                rawLogs = response.data.data.sessionById.logsBySessionId.nodes.map(function(log) {
                  return this.buildLogLine(log.id, log.createdDate, log.fileName, log.logLevel, log.message);
                }.bind(this));
              }
              // Fetch logs for data source
              else if (this.dataSourceId) {
                this.dataSource = response.data.data.dataSourceById.name;
                this.dataSourceType = response.data.data.dataSourceById.dataSourceTypeByDataSourceTypeId.name;
                rawLogs = response.data.data.dataSourceById.logsByDataSourceId.nodes.map(function(log) {
                  return this.buildLogLine(log.id, log.createdDate, log.fileName, log.logLevel, log.message);
                }.bind(this));
              }

              // Combine logs into string
              this.logs = rawLogs.join('\n');
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
    },
    buildLogLine(id, createdDate, fileName, logLevel, message) {
      message = message.replace(/\\n/g, "\n"); // Replace string \n by new line
      message = message.replace(/\\"/g, "\""); // Replace string \" by double quotes
      message = message.substring(1, message.length-1) // Remove first and last characters which are double quotes
      let logLine = id + " | " + createdDate + " - " + fileName + " - " + logLevel + " - " + message;
      return logLine;
    }
  },
  created: function() {
    this.getLog();
  }
};
</script>

<style>
pre {
    display: block;
    font-size: 100%;
    color: #ffffff;
    background: #212529;
    padding: 10px;
}
</style>
