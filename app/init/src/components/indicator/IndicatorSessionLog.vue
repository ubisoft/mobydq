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
    sessionId() {
      return this.$route.params.sessionId;
    },
  },
  methods: {
    getLog() {
      let payload = {
        query: this.$store.state.queryGetIndicatorSessionLog,
        variables: {
          sessionId: parseInt(this.sessionId),
          orderBy: ["CREATED_DATE_ASC", "ID_ASC"]
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
