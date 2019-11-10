export const mutationCreateParameter = `mutation createParameter($parameter: ParameterInput!) {
    createParameter(input: {parameter: $parameter}) {
        parameter {
            id
            parameterTypeId
            parameterTypeByParameterTypeId { name }
            value
            createdDate
            updatedDate
            userByCreatedById { email }
            userByUpdatedById { email }
        }
    }
}`;

export const mutationUpdateParameter = `mutation updateParameter($id: Int!, $parameterPatch: ParameterPatch!) {
    updateParameterById(input: {id: $id, parameterPatch: $parameterPatch }) {
        parameter {
            id
            parameterTypeId
            parameterTypeByParameterTypeId { name }
            value
            createdDate
            updatedDate
            userByCreatedById { email }
            userByUpdatedById { email }
        }
    }
}`;

export const mutationDeleteParameter = `mutation deleteParameter($id: Int!) {
    deleteParameterById(input: {id: $id}) {
        parameter {
            id
        }
    }
}`;

// Response labels must be formatted according to Treeselect requirements
export const queryGetParameterTypes = `query getAllParameterTypes {
    allParameterTypes(orderBy: NAME_ASC) {
        nodes {
            id
            label:name
        }
    }
}`;
