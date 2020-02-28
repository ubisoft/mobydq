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
          text: 'Sessions executed over the last 24h',
          fontColor: "#ffffff",
          fontSize: "14",
          fontStyle: "normal"
        },
        tooltips: {
          mode: "point",
          intersect: false,
          displayColors: true,
          bodySpacing: 5,
          callbacks: {
            label: function(tooltipItem) {
              let tooltip = [];
              tooltip.push(" Session: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].sessionId);
              //tooltip.push(" Indicator: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].indicator);
              //tooltip.push(" Created Date: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].createdDate);
              //tooltip.push(" Status: " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].status);
              //tooltip.push(" Quality Level (%): " + this.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].y);
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
              unit: 'hour',
              stepSize: 0.5,
              displayFormats: {
                hour: 'YYYY-MM-DD hA'
              }
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Quality Level (%)'
            },
            ticks: {
              max: 100,
              min: 0,
              stepSize: 10
            }
          }]
        },
        //onClick: this.goToIndicator
      }
    };
  },
  mounted: function() {
    this.renderChart(this.data, this.options)
  },
  created: function() {
  },
  methods: {
    goToIndicator(point, event) {
      this.$router.push({
        name: "edit-indicator",
        params: {
          indicatorId: this.data.datasets[event[0]._datasetIndex].data[event[0]._index].indicatorId
        }
      });
    }
  }
};
</script>
