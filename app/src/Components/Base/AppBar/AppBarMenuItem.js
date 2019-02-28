import React from 'react';

export const AppBarMenuItem = ({ icon, label, action }) => <div style={{'width': '150px', 'padding': '10px', 'cursor': 'pointer'}} role="button" onClick={() => action()}>
  <div style={{'float': 'left'}}>{icon}</div>
  <div style={{'padding': '4px 10px 4px 15px'}}>{label}</div>
</div>