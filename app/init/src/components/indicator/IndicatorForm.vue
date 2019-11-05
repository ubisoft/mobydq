<template>
  <div>
    <h1 class="mt-5">Edit Indicator</h1>

    <form>
      <div class="form-row">
        <div class="col-md-4">
          <!-- Data Source Form -->
          <div class="form-group required">
            <label for="indicatorName" class="col-form-label">
              Name:
            </label>
            <input
              class="form-control col-sm"
              id="indicatorName"
              type="text"
              required="required"
              placeholder="Type indicator name"
              v-model="indicator.name"
            />
          </div>
          <div class="form-group">
            <label for="indicatorDescription" class="col-form-label">
              Description:
            </label>
            <textarea
              class="form-control col-sm"
              id="indicatorDescription"
              placeholder="Type indicator description"
              rows="3"
              v-model="indicator.description"
            />
          </div>
          <div class="form-group required">
            <indicator-select-indicator-type
              v-model="indicator.indicatorTypeId"
              v-on:changeIndicatorType="getIndicatorType">
            </indicator-select-indicator-type>
          </div>
          <div class="form-group required">
            <indicator-select-indicator-group
              v-model="indicator.indicatorGroupId"
              v-on:changeIndicatorGroup="getIndicatorGroup">
            </indicator-select-indicator-group>
          </div>
          <div class="form-group">
            <label for="indicatorExecutionOrder" class="col-form-label">
              Execution Order:
            </label>
            <input
              class="form-control col-sm"
              type="number"
              id="indicatorExecutionOrder"
              v-model="indicator.executionOrder"
            />
          </div>
          <div class="custom-control custom-switch mr-4 mt-1 mb-2">
            <input class="custom-control-input" id="active" type="checkbox" value="" v-model="indicator.flagActive" />
            <label for="active" class="custom-control-label">
              Active
            </label>
          </div>

          <!-- Meta-Data -->
          <div>
            <indicator-meta-data
              v-if="indicator.id"
              v-bind:id="indicator.id"
              v-bind:createdDate="indicator.createdDate"
              v-bind:createdBy="indicator.userByCreatedById.email"
              v-bind:updatedDate="indicator.updatedDate"
              v-bind:updatedBy="indicator.userByUpdatedById.email"
            ></indicator-meta-data>
          </div>

          <!-- Button Menu -->
          <div class="mt-3">
            <indicator-button-save v-bind:indicator="indicator"> </indicator-button-save>
            <indicator-button-close> </indicator-button-close>
            <indicator-button-delete v-if="indicator.id" v-bind:indicatorId="indicator.id"> </indicator-button-delete>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import IndicatorSelectIndicatorType from "./IndicatorSelectIndicatorType.vue";
import IndicatorSelectIndicatorGroup from "./IndicatorSelectIndicatorGroup.vue";
import IndicatorButtonSave from "./IndicatorButtonSave.vue";
import IndicatorButtonClose from "./IndicatorButtonClose.vue";
import IndicatorButtonDelete from "./IndicatorButtonDelete.vue";
import MetaDataCard from "../utils/MetaDataCard.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "indicator-select-indicator-type": IndicatorSelectIndicatorType,
    "indicator-select-indicator-group": IndicatorSelectIndicatorGroup,
    "indicator-meta-data": MetaDataCard,
    "indicator-button-save": IndicatorButtonSave,
    "indicator-button-close": IndicatorButtonClose,
    "indicator-button-delete": IndicatorButtonDelete
  },
  data: function() {
    return {
      indicator: {}
    };
  },
  computed: {
    indicatorId() {
      return this.$route.params.indicatorId;
    }
  },
  created: function() {
    // If indicatorId != new then get data for existing indicator
    if (this.indicatorId != "new") {
      let payload = {
        query: this.$store.state.queryGetIndicator,
        variables: {
          id: parseInt(this.indicatorId)
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
            this.indicator = response.data.data.indicatorById;
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
    getIndicatorType(value) {
      // Get indicator type from child component
      if (value != null) {
        this.indicator["indicatorTypeId"] = value;
      } else {
        this.indicator["indicatorTypeId"] = null;
      }
    },
    getIndicatorGroup(value) {
      // Get indicator group from child component
      if (value != null) {
        this.indicator["indicatorGroupId"] = value;
      } else {
        this.indicator["indicatorGroupId"] = null;
      }
    }
  }
};
</script>
