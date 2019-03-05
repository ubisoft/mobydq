import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SaveButton from './../FormInput/SaveButton';
import ExecuteButton from './../FormInput/ExecuteButton';
import DeleteButton from './../FormInput/DeleteButton';
import LinkButton from './../FormInput/LinkButton';

const UserGroupFormFields = (props) => {
  const {
    data,
    values,
    touched,
    errors,
    handleChange,
    handleBlur,
    handleSubmit,
    isSubmitting
  } = props;
  return <form onSubmit={handleSubmit} style={{ 'marginLeft': '50px' }}>
    <div style={{ 'marginTop': '10px', 'marginBottom': '30px' }}>
      <SaveButton disabled={isSubmitting} />
      <ExecuteButton onClick={() => alert('not yet implemented')}/>
    </div>
    <div>
      <TextInput
        id="name"
        label="Name"
        helperText=""
        placeholder=""
        touched={touched.name}
        error={touched.name && errors.name}
        value={values.name}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
    <div>
      <TextInput
        id="createdDate"
        label="Created Date"
        helperText=""
        placeholder=""
        touched={touched.createdDate}
        error={touched.createdDate && errors.createdDate}
        value={values.createdDate}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
    <div>
      <TextInput
        id="createdBy"
        label="Created By"
        helperText=""
        placeholder=""
        touched={touched.createdBy}
        error={touched.createdBy && errors.createdBy}
        value={values.createdBy}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
    <div>
      <TextInput
        id="updatedDate"
        label="Updated Date"
        helperText=""
        placeholder=""
        touched={touched.updatedDate}
        error={touched.updatedDate && errors.updatedDate}
        value={values.updatedDate}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
    <div>
      <TextInput
        id="updatedBy"
        label="Updated By"
        helperText=""
        placeholder=""
        touched={touched.updatedBy}
        error={touched.updatedBy && errors.updatedBy}
        value={values.updatedBy}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
  </form>;
};

const formikEnhancer = withFormik({
  'validationSchema': Yup.object().shape({
    'name': Yup.string()
      .required('Name cannot be blank')
  }),
  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? {
      'name': ''
    }
    : {
      'id': props.initialFieldValues.userGroupId,
      'name': props.initialFieldValues.name,
      'createdDate': props.initialFieldValues.createdDate,
      'createdBy': props.initialFieldValues.userByCreatedById.email,
      'updatedDate': props.initialFieldValues.updatedDate,
      'updatedBy': props.initialFieldValues.userByUpdatedById.email
    },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    delete payload.createdDate;
    delete payload.createdBy;
    delete payload.updatedDate;
    delete payload.updatedBy;
    let variables;
    if (props.initialFieldValues === null) {
      variables = { 'userGroup': payload };
    } else {
      variables = { 'userGroupPatch': payload, 'id': props.initialFieldValues.id };
    }
    props.mutate({
      variables
    });
  },
  'displayName': 'UserGroupForm'
});


const EnhancedUserGroupForm = formikEnhancer(UserGroupFormFields);

export default EnhancedUserGroupForm;
