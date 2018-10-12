import React from 'react';
import {styles} from './../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';

class NotFoundComponent extends React.Component {

    render() {
        return (
            <React.Fragment>
                <br/><br/><br/>
                <h1>404 Not Found</h1>
            </React.Fragment>
        )
    }
}

export default withStyles(styles)(NotFoundComponent);
