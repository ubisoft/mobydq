<template>
  <div class="mt-5">
    <!-- Search bar -->
    <input
      class="form-control form-control-lg mb-4"
      type="search"
      aria-label="Search"
      placeholder="Search user groups"
      v-model="searchKeyword"
      v-on:keyup.enter="search"
    />

    <!-- User group table -->
    <user-group-table v-bind:userGroups="userGroups" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></user-group-table>

    <!-- User group pagination -->
    <user-group-pagination
      v-if="showPagination"
      v-bind:totalCount="nbUserGroups"
      v-bind:currentPage="currentPage"
      v-on:goToPage="getAllUserGroups"
    ></user-group-pagination>
  </div>
</template>

<script>
import toUpper from "lodash/toUpper";
import Mixins from "../utils/Mixins.vue";
import Pagination from "../utils/Pagination.vue";
import UserGroupTable from "./UserGroupTable.vue";

export default {
  mixins: [Mixins],
  components: {
    "user-group-table": UserGroupTable,
    "user-group-pagination": Pagination
  },
  data: function() {
    return {
      searchKeyword: null,
      userGroups: [],
      nbUserGroups: null,
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
    getAllUserGroups(page) {
      let payload = {
        query: this.$store.state.queryGetAllUserGroups,
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
            this.userGroups = response.data.data.allUserGroups.nodes;
            this.nbUserGroups = response.data.data.allUserGroups.totalCount;

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
      // Search user groups based on keywords
      // If keyword is empty, use GraphQL native query to benefit from pagination
      if (this.searchKeyword == "" || this.searchKeyword == null) {
        // Show pagination since regular query provide pagination feature
        this.showPagination = true;
        this.getAllUserGroups(this.currentPage);
      } else {
        // Do not show pagination since custom search feature does not include pagination
        this.showPagination = false;
        let payload = {
          query: this.$store.state.mutationSearchUserGroup,
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
              this.userGroups = response.data.data.searchUserGroup.userGroups;
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
    this.getAllUserGroups(this.currentPage);
  }
};
</script>
