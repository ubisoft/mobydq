<script>
import { Bubble, mixins } from 'vue-chartjs';
const { reactiveProp, reactiveData } = mixins

export default {
  extends: Bubble,
  props: {
    rawSessions: Array,
    sessionLabelsAlias: Array,
    sessionLabels: Array,
    sessions: Array
  },
  data: function() {
    return {
      data: {
        labels: this.sessionLabels,
        datasets: [
          {
            label: 'Quality Level (%)',
            backgroundColor: "#42b983",
            data: this.sessions
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
            title: function(tooltipItem, data) {
              console.log(tooltipItem);
              return " Session " + tooltipItem[0].xLabel;
            },
            label: function(tooltipItem, data) {
              let tooltip = [];
              tooltip.push(" Indicator: " + this.rawSessions[tooltipItem.index].indicator);
              tooltip.push(" Created Date: " + this.rawSessions[tooltipItem.index].createdDate);
              tooltip.push(" Quality Level (%): " + Math.round(this.rawSessions[tooltipItem.index].qualityLevel*100));
              return tooltip;
            }.bind(this)
          }
        },
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            time: {
              unit: 'day',
              unitStepSize: 0.5,
            },
            ticks: {
              callback: function(value, index, values) {
                //return new Date(this.sessionLabelsAlias[index]);
                return null;
              }.bind(this)
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
