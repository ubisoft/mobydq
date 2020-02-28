<template>
  <div class="col">
    <h1 class="mt-5">Dashboard</h1>
    <div class="row">
      <div class="doughnut" v-if="nbIndicators > 0">
        <indicator-chart
          v-bind:nbIndicators="[nbIndicatorsActive, nbIndicatorsInactive]"
          v-bind:nbIndicatorsPerType="[nbIndicatorsCompleteness, nbIndicatorsFreshness, nbIndicatorsLatency, nbIndicatorsValidity]"
          v-bind:width="500"
          v-bind:height="250"
        >
        </indicator-chart>

        <div v-if="nbIndicators" class="nbindicators">
          <h1>{{ nbIndicators }}</h1>
        </div>
      </div>

      <div class="timeserie" v-if="sessionsLabels.length > 0">
        <session-chart
          v-bind:sessionsLabels="sessionsLabels"
          v-bind:sessionsCompleteness="sessionsCompleteness"
          v-bind:sessionsFreshness="sessionsFreshness"
          v-bind:sessionsLatency="sessionsLatency"
          v-bind:sessionsValidity="sessionsValidity"
          v-bind:rawSessions="rawSessions"
          v-bind:width="1000"
          v-bind:height="300"
        >
        </session-chart>
      </div>
    </div>

    <h1 class="mt-5">Sessions</h1>
    <session-search></session-search>
  </div>
</template>

<script>
import Mixins from "./utils/Mixins.vue";
import IndicatorChart from "./dashboard/IndicatorChart.vue";
import SessionChart from "./dashboard/SessionChart.vue";
import SessionSearch from "./session/SessionSearch.vue";

export default {
  mixins: [Mixins],
  components: {
    "indicator-chart": IndicatorChart,
    "session-chart": SessionChart,
    "session-search": SessionSearch
  },
  data: function() {
    return {
      rawIndicators: [],
      nbIndicators: 0,
      nbIndicatorsActive: 0,
      nbIndicatorsInactive: 0,
      nbIndicatorsCompleteness: 0,
      nbIndicatorsFreshness: 0,
      nbIndicatorsLatency: 0,
      nbIndicatorsValidity: 0,
      rawSessions: [],
      sessionsLabels: [],
      sessionsCompleteness: [],
      sessionsFreshness: [],
      sessionsLatency: [],
      sessionsValidity: []
    };
  },
  created: function() {
    // Get number of indicators
    this.getIndicators();

    // Get sessions
    var date = new Date();
    date.setDate(date.getDate() - 1);
    date.toISOString();
    this.getSessions(date);
  },
  methods: {
    getIndicators() {
      // Get indicators
      let payload = {
        query: this.$store.state.queryGetNbIndicators
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
            // Get list of indicators
            this.rawIndicators = response.data.data.allNbIndicators.nodes;

            for (let i = 0; i < this.rawIndicators.length; i++) {
              // Number of active / inactive indicators
              if (this.rawIndicators[i].flagActive) {
                this.nbIndicatorsActive = this.nbIndicatorsActive + parseInt(this.rawIndicators[i].nbIndicators);
              } else {
                this.nbIndicatorsInactive = this.nbIndicatorsInactive + parseInt(this.rawIndicators[i].nbIndicators);
              }

              // Number of indicators per type
              if (this.rawIndicators[i].indicatorType == "Completeness") {
                this.nbIndicatorsCompleteness = this.nbIndicatorsCompleteness + parseInt(this.rawIndicators[i].nbIndicators);
              } else if (this.rawIndicators[i].indicatorType == "Freshness") {
                this.nbIndicatorsFreshness = this.nbIndicatorsFreshness + parseInt(this.rawIndicators[i].nbIndicators);
              } else if (this.rawIndicators[i].indicatorType == "Latency") {
                this.nbIndicatorsLatency = this.nbIndicatorsLatency + parseInt(this.rawIndicators[i].nbIndicators);
              } else if (this.rawIndicators[i].indicatorType == "Validity") {
                this.nbIndicatorsValidity = this.nbIndicatorsValidity + parseInt(this.rawIndicators[i].nbIndicators);
              }

              // Total number of indicators
              this.nbIndicators = this.nbIndicators + parseInt(this.rawIndicators[i].nbIndicators);
            }
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    },
    getSessions(date) {
      // Get sessions
      let payload = {
        query: this.$store.state.queryGetLastSessions,
        variables: {
          date: date
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
            // Get list of sessions
            this.rawSessions = response.data.data.allSessionStatuses.nodes;

            // Prepare data for visualization
            if (this.rawSessions.length > 0) {
              for (let i = 0; i < this.rawSessions.length; i++) {
                // Build labels
                let sessionDate = new Date(this.rawSessions[i].createdDate.substring(0, 19));
                if (!this.sessionsLabels.includes(sessionDate)) {
                  this.sessionsLabels.push(sessionDate);
                }

                // Build data point
                let dataPoint = {
                  x: sessionDate,
                  y: Math.round(this.rawSessions[i].qualityLevel * 100),
                  r: 5,
                  sessionId: this.rawSessions[i].id,
                  indicatorId: this.rawSessions[i].indicatorId,
                  indicator: this.rawSessions[i].indicator,
                  createdDate: this.rawSessions[i].createdDate,
                  status: this.rawSessions[i].status,
                }

                // Add data point to dataset
                if (this.rawSessions[i].indicatorType == "Completeness") {
                  this.sessionsCompleteness.push(dataPoint);
                } else if (this.rawSessions[i].indicatorType == "Freshness") {
                  this.sessionsFreshness.push(dataPoint);
                } else if (this.rawSessions[i].indicatorType == "Latency") {
                  this.sessionsLatency.push(dataPoint);
                } else if (this.rawSessions[i].indicatorType == "Validity") {
                  this.sessionsValidity.push(dataPoint);
                }
              }
            } else {
              this.sessionsLabels.push(Date.now());
            }
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    }
  }
};
</script>

<style>
.doughnut {
  float: left;
  width: 500px;
  height: 250px;
}
.doughnut .nbindicators {
  width: 150px;
  text-align: center;
  display: inline-block;
  position: relative;
  bottom: 135px;
  left: 175px;
}
.timeserie {
  display: block;
  width: 1000px;
  height: 300px;
}
</style>
