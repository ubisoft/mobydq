<script>
import { Line  } from 'vue-chartjs'

export default {
  extends: Line,
  props: {
    indicatorSessions: Array,
    labels: Array
  },
  data: function() {
    return {
      dataset: {
        labels: this.labels,
        datasets: [
          {
            label: 'Quality Level Objective (%)',
            backgroundColor: this.generateGradient,
            data: [40, 20, 12, 39]
          }
        ]
      },
      options: {
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
          }]
        }
      }
    };
  },
  mounted: function() {
    this.renderChart(this.dataset, this.options)
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
