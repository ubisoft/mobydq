import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import PersonIcon from '@material-ui/icons/Person';
import IconButton from '@material-ui/core/IconButton/IconButton';
import Divider from '@material-ui/core/Divider';
import Popover from '@material-ui/core/Popover';
import React from 'react';
import { setUserMenuAnchor } from '../../../actions/topbar';
import { setAlertDialog } from '../../../actions/app';
import { AppBarMenuItem } from './AppBarMenuItem';
import SessionUser from '../../../Authentication/SessionUser';

class UserMenu extends React.Component {
  constructor() {
    super();
    this.logout = this.logout.bind(this);
    this.handleLogout = this.handleLogout.bind(this);
    this.closeUserMenu = this.closeUserMenu.bind(this);
    this.login = this.login.bind(this);
    this.admin = this.admin.bind(this);
  }

  handleClick(event) {
    this.props.setUserMenuAnchor(event.currentTarget);
  }

  closeUserMenu() {
    this.props.setUserMenuAnchor(null);
  }

  logout() {
    this.props.setAlertDialog({
      'title': 'Log out',
      'description': 'Do you really want to log out?',
      'yesText': 'Yes',
      'noText': 'No',
      'onYes': this.handleLogout,
      'onNo': this.closeUserMenu
    });
  }

  handleLogout() {
    this.closeUserMenu();
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    this.props.history.push('/login');
  }

  login() {
    this.closeUserMenu();
    this.props.history.push('/login');
  }

  admin() {
    this.closeUserMenu();
    this.props.history.push('/admin');
  }

  render() {
    const open = Boolean(this.props.userMenuAnchor);
    return <React.Fragment>
      <IconButton color="inherit"
      aria-label="Open user menu" onClick={(event) => {
        this.handleClick(event);
      }} >
        <PersonIcon />
      </IconButton>
      <Popover
        open={open}
        anchorOrigin={{ 'vertical': 'bottom', 'horizontal': 'center' }}
        anchorEl={this.props.userMenuAnchor}
        onClose={() => {
          this.closeUserMenu();
        }}
        transformOrigin={{ 'vertical': 'top', 'horizontal': 'center' }}
      >
        <div><AppBarMenuItem icon={null} label={'Admin'} action={ this.admin }/></div>
        <Divider/>
        <div><AppBarMenuItem icon={null} label={ SessionUser.user ? 'Logout' : 'Login'} action={SessionUser.user ? this.logout : this.login }/></div>
      </Popover>
    </React.Fragment>;
  }
}

const mapStateToProps = (state) => ({
  'userMenuAnchor': state.userMenuAnchor,
  'alertDialog': state.alertDialog
});

const mapDispatchToProps = (dispatch) => ({
  'setUserMenuAnchor': (anchor) => dispatch(setUserMenuAnchor(anchor)),
  'setAlertDialog': (alertDialog) => dispatch(setAlertDialog(alertDialog))
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(UserMenu));
