import gql from 'graphql-tag';

class ParameterRepository {
  static getFormDropdownData() {
    return gql`
      {
        allParameterTypes {
          nodes {
            id
            name
          }
        }
      }
    `;
  }

  static display() {
    return gql`
        query getParameter($id: Int!) {
          parameterById(id: $id) {
            id
            value
            createdDate
            userByCreatedById { email }
            updatedDate
            userByUpdatedById { email }
            userGroupId
            indicatorId
            parameterTypeId

          }
        }
    `;
  }

  static insert() {
  return gql`
    mutation addNewParameter($parameter: ParameterInput!) {
      createParameter(input: {parameter: $parameter}) {
        parameter {
          id
          value
          indicatorId
          parameterTypeId
          createdDate
          updatedDate
        }
      }
    }
  `;
  }

  static update() {
  return gql`
    mutation updateParameterById($parameterPatch: ParameterPatch!, $id: Int!) {
      updateParameterById(input: {parameterPatch: $parameterPatch, id: $id }) {
        parameter {
          id
          value
          indicatorId
          parameterTypeId
          createdDate
          updatedDate
        }
      }
    }
  `;
  }

  static delete() {
  return gql`
    mutation deleteParameterById($id: Int!) {
      deleteParameterById(input: { id: $id }) {
        parameter {
          id
        }
      }
    }
  `;
  }
}

export default ParameterRepository;