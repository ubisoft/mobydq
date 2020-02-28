<script>
import { Line  } from 'vue-chartjs';
import reverse from "lodash/reverse";

export default {
  extends: Line,
  props: {
    sessions: Array
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
  mounted: function() {
    this.renderChart(this.data, this.options)
  },
  created: function() {
    // Create labels array
    this.data.labels = this.sessions.map(function(session) {
      return "Session " + session.id;
    });
    reverse(this.data.labels);

    // Create data array
    this.data.datasets[0]['data'] = this.sessions.map(function(session) {
      if (session.nbRecords>0) {
        return Math.round((session.nbRecordsNoAlert/session.nbRecords)*100);
      } else {
        return 0;
      }
    });
    reverse(this.data.datasets[0]['data']);
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
