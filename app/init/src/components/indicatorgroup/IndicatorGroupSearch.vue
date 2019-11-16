<template>
  <div class="mt-5">
    <!-- Search bar -->
    <input
      class="form-control form-control-lg mb-4"
      type="search"
      aria-label="Search"
      placeholder="Search indicator groups"
      v-model="searchKeyword"
      v-on:keyup.enter="search"
    />

    <!-- Indicator group table -->
    <indicator-group-table v-bind:indicatorGroups="indicatorGroups" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></indicator-group-table>

    <!-- Indicator group pagination -->
    <indicator-group-pagination
      v-if="showPagination"
      v-bind:totalCount="nbIndicatorGroups"
      v-bind:currentPage="currentPage"
      v-on:goToPage="getAllIndicatorGroups"
    ></indicator-group-pagination>
  </div>
</template>

<script>
import toUpper from "lodash/toUpper";
import Mixins from "../utils/Mixins.vue";
import Pagination from "../utils/Pagination.vue";
import IndicatorGroupTable from "./IndicatorGroupTable.vue";

export default {
  mixins: [Mixins],
  components: {
    "indicator-group-table": IndicatorGroupTable,
    "indicator-group-pagination": Pagination
  },
  data: function() {
    return {
      searchKeyword: null,
      indicatorGroups: [],
      nbIndicatorGroups: null,
      showPagination: true,
      currentPage: {
        pageNum: 1,
        offset: 0,
        nbItems: 10,
        isActive: true
      },
      sortAttribute: {
        columnName: "name",
        sortOrder: "asc"
      }
    };
  },
  methods: {
    getAllIndicatorGroups(page) {
      let payload = {
        query: this.$store.state.queryGetAllIndicatorGroups,
        variables: {
          first: page.nbItems,
          offset: page.offset,
          orderBy: [toUpper(this.sortAttribute.columnName + "_" + this.sortAttribute.sortOrder)]
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
            this.indicatorGroups = response.data.data.allIndicatorGroups.nodes;
            this.nbIndicatorGroups = response.data.data.allIndicatorGroups.totalCount;

            // Set current page
            this.currentPage = {
              pageNum: page.pageNum,
              offset: page.offset,
              nbItems: page.nbItems,
              isActive: page.isActive
            };
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    },
    search() {
      // Search indicator groups based on keywords
      // If keyword is empty, use GraphQL native query to benefit from pagination
      if (this.searchKeyword == "" || this.searchKeyword == null) {
        // Show pagination since regular query provide pagination feature
        this.showPagination = true;
        this.getAllIndicatorGroups(this.currentPage);
      } else {
        // Do not show pagination since custom search feature does not include pagination
        this.showPagination = false;
        let payload = {
          query: this.$store.state.mutationSearchIndicatorGroup,
          variables: {
            searchKeyword: this.searchKeyword,
            sortAttribute: this.sortAttribute.columnName,
            sortOrder: this.sortAttribute.sortOrder
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
              this.indicatorGroups = response.data.data.searchIndicatorGroup.indicatorGroups;
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
    },
    setSortAttribute(attribute) {
      this.sortAttribute = {
        columnName: attribute.columnName,
        sortOrder: attribute.sortOrder
      };
      this.search();
    }
  },
  created: function() {
    this.getAllIndicatorGroups(this.currentPage);
  }
};
</script>
