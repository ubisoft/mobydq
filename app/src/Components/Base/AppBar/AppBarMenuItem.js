import React from 'react';
import ListItem from '@material-ui/core/ListItem';

export const AppBarMenuItem = ({ icon, label, action }) => <ListItem style={{'width': '150px', 'padding': '10px', 'cursor': 'pointer'}} button onClick={() => action()}>
  <div style={{'float': 'left'}}>{icon}</div>
  <div style={{'padding': '4px 10px 4px 15px'}}>{label}</div>
</ListItem>