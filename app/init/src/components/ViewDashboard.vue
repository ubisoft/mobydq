<template>
  <div class="col">
    <h1 class="mt-5">Dashboard</h1>
      <div class="row"> 
         
        <div class="doughnut">
          <nb-indicators
            v-if="nbIndicatorsActive + nbIndicatorsInactive"
            v-bind:nbIndicators="[nbIndicatorsActive, nbIndicatorsInactive]"
            v-bind:nbIndicatorsPerType="[nbIndicatorsCompleteness, nbIndicatorsFreshness, nbIndicatorsLatency, nbIndicatorsValidity]"
            v-bind:height=250
            v-bind:width=500>
          </nb-indicators>
          
          <div v-if="nbIndicators" class="nbindicators">
            <h1>{{ nbIndicators }}</h1>
          </div>
        </div>
        
        <div class="timeserie">
          <nb-sessions
            v-if="rawSessions.length > 0 && sessionLabelsAlias.length > 0 && sessionLabels.length > 0 && sessions.length > 0"
            v-bind:rawSessions="rawSessions"
            v-bind:sessionLabelsAlias="sessionLabelsAlias"
            v-bind:sessionLabels="sessionLabels"
            v-bind:sessions="sessions"
            v-bind:height=250
            v-bind:width=1000>
          </nb-sessions>
        </div>
      </div>

    <h1 class="mt-5">Sessions</h1>
    <session-search></session-search>
  </div>
</template>

<script>
import Mixins from "./utils/Mixins.vue";
import NbIndicators from "./dashboard/NbIndicators.vue";
import NbSessions from "./dashboard/NbSessions.vue";
import SessionSearch from "./session/SessionSearch.vue";

export default {
  mixins: [Mixins],
  components: {
    "nb-indicators": NbIndicators,
    "nb-sessions": NbSessions,
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
      sessionLabels: [],
      sessionLabelsAlias: [],
      sessions: [],
      tooltips: []
    }
  },
  created: function() {
    // Get number of indicators
    this.getIndicators();
    
    // Get sessions
    var date = new Date();
    date.setDate(date.getDate()-7);
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
              // Total number of indicators
              this.nbIndicators = this.nbIndicators + parseInt(this.rawIndicators[i].nbIndicators);
              
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

            for (let i = 0; i < this.rawSessions.length; i++) {
              this.sessionLabels.push(this.rawSessions[i].id);
              this.sessionLabelsAlias.push(this.rawSessions[i].createdDate);
              this.sessions.push({ x: this.rawSessions[i].id, y: Math.round(this.rawSessions[i].qualityLevel*100), r: 5 });
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
  height: 250px;
}
</style>
