import React from 'react';
import { Link } from 'react-router-dom'
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import ViewListIcon from '@material-ui/icons/ViewList';
import PeopleIcon from '@material-ui/icons/People';
import CategoryIcon from '@material-ui/icons/Category';
import LayersIcon from '@material-ui/icons/Layers';
import AssignmentIcon from '@material-ui/icons/Assignment';
import DvrIcon from '@material-ui/icons/Dvr';

export const mainListItems = (
  <div>
    <ListSubheader inset>Data Quality Framework</ListSubheader>
    <ListItem button component={Link} to="/">
      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard" />
    </ListItem>
      <ListItem button component={Link} to="/indicators">
      <ListItemIcon>
        <CategoryIcon />
      </ListItemIcon>
      <ListItemText primary="Indicators" />
    </ListItem>
    <ListItem button component={Link} to="/indicator-groups">
      <ListItemIcon>
        <ViewListIcon />
      </ListItemIcon>
      <ListItemText primary="Indicator Groups" />
    </ListItem>
    <ListItem button component={Link} to="/data-sources">
      <ListItemIcon>
        <DvrIcon />
      </ListItemIcon>
      <ListItemText primary="Data Sources" />
    </ListItem>
    <ListItem button component={Link} to="/admin">
      <ListItemIcon>
        <PeopleIcon />
      </ListItemIcon>
      <ListItemText primary="Admin" />
    </ListItem>
  </div>
);