<script>
import { Bubble } from 'vue-chartjs';

export default {
  extends: Bubble,
  props: {
    sessionsLabels: Array,
    sessionsCompleteness: Array,
    sessionsFreshness: Array,
    sessionsLatency: Array,
    sessionsValidity: Array,
    rawSessions: Array
  },
  data: function() {
    return {
      data: {
        labels: this.sessionsLabels,
        datasets: [
          {
            label: 'Completeness',
            backgroundColor: "#42b983",
            data: this.sessionsCompleteness
          },
          {
            label: 'Freshness',
            backgroundColor: "#36a2eb",
            data: this.sessionsFreshness
          },
          {
            label: 'Latency',
            backgroundColor: "#ffcd56",
            data: this.sessionsLatency
          },
          {
            label: 'Validity',
            backgroundColor: "#ff6384",
            data: this.sessionsValidity
          }
        ]
      },
      options: {
        title: {
          display: true,
          text: 'Sessions executed over the last 7 days',
          fontColor: "#ffffff",
          fontSize: "14",
          fontStyle: "normal"
        },
        tooltips: {
          displayColors: false,
          bodySpacing: 5,
          callbacks: {
            label: function(tooltipItem, data) {
              let tooltip = [];
              tooltip.push(" Session: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].sessionId);
              tooltip.push(" Indicator: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].indicator);
              tooltip.push(" Created Date: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].createdDate);
              tooltip.push(" Status: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].status);
              tooltip.push(" Quality Level (%): " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].y);
              return tooltip;
            }.bind(this)
          }
        },
        legend: {
          display: true,
          position: "bottom"
        },
        scales: {
          xAxes: [{
            type: "time",
            time: {
            }
          }],
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
  },
  methods: {
  }
};
</script>
