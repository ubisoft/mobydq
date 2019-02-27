
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import PersonIcon from '@material-ui/icons/Person';
import IconButton from '@material-ui/core/IconButton/IconButton';
import Divider from '@material-ui/core/Divider';
import Popover from '@material-ui/core/Popover';
import React from 'react';
import { setUserMenuAnchor } from '../../../actions/topbar';
import { AppBarMenuItem } from './AppBarMenuItem';

class UserMenu extends React.Component {
constructor() {
  super();
  this.logout = this.logout.bind(this);
  this.admin = this.admin.bind(this);
}

handleClick(event) {
  this.props.setUserMenuAnchor(event.currentTarget); 
}  

logout() {
  document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
  alert("user logged out.")
  this.props.history.push('/login');
}

admin() {
  this.props.history.push('/admin');
}

render() {
  const open = Boolean(this.props.userMenuAnchor);
  return <React.Fragment>
    <IconButton color="inherit" color="inherit" 
    aria-label="Open user menu" onClick={(event) => {this.handleClick(event)}} >
      <PersonIcon />
    </IconButton>
    <Popover 
        open={open}
        anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
        }}
        anchorEl={this.props.userMenuAnchor}
        onClose={() => {
          this.props.setUserMenuAnchor(null);
        }}
        transformOrigin={{
            vertical: 'top',
            horizontal: 'center',
        }}
      >
        <div><AppBarMenuItem icon={null} label='Admin' action={this.admin}/></div>
        <div><AppBarMenuItem icon={null} label='Logout' action={this.logout}/></div>
        <div><AppBarMenuItem icon={<Divider/>} label='' action={null}/></div>
    </Popover>
    </React.Fragment>;
  }
}

const mapStateToProps = (state) => ({
  'userMenuAnchor': state.userMenuAnchor
});

const mapDispatchToProps = (dispatch) => ({
  'setUserMenuAnchor': (anchor) => dispatch(setUserMenuAnchor(anchor)),
});


export default withRouter(connect(mapStateToProps, mapDispatchToProps)(UserMenu));