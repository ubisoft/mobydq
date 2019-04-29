/**
 * The Permissions of each role.
 * r = READ
 * w = WRITE
 */
export default class UserRolePermissions {
  static getPermissionsObjectByRole(role){
    switch (role) {
      case 'admin':
        return new Admin();
      case 'advanced':
        return new Advanced();
      case 'Standard':
        return new Standard();
      default:
        return new Anonymous();
    }
  }
}
export class Anonymous {
  static get permissions() {
    return [
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
}

export class Standard extends Anonymous {
  static get permissions() {
    return Anonymous.permissions.push(
      'w_indicators',
      'w_indicator_groups',
      'w_indicator_parameters',
      'w_batches',
      'w_sessions',
      'w_session_results'
    );
  }
}

export class Advanced extends Standard {
  static get permissions() {
    return Standard.permissions.push(
      'w_data_sources',
    );
  }
}

export class Admin extends Advanced {
  static get permissions() {
    return Advanced.permissions.push(
      'w_data_source_types',
      'w_indicator_types',
      'w_indicator_parameters',
      'r_users',
      'w_users',
      'r_user_groups',
      'w_user_groups'
    );
  }
}
