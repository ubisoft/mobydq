/* eslint-disable */
// Disable because it's much more convenient to have all classes/roles with their permissions in one file.
/**
 * The Permissions of each role.
 * r = READ
 * w = WRITE
 */
class UserRolePermissions {
  static getPermissionsObjectByRole(role) {
    switch (role) {
      case 'admin':
        return new UserRolePermissions.Admin();
      case 'advanced':
        return new UserRolePermissions.Advanced();
      case 'standard':
        return new UserRolePermissions.Standard();
      default:
        return new UserRolePermissions.Anonymous();
    }
  }
}

UserRolePermissions.Anonymous = class Anonymous {
  permissions;

  constructor() {
    this.permissions = [
      'r_data_sources',
      'r_data_source_types',
      'r_indicators',
      'r_indicator_groups',
      'r_indicator_types',
      'r_indicator_parameters',
      'r_indicator_parameter_types',
      'r_batches',
      'r_sessions',
      'r_session_results'
    ];
  }
};

UserRolePermissions.Standard = class Standard extends UserRolePermissions.Anonymous {
  constructor() {
    super();
    this.permissions.push(
      'w_indicators',
      'w_indicator_groups',
      'w_indicator_parameters',
      'w_batches',
      'w_sessions',
      'w_session_results',
      'r_users',
      'r_user_groups'
    );
  }
};

UserRolePermissions.Advanced = class Advanced extends UserRolePermissions.Standard {
  constructor() {
    super();
    this.permissions.push(
      'w_data_sources'
    );
  }
};

UserRolePermissions.Admin = class Admin extends UserRolePermissions.Advanced {
  constructor() {
    super();
    this.permissions.push(
      'w_data_source_types',
      'w_indicator_types',
      'w_indicator_parameters',
      'w_users',
      'w_user_groups'
    );
  }
};

export default UserRolePermissions;
