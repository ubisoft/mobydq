<template>
  <div>
    <div class="row">
      <!-- Left column -->
      <div class="col-5">
        <h1 class="mt-5">Edit Indicator</h1>

        <form>
          <div class="form-row">
            <div class="col-11">
              <!-- Indicator Form -->
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
                  v-bind:disabled="isReadOnly"
                  v-bind:readonly="isReadOnly"
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
                  v-bind:disabled="isReadOnly"
                  v-bind:readonly="isReadOnly"
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
                  Execution Order: <span class="badge badge-pill badge-info" data-toggle="tooltip" data-placement="right" title="Order in wich the indicator is executed in a batch.">?</span>
                </label>
                <input
                  class="form-control col-sm"
                  type="number"
                  id="indicatorExecutionOrder"
                  v-model="indicator.executionOrder"
                  v-bind:disabled="isReadOnly"
                  v-bind:readonly="isReadOnly"
                />
              </div>
              <div class="custom-control custom-switch mr-4 mt-1 mb-2">
                <input
                  class="custom-control-input"
                  id="active"
                  type="checkbox"
                  value=""
                  v-model="indicator.flagActive" 
                  v-bind:disabled="isReadOnly"
                  v-bind:readonly="isReadOnly"
                />
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
                <indicator-button-execute v-bind:indicatorId="indicatorId" v-bind:indicatorGroupId="indicator.indicatorGroupId" v-bind:flagActive="indicator.flagActive" v-on:executeIndicator="addSession"> </indicator-button-execute>
                <indicator-button-duplicate v-bind:indicatorId="indicatorId"> </indicator-button-duplicate>
                <indicator-button-close> </indicator-button-close>
                <indicator-button-delete v-bind:indicatorId="indicatorId"> </indicator-button-delete>
              </div>
            </div>
          </div>
        </form>
      </div>

      <!-- Right column -->
      <div class="col-6">
        <h1 class="mt-5">Execution History</h1>
        Quality Level (%): <span class="badge badge-pill badge-info" data-toggle="tooltip" data-placement="right" title="(Nb Records Without Alert/Nb Records)x100">?</span>
        
        <!-- Chart -->
        <indicator-session-chart
          v-if="indicator.id"
          v-bind:height=150
          v-bind:width=510
          v-bind:sessions="sessions">
        </indicator-session-chart>

        <!-- Session table -->
        <indicator-session
          v-if="indicator.id"
          v-bind:indicatorId="indicatorId"
          v-bind:indicatorGroupId="indicator.indicatorGroupId"
          v-bind:sessions="sessions">
        </indicator-session>
      </div>
    </div>

    <!-- Parameters -->
    <h1 class="mt-5" v-if="indicator.id">Indicator Parameters</h1>
    <p>
      <indicator-button-add-parameter
        v-if="indicator.id"
        v-on:editParameter="getParameter">
      </indicator-button-add-parameter>
    </p>

    <!-- Parameter table -->
    <parameter-table
      v-if="indicator.id"
      v-bind:parameters="parameters"
      v-on:editParameter="getParameter"
      v-bind:key="refreshTable">
    </parameter-table>

    <!-- Modal box to update parameters -->
    <parameter-modal-box
      v-if="indicator.id"
      v-bind:indicatorId="indicator.id"
      v-bind:indicatorTypeId="indicator.indicatorTypeId"
      v-bind:parameter="selectedParameter"
      v-on:addParameter="addParameter"
      v-on:removeParameter="removeParameter">
    </parameter-modal-box>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";
