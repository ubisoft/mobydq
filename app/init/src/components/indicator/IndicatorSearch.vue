<template>
  <div class="mt-5">
    <!-- Search bar -->
    <input
      class="form-control form-control-lg mb-4"
      type="search"
      aria-label="Search"
      placeholder="Search indicators"
      v-model="searchKeyword"
      v-on:keyup.enter="search"
    />

    <!-- Indicator table -->
    <indicator-table v-bind:indicators="indicators" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></indicator-table>

    <!-- Indicator pagination -->
    <indicator-pagination
      v-if="showPagination"
      v-bind:totalCount="nbIndicators"
      v-bind:currentPage="currentPage"
      v-on:goToPage="getAllIndicators"
    ></indicator-pagination>
  </div>
</template>

<script>
import toUpper from "lodash/toUpper";
import Mixins from "../utils/Mixins.vue";
import Pagination from "../utils/Pagination.vue";
import IndicatorTable from "./IndicatorTable.vue";

export default {
  mixins: [Mixins],
  components: {
    "indicator-table": IndicatorTable,
    "indicator-pagination": Pagination
  },
  data: function() {
    return {
      searchKeyword: null,
      indicators: [],
      nbIndicators: null,
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
    getAllIndicators(page) {
      let payload = {
        query: this.$store.state.queryGetAllIndicators,
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
            this.indicators = response.data.data.allIndicators.nodes;
            this.nbIndicators = response.data.data.allIndicators.totalCount;

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
      // Search indicators based on keywords
      // If keyword is empty, use GraphQL native query to benefit from pagination
      if (this.searchKeyword == "" || this.searchKeyword == null) {
        // Show pagination since regular query provide pagination feature
        this.showPagination = true;
        this.getAllIndicators(this.currentPage);
      } else {
        // Do not show pagination since custom search feature does not include pagination
        this.showPagination = false;
        let payload = {
          query: this.$store.state.mutationSearchIndicator,
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
              this.indicators = response.data.data.searchIndicator.indicators;
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
    this.getAllIndicators(this.currentPage);
  }
};
</script>
