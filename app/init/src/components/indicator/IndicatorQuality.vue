<script>
import { Line  } from 'vue-chartjs';
import reverse from "lodash/reverse";

export default {
  extends: Line,
  props: {
    indicatorId: String,
  },
  data: function() {
    return {
      data: {
        labels: [],
        datasets: [
          {
            label: 'Quality Level (%)',
            backgroundColor: this.generateGradient,
            data: [],
          }
        ]
      },
      options: {
        title: {
          display: false,
          text: 'Quality Level'
        },
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            ticks: {
              max: 100,
              min: 0,
              stepSize: 10
            }
          }]
        }
      }
    };
  },
  computed: {
    indicatorSessionsLabels() {
      return this.indicatorSessions.map(function(session) {
        return "Session " + session.id;
      });
    }
  },
  mounted: function() {
    // this.renderChart(this.data, this.options)
  },
  created: function() {
    // If indicatorId != new then get data for existing indicator
    if (this.indicatorId != "new") {
      let headers = {};
      if (this.$session.exists()) {
        headers = { Authorization: "Bearer " + this.$session.get("jwt") };
      }
      let payload = {
        query: this.$store.state.queryGetIndicatorSessions,
        variables: {
          first: 10,
          offset: 0,
          orderBy: "ID_DESC",
          indicatorId: parseInt(this.indicatorId)
        }
      };
      this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
        function(response) {
          if (response.data.errors) {
            this.displayError(response);
          } else {
            let sessions = response.data.data.allSessions.nodes;
            
            // Create labels array
            this.data.labels = sessions.map(function(session) {
              return "Session " + session.id;
            });
            reverse(this.data.labels);

            // Create data array
            this.data.datasets[0]['data'] = sessions.map(function(session) {
              if (session.sessionResultsBySessionId.nodes[0]) {
                let results = session.sessionResultsBySessionId.nodes[0];
                return (results.nbRecordsNoAlert/results.nbRecords)*100;
              } else {
                return 0;
              }
            });
            reverse(this.data.datasets[0]['data']);

            // Render chart
            this.renderChart(this.data, this.options)
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    }
  },
  methods: {
    generateGradient() {
      var ctx = this.$refs.canvas.getContext("2d");
      var gradientStroke = ctx.createLinearGradient(280, 280, 280, 0);
      gradientStroke.addColorStop(0, "#2c3e50");
      gradientStroke.addColorStop(1, "#42b983");
      return gradientStroke;
    }
  }
};
</script>
