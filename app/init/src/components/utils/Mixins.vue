<script>
export default {
  methods: {
    displayError(response, batchErrors = null) {
      // Method to display error message
      let errorObject = {
        flag: true,
        message: ""
      };
      // PostGraphile errors return status 200 with error message
      if (response.status == 200) {
        // Batch queries
        if (batchErrors) {
          errorObject.message = batchErrors;
        }
        // Single query
        else {
          errorObject.message = response.data.errors[0].message;
        }
      }
      // Nginx errors return a proper error status code
      else {
        errorObject.message = response.bodyText;
      }
      this.$store.commit("setErrorObject", errorObject);
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
