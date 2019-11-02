<template>
  <div class="card text-white bg-secondary small p-2">
    <table>
      <tr>
        <td>Id:</td>
        <td>{{ id }}</td>
      </tr>
      <tr>
        <td>Created Date:</td>
        <td>{{ cleanCreatedDate }}</td>
      </tr>
      <tr>
        <td>Created By:</td>
        <td>{{ createdBy }}</td>
      </tr>
      <tr>
        <td>Updated Date:</td>
        <td>{{ cleanUpdatedDate }}</td>
      </tr>
      <tr>
        <td>Updated By:</td>
        <td>{{ updatedBy }}</td>
      </tr>
      <tr v-if="tableName">
        <td>Table Name:</td>
        <td>{{ tableName }}</td>
      </tr>
      <tr v-if="columnName">
        <td>Column Name:</td>
        <td>{{ columnName }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    id: Number,
    createdDate: String,
    createdBy: String,
    updatedDate: String,
    updatedBy: String,
    tableName: String,
    columnName: String
  },
  computed: {
    cleanCreatedDate() {
      return this.createdDate.replace("T", " ").substring(0, 19);
    },
    cleanUpdatedDate() {
      return this.updatedDate.replace("T", " ").substring(0, 19);
    }
  }
};
</script>
