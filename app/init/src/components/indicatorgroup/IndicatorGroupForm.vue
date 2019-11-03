<template>
  <div>
    <h1 class="mt-5">Edit Indicator Group</h1>

    <form>
      <div class="form-row">
        <div class="col-md-4">
          <!-- Data Source Form -->
          <div class="form-group required">
            <label for="indicatorGroupName" class="col-form-label">
              Name:
            </label>
            <input
              class="form-control col-sm"
              id="indicatorGroupName"
              type="text"
              required="required"
              placeholder="Type indicator group name"
              v-model="indicatorGroup.name"
            />
          </div>

          <!-- Meta-Data -->
          <div>
            <indicator-group-meta-data
              v-if="indicatorGroup.id"
              v-bind:id="indicatorGroup.id"
              v-bind:createdDate="indicatorGroup.createdDate"
              v-bind:createdBy="indicatorGroup.userByCreatedById.email"
              v-bind:updatedDate="indicatorGroup.updatedDate"
              v-bind:updatedBy="indicatorGroup.userByUpdatedById.email"
            ></indicator-group-meta-data>
          </div>

          <!-- Button Menu -->
          <div class="mt-3">
            <indicator-group-button-save v-bind:indicatorGroup="indicatorGroup"> </indicator-group-button-save>
            <indicator-group-button-close> </indicator-group-button-close>
            <indicator-group-button-delete v-if="indicatorGroup.id" v-bind:indicatorGroupId="indicatorGroup.id"> </indicator-group-button-delete>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import IndicatorGroupButtonSave from "./IndicatorGroupButtonSave.vue";
import IndicatorGroupButtonClose from "./IndicatorGroupButtonClose.vue";
import IndicatorGroupButtonDelete from "./IndicatorGroupButtonDelete.vue";
import MetaDataCard from "../utils/MetaDataCard.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "indicator-group-meta-data": MetaDataCard,
    "indicator-group-button-save": IndicatorGroupButtonSave,
    "indicator-group-button-close": IndicatorGroupButtonClose,
    "indicator-group-button-delete": IndicatorGroupButtonDelete
  },
  data: function() {
    return {
      indicatorGroup: {}
    };
  },
  computed: {
    indicatorGroupId() {
      return this.$route.params.indicatorGroupId;
    }
  },
  created: function() {
    // If indicatorGroupId != new then get data for existing indicator group
    if (this.indicatorGroupId != "new") {
      let payload = {
        query: this.$store.state.queryGetIndicatorGroup,
        variables: {
          id: parseInt(this.indicatorGroupId)
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
            this.indicatorGroup = response.data.data.indicatorGroupById;
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
