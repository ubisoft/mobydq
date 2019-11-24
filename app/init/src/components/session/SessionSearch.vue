<template>
  <div class="mt-5">
    <!-- Search bar -->
    <input
      class="form-control form-control-lg mb-4"
      type="search"
      aria-label="Search"
      placeholder="Search sessions"
      v-model="searchKeyword"
      v-on:keyup.enter="search"
    />

    <!-- Session table -->
    <session-table v-bind:sessions="sessions" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></session-table>

    <!-- Session pagination -->
    <session-pagination
      v-if="showPagination"
      v-bind:totalCount="nbSessions"
      v-bind:currentPage="currentPage"
      v-on:goToPage="getAllSessions"
    ></session-pagination>
  </div>
</template>

<script>
import toUpper from "lodash/toUpper";
import Mixins from "../utils/Mixins.vue";
import Pagination from "../utils/Pagination.vue";
import SessionTable from "./SessionTable.vue";

export default {
  mixins: [Mixins],
  components: {
    "session-table": SessionTable,
    "session-pagination": Pagination
  },
  data: function() {
    return {
      searchKeyword: null,
      sessions: [],
      nbSessions: null,
      showPagination: true,
      currentPage: {
        pageNum: 1,
        offset: 0,
        nbItems: 10,
        isActive: true
      },
      sortAttribute: {
        columnName: "updated_date",
        sortOrder: "desc"
      }
    };
  },
  methods: {
    getAllSessions(page) {
      let payload = {
        query: this.$store.state.queryGetAllSessions,
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
            this.sessions = response.data.data.allSessions.nodes;
            this.nbSessions = response.data.data.allSessions.totalCount;

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
      // Search sessions based on keywords
      // If keyword is empty, use GraphQL native query to benefit from pagination
      if (this.searchKeyword == "" || this.searchKeyword == null) {
        // Show pagination since regular query provide pagination feature
        this.showPagination = true;
        this.getAllSessions(this.currentPage);
      } else {
        // Do not show pagination since custom search feature does not include pagination
        this.showPagination = false;
        let payload = {
          query: this.$store.state.mutationSearchSession,
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
              this.sessions = response.data.data.searchSession.sessions;
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
    this.getAllSessions(this.currentPage);
  }
};
</script>
