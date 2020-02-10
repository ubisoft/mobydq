<template>
  <span>
    <button v-if="show" type="button" class="btn btn-secondary ml-1" data-toggle="modal" data-target="#ModalBoxDuplicate">
      Duplicate
    </button>

    <!-- Modal box to provide duplicate details-->
    <modal-box-duplicate v-bind:indicatorId="indicatorId"> </modal-box-duplicate>
  </span>
</template>

<script>
import IndicatorModalBoxDuplicate from "./IndicatorModalBoxDuplicate.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "modal-box-duplicate": IndicatorModalBoxDuplicate
  },
  props: {
    indicatorId: Number
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return Number.isInteger(this.indicatorId) && roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
