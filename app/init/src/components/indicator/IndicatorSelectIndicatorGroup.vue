<template>
  <div class="form-group">
    <label for="indicatorGroup" class="col-form-label">
      Indicator Group:
    </label>
    <treeselect
      placeholder="Select data source type"
      v-model="selectedValue"
      v-bind:options="options"
      v-bind:multiple="false"
      v-bind:disable-branch-nodes="true"
    />
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";
import Treeselect from "@riophae/vue-treeselect";
import "@riophae/vue-treeselect/dist/vue-treeselect.css";

export default {
  mixins: [Mixins],
  components: {
    treeselect: Treeselect
  },
  props: {
    value: Number
  },
  data() {
    return {
      selectedValue: this.value,
      options: []
    };
  },
  watch: {
    value(arg) {
      this.selectedValue = arg;
    },
    selectedValue(arg) {
      this.$emit("changeIndicatorGroup", arg);
    }
  },
  created: function() {
    // Get list of indicator groups to populate dropdown options
    let payload = { query: this.$store.state.queryGetIndicatorGroups };
    let headers = {};
    if (this.$session.exists()) {
      headers = { Authorization: "Bearer " + this.$session.get("jwt") };
    }
    this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
      function(response) {
        if (response.data.errors) {
          this.displayError(response);
        } else {
          this.options = response.data.data.allIndicatorGroups.nodes;
        }
      },
      // Error callback
      function(response) {
        this.displayError(response);
      }
    );
  }
};
</script>

<style>
.vue-treeselect {
  color: #666666;
}
</style>
