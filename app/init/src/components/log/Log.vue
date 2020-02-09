<template>
  <div class="mt-5">
    <pre>{{ logs }}</pre>
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
      logs: ''
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
              let logs = response.data.data.allLogs.nodes.map(function(log) {
                return log.id + " | " + log.createdDate + " - " + log.fileName + " - " + log.logLevel + " - " + log.message;
              });
              this.logs = logs.join('\n');
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
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
