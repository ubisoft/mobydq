<template>
  <span>
    <button v-if="show"
      type="button"
      class="btn btn-success"
      v-on:click="editParameter"
      data-toggle="modal"
      data-target="#ParameterModalBox">
      Create Parameter
    </button>
  </span>
</template>

<script>
import ParameterModalBox from "../parameter/ParameterModalBox.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "add-parameter-modal-box": ParameterModalBox,
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    editParameter() {
      this.$emit("editParameter", null);
    }
  }
};
</script>
