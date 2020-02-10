<script>
import { Doughnut } from 'vue-chartjs';

export default {
  extends: Doughnut,
  props: {
    nbIndicators: Array,
    nbIndicatorsPerType: Array,
  },
  data: function() {
    return {
      data: {
        datasets: [
          {
            label: "Indicator type",
            labels: [" Completeness", " Freshness", " Latency", " Validity"],
            data: this.nbIndicatorsPerType,
            borderColor: "#343a40",
            backgroundColor: ["#42b983", "#36a2eb", "#ffcd56", "#ff6384"],
            weight: 2
          },
          {
            label: "Indicator status",
            labels: [" Active", " Inactive"],
            data: this.nbIndicators,
            borderColor: "#343a40",
            backgroundColor: ["#22cece", "#343a40"],
            weight: 1
          }
        ]
      },
      options: {
        cutoutPercentage: 70,
        title: {
          display: true,
          text: 'Number of indicators',
          fontColor: "#ffffff",
          fontSize: "14",
          fontStyle: "normal"
        },
        legend: {
          display: false
        },
        tooltips: {
          callbacks: {
            label: function (item, data) {
              var label = data.datasets[item.datasetIndex].labels[item.index];
              var value = data.datasets[item.datasetIndex].data[item.index];
              return label + ': ' + value;
            }
          }
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
