<script>
export default {
  methods: {
    displayError(response, batchErrors = null) {
      // Method to display error message
      let errorObject = {
        flag: false,
        message: ""
      };

      // PostGraphile errors return status 200 with error message
      if (response.status == 200) {
        // Check if it's a batch query and capture error messages
        if (batchErrors) {
          errorObject.message = batchErrors;
        }
        // Check if it's a single query and capture error message
        else {
          errorObject.message = response.data.errors[0].message;
        }
      }
      // If it's an Nginx errors return a proper error status code
      else {
        errorObject.message = response.bodyText;
      }

      // Check if error message is about expired JWT
      if (errorObject.message.includes("jwt expired")) {
        // Reset current user
        let currentUser = {
          isAuthenticated: false,
          role: "anonymous"
        };
        this.$store.commit("setCurrentUser", currentUser);
      }
      // If not, display the error message
      else {
        errorObject.flag = true;
        this.$store.commit("setErrorObject", errorObject);
      }
    },
    statusCssClass(status) {
      let cssClass;
      if (status == "Pending") {
        cssClass = "badge-secondary";
      } else if (status == "Running") {
        cssClass = "badge-info";
      } else if (status == "Success") {
        cssClass = "badge-success";
      } else if (status == "Failed") {
        cssClass = "badge-danger";
      } else if (status == "Killed") {
        cssClass = "badge-light";
      }
      return cssClass;
    }
  }
};
</script>
