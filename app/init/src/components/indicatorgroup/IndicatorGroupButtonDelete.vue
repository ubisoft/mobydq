<template>
  <span>
    <button v-if="show" type="button" class="btn btn-danger float-right" data-toggle="modal" data-target="#ModalBoxDelete">
      Delete
    </button>

    <!-- Modal box to confirm deletion -->
    <modal-box-delete v-bind:objectType="'indicatorGroup'" v-bind:objectId="indicatorGroupId"> </modal-box-delete>
  </span>
</template>

<script>
import ModalBoxDelete from "../utils/ModalBoxDelete.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "modal-box-delete": ModalBoxDelete
  },
  props: {
    indicatorGroupId: Number
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return Number.isInteger(this.indicatorGroupId) && roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
