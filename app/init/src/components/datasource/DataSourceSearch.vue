<template>
  <div class="mt-5">
    <!-- Search bar -->
    <input
      class="form-control form-control-lg mb-4"
      type="search"
      aria-label="Search"
      placeholder="Search data sources"
      v-model="searchKeyword"
      v-on:keyup.enter="search"
    />

    <!-- Data source table -->
    <data-source-table
      v-bind:dataSources="dataSources"
      v-bind:sortAttribute="sortAttribute"
      v-on:sortAttribute="setSortAttribute"
    ></data-source-table>

    <!-- Data source pagination -->
    <data-source-pagination
      v-if="showPagination"
      v-bind:totalCount="nbDataSources"
      v-bind:currentPage="currentPage"
      v-on:goToPage="getAllDataSources"
    ></data-source-pagination>
  </div>
</template>

<script>
import toUpper from "lodash/toUpper";
import Mixins from "../utils/Mixins.vue";
import Pagination from "../utils/Pagination.vue";
import DataSourceTable from "./DataSourceTable.vue";

export default {
  mixins: [Mixins],
  components: {
    "data-source-table": DataSourceTable,
    "data-source-pagination": Pagination
  },
  data: function() {
    return {
      searchKeyword: null,
      dataSources: [],
      nbDataSources: null,
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
    getAllDataSources(page) {
      let payload = {
        query: this.$store.state.queryGetAllDataSources,
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
            this.dataSources = response.data.data.allDataSources.nodes;
            this.nbDataSources = response.data.data.allDataSources.totalCount;

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
      // Search data sources based on keywords
      // If keyword is empty, use GraphQL native query to benefit from pagination
      if (this.searchKeyword == "" || this.searchKeyword == null) {
        // Show pagination since regular query provide pagination feature
        this.showPagination = true;
        this.getAllDataSources(this.currentPage);
      } else {
        // Do not show pagination since custom search feature does not include pagination
        this.showPagination = false;
        let payload = {
          query: this.$store.state.mutationSearchDataSource,
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
              this.dataSources = response.data.data.searchDataSource.dataSources;
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
    this.getAllDataSources(this.currentPage);

    // Capture updated data source via websocket listener
    this.$options.sockets.onmessage = function(data) {
      let message = JSON.parse(data.data);
      if (message.id == "dataSource" && message.type == "data") {
        let updatedDataSource = message.payload.data.listen.relatedNode;
        for (let i = 0; i < this.dataSources.length; i++) {
          if (this.dataSources[i].id == updatedDataSource.id) {
            this.dataSources.splice(i, 1, updatedDataSource);
            break; // Stop this loop, we found it!
          }
        }
      }
    }
  }
};
</script>