import remove from "lodash/remove";
import IndicatorSelectIndicatorType from "./IndicatorSelectIndicatorType.vue";
import IndicatorSelectIndicatorGroup from "./IndicatorSelectIndicatorGroup.vue";
import IndicatorButtonSave from "./IndicatorButtonSave.vue";
import IndicatorButtonClose from "./IndicatorButtonClose.vue";
import IndicatorButtonDelete from "./IndicatorButtonDelete.vue";
import IndicatorButtonExecute from "./IndicatorButtonExecute.vue";
import IndicatorButtonDuplicate from "./IndicatorButtonDuplicate.vue";
import IndicatorButtonAddParameter from "./IndicatorButtonAddParameter.vue";
import IndicatorSession from "./IndicatorSession.vue";
import IndicatorSessionChart from "./IndicatorSessionChart.vue";
import IndicatorParameterTable from "./IndicatorParameterTable.vue";
import ParameterModalBox from "../parameter/ParameterModalBox.vue";
import MetaDataCard from "../utils/MetaDataCard.vue";

export default {
  mixins: [Mixins],
  components: {
    "indicator-select-indicator-type": IndicatorSelectIndicatorType,
    "indicator-select-indicator-group": IndicatorSelectIndicatorGroup,
    "indicator-button-save": IndicatorButtonSave,
    "indicator-button-close": IndicatorButtonClose,
    "indicator-button-delete": IndicatorButtonDelete,
    "indicator-button-execute": IndicatorButtonExecute,
    "indicator-button-duplicate": IndicatorButtonDuplicate,
    "indicator-button-add-parameter": IndicatorButtonAddParameter,
    "indicator-session": IndicatorSession,
    "indicator-session-chart": IndicatorSessionChart,
    "parameter-table": IndicatorParameterTable,
    "parameter-modal-box": ParameterModalBox,
    "indicator-meta-data": MetaDataCard
  },
  data: function() {
    return {
      indicator: {},
      selectedParameter: {
        id: null,
        parameterTypeId: null,
        value: null,
        indicatorId: null
      },
      refreshTable: 0 // Key used to force refresh of parameter table when deleting parameter
    };
  },
  computed: {
    indicatorId() {
      return parseInt(this.$route.params.indicatorId);
    },
    parameters() {
      return this.indicator.parametersByIndicatorId.nodes;
    },
    sessions() {
      return this.indicator.sessionsByIndicatorId.nodes;
    },
    isReadOnly() {
      let roles = ["standard", "advanced", "admin"];
      return !roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    getIndicator() {
      // If indicatorId != new then get data for existing indicator
      if (Number.isInteger(this.indicatorId)) {
        let headers = {};
        if (this.$session.exists()) {
          headers = { Authorization: "Bearer " + this.$session.get("jwt") };
        }
        let payload = {
          query: this.$store.state.queryGetIndicator,
          variables: {
            id: parseInt(this.indicatorId),
            first: 10,
            offset: 0,
            orderBy: "ID_DESC"
          }
        };
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
    },
    getParameter(value) {
      // Get parameter to be created or updated, from child component (modal box)
      if (value != null) {
        this.selectedParameter = value;
      } else {
        this.selectedParameter['id'] = null;
        this.selectedParameter['parameterTypeId'] = null;
        this.selectedParameter['value'] = null;
        this.selectedParameter['indicatorId'] = null;
      }
    },
    addParameter(value) {
      // Add newly created parameter to parameter table
      this.indicator.parametersByIndicatorId.nodes.push(value);
    },
    removeParameter(value) {
      // Remove parameter from parameter table
      remove(this.indicator.parametersByIndicatorId.nodes, function(parameter) {
        return parameter.id == value;
      });
      this.refreshTable += 1; // Force refresh of parameter table
    },
    addSession(value) {
      this.indicator.sessionsByIndicatorId.nodes.unshift(value);
    }
  },
  created: function() {
    this.getIndicator();

    // Capture updated session via websocket listener
    this.$options.sockets.onmessage = function(data) {
      let message = JSON.parse(data.data);
      if (message.id == "session" && message.type == "data") {
        let updatedSession = message.payload.data.listen.relatedNode;
        for (let i = 0; i < this.indicator.sessionsByIndicatorId.nodes.length; i++) {
          if (this.indicator.sessionsByIndicatorId.nodes[i].id == updatedSession.id) {
            this.indicator.sessionsByIndicatorId.nodes.splice(i, 1, updatedSession);
            break; // Stop this loop, we found it!
          }
        }
      }
    }
  }
};
</script>