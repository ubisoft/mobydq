<template>
  <div>
    <table class="table table-striped table-dark table-hover table-borderless">
      <thead>
        <tr>
          <th scope="col">
            Parameter Type
          </th>
          <th scope="col">
            Parameter Value
          </th>
          <th scope="col">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="parameter in parameters" v-bind:key="parameter.id">
          <td>
            {{ parameter.parameterTypeByParameterTypeId.name }}
          </td>
          <td>
            {{ parameter.value }}
          </td>
          <td>
            <span v-if="showEditParameter"
              class="badge badge-secondary"
              v-on:click="editParameter(parameter)"
              data-toggle="modal"
              data-target="#ParameterModalBox">
              Edit
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    parameters: Array
  },
  data: function() {
    return {
      selectedParameter: null
    };
  },
  computed: {
    showEditParameter() {
      let roles = ["standard", "advanced", "admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    editParameter(parameter) {
      this.$emit("editParameter", parameter);
    }
  }
};
</script>
