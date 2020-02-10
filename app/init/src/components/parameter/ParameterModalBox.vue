<template>
  <div class="modal fade" id="ParameterModalBox" tabindex="-1" role="dialog" aria-labelledby="Parameter" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
      <div class="modal-content bg-dark text-light">
        <div class="modal-header">
          <h5 class="modal-title">Edit Parameter</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>

        <div class="modal-body bg-secondary text-light">
          <div class="form-group required">
            <parameter-select-parameter-type
              v-model="parameter.parameterTypeId"
              v-on:changeParameterType="getParameterType">
            </parameter-select-parameter-type>
          </div>

          <!-- Input for alert operator -->
          <div v-if="parameter.parameterTypeId==1" class="form-group">
              <label for="alertOperator" class="col-form-label">
                Alert Operator:
              </label>
              <select
                class="form-control"
                id="alertOperator"
                v-model="parameter.value"
                v-bind:disabled="isReadOnly"
                v-bind:readonly="isReadOnly">
                  <option value="==">&#61;&#61;</option>
                  <option value=">">&gt;</option>
                  <option value=">=">&gt;&#61;</option>
                  <option value="<">&lt;</option>
                  <option value="<=">&lt;&#61;</option>
                  <option value="<>">&lt;&gt;</option>
              </select>
          </div>

          <!-- Input for alert threshold -->
          <div v-if="parameter.parameterTypeId==2" class="form-group">
            <label for="alertOperator" class="col-form-label">
              Alert Threshold:
            </label>
            <input
              class="form-control col-sm"
              id="alertThreshold"
              type="number"
              placeholder="Type alert threshold value"
              v-model="parameter.value"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>

          <!-- Input for distribution list -->
          <div v-if="parameter.parameterTypeId==3" class="form-group">
            <label for="distributionList" class="col-form-label">
              Distribution List: <span class="badge badge-pill badge-info" data-toggle="tooltip" data-placement="right" title="Must be in Python list format such as: ['a@b.com', 'c@d.com']">?</span>
            </label>
            <input
              class="form-control col-sm"
              id="distributionList"
              type="text"
              placeholder="Type e-mail address"
              v-model="parameter.value"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>

          <!-- Input for dimension -->
          <div v-if="parameter.parameterTypeId==4" class="form-group">
            <label for="dimension" class="col-form-label">
              Dimensions: <span class="badge badge-pill badge-info" data-toggle="tooltip" data-placement="right" title="Must be in Python list format such as: ['dim column 1', 'dim column 2']">?</span>
            </label>
            <input
              class="form-control col-sm"
              id="dimension"
              type="text"
              placeholder="Type alias name for dimension column"
              v-model="parameter.value"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>

          <!-- Input for measure -->
          <div v-if="parameter.parameterTypeId==5" class="form-group">
            <label for="measure" class="col-form-label">
              Measures: <span class="badge badge-pill badge-info" data-toggle="tooltip" data-placement="right" title="Must be in Python list format such as: ['measure column 1', ' measure column 2']">?</span>
            </label>
            <input
              class="form-control col-sm"
              id="measure"
              type="text"
              placeholder="Type alias name for measure column"
              v-model="parameter.value"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>

          <!-- Input for source or target system -->
          <div v-if="[6, 8].includes(parameter.parameterTypeId)" class="form-group">
            <parameter-select-data-source
              v-on:changeDataSource="getDataSource"
              v-model="parameter.value">
            </parameter-select-data-source>
          </div>

          <!-- Input for source or target request -->
          <div v-if="[7, 9].includes(parameter.parameterTypeId)" class="form-group">
            <label for="request" class="col-form-label">
              Request:
            </label>
            <textarea
              class="form-control col-sm"
              id="request"
              placeholder="Type query to be executed on data source"
              rows="5"
              v-model="parameter.value"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <parameter-button-delete
            v-if="parameter.id"
            v-bind:parameterId="parameter.id"
            v-on:removeParameter="removeParameter">
          </parameter-button-delete>
          
          <parameter-button-close>
          </parameter-button-close>
          
          <parameter-button-save
            v-bind:indicatorId="indicatorId"
            v-bind:parameter="parameter"
            v-on:addParameter="addParameter">
          </parameter-button-save>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ParameterSelectParameterType from "./ParameterSelectParameterType.vue";
import ParameterSelectDataSource from "./ParameterSelectDataSource.vue";
import ParameterButtonSave from "./ParameterButtonSave.vue";
import ParameterButtonClose from "./ParameterButtonClose.vue";
import ParameterButtonDelete from "./ParameterButtonDelete.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "parameter-select-parameter-type": ParameterSelectParameterType,
    "parameter-select-data-source": ParameterSelectDataSource,
    "parameter-button-save": ParameterButtonSave,
    "parameter-button-close": ParameterButtonClose,
    "parameter-button-delete": ParameterButtonDelete
  },
  props: {
    indicatorId: Number,
    indicatorTypeId: Number,
    parameter: Object
  },
  data: function() {
    return {
    };
  },
  computed: {
    isReadOnly() {
      let roles = ["standard", "advanced", "admin"];
      return !roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    getParameterType(value) {
      // Get indicator parameter type from child component
      if (value != null) {
        this.parameter["parameterTypeId"] = value;
      } else {
        this.parameter["parameterTypeId"] = null;
      }
    },
    getDataSource(value) {
      // Get indicator group from child component
      if (value != null) {
        this.parameter["value"] = value;
      } else {
        this.parameter["value"] = null;
      }
    },
    addParameter(value) {
      this.parameter.id = value.id;
      this.$emit("addParameter", value);
    },
    removeParameter(value) {
      this.$emit("removeParameter", value);
    }
  }
};
</script>

<style>
.modal-header {
  border: 0px;
}
.modal-footer {
  border: 0px;
  display: block;
}
</style>
