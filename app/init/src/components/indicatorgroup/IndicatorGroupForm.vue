<template>
  <div>
    <div class="row">
      <!-- Left column -->
      <div class="col-5">
        <h1 class="mt-5">Edit Indicator Group</h1>

        <form>
          <div class="form-row">
            <div class="col-11">
              <!-- Indicator Group Form -->
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
                  v-bind:disabled="isReadOnly"
                  v-bind:readonly="isReadOnly"
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
                <indicator-group-button-execute v-bind:indicatorGroupId="indicatorGroupId" v-on:executeIndicatorGroup="addBatch"> </indicator-group-button-execute>
                <indicator-group-button-close> </indicator-group-button-close>
                <indicator-group-button-delete v-bind:indicatorGroupId="indicatorGroupId"> </indicator-group-button-delete>
              </div>
            </div>
          </div>
        </form>
      </div>

      <!-- Right column -->
      <div class="col-6">
        <h1 class="mt-5">Execution History</h1>

        <!-- Batch table -->
        <batch-table
          v-if="indicatorGroup.id"
          v-bind:indicatorGroupId="indicatorGroupId"
          v-bind:batches="batches">
        </batch-table>
      </div>
    </div>

    <!-- Indicators -->
    <h1 class="mt-5" v-if="indicatorGroup.id">Indicators</h1>
    <p>
      <indicator-group-button-add-indicator
        v-if="indicatorGroup.id">
      </indicator-group-button-add-indicator>
    </p>

    <!-- Indicator table -->
    <indicator-table
      v-if="indicatorGroup.id"
      v-bind:indicatorGroupId="indicatorGroup.id"
      v-bind:indicators="indicators">
    </indicator-table>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";
import IndicatorGroupButtonSave from "./IndicatorGroupButtonSave.vue";
import IndicatorGroupButtonClose from "./IndicatorGroupButtonClose.vue";
import IndicatorGroupButtonDelete from "./IndicatorGroupButtonDelete.vue";
import IndicatorGroupButtonExecute from "./IndicatorGroupButtonExecute.vue";
import IndicatorGroupButtonAddIndicator from "./IndicatorGroupButtonAddIndicator.vue";
import IndicatorGroupIndicatorTable from "./IndicatorGroupIndicatorTable.vue";
import IndicatorGroupBatch from "./IndicatorGroupBatch.vue";
import MetaDataCard from "../utils/MetaDataCard.vue";

export default {
  mixins: [Mixins],
  components: {
    "indicator-group-button-save": IndicatorGroupButtonSave,
    "indicator-group-button-close": IndicatorGroupButtonClose,
    "indicator-group-button-delete": IndicatorGroupButtonDelete,
    "indicator-group-button-execute": IndicatorGroupButtonExecute,
    "indicator-group-button-add-indicator": IndicatorGroupButtonAddIndicator,
    "indicator-table": IndicatorGroupIndicatorTable,
    "batch-table": IndicatorGroupBatch,
    "indicator-group-meta-data": MetaDataCard
  },
  data: function() {
    return {
      indicatorGroup: {}
    };
  },
  computed: {
    indicatorGroupId() {
      return parseInt(this.$route.params.indicatorGroupId);
    },
    indicators() {
      return this.indicatorGroup.indicatorsByIndicatorGroupId.nodes;
    },
    batches() {
      return this.indicatorGroup.batchesByIndicatorGroupId.nodes;
    },
    isReadOnly() {
      let roles = ["standard", "advanced", "admin"];
      return !roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    getIndicatorGroup() {
      // If indicatorGroupId != new then get data for existing indicator group
      if (Number.isInteger(this.indicatorGroupId)) {
        let payload = {
          query: this.$store.state.queryGetIndicatorGroup,
          variables: {
            id: parseInt(this.indicatorGroupId),
            first: 10,
            offset: 0,
            orderBy: "ID_DESC"
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
    },
    addBatch(value) {
      this.indicatorGroup.batchesByIndicatorGroupId.nodes.unshift(value);
    }
  },
  created: function() {
    this.getIndicatorGroup();

    // Capture updated batch via websocket listener
    this.$options.sockets.onmessage = function(data) {
      let message = JSON.parse(data.data);
      if (message.id == "batch" && message.type == "data") {
        let updatedBatch = message.payload.data.listen.relatedNode;
        for (let i = 0; i < this.indicatorGroup.batchesByIndicatorGroupId.nodes.length; i++) {
          if (this.indicatorGroup.batchesByIndicatorGroupId.nodes[i].id == updatedBatch.id) {
            this.indicatorGroup.batchesByIndicatorGroupId.nodes.splice(i, 1, updatedBatch);
            break; // Stop this loop, we found it!
          }
        }
      }
    }
  }
};
</script>
