import React from 'react';
import { Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import PlayArrow from '@material-ui/icons/PlayArrow';
import Snackbar from '@material-ui/core/Snackbar';


class ExecuteRowButton extends React.Component {
    constructor() {
        super();
        this.state = {
            'open': false
        };
    }

    handleSnackbarClose() {
        this.setState({
            'open': false
        });
    }

    render() {
        return (<Mutation
            key={`execute_${this.props.recordId}`}
            mutation={this.props.parameter.repository.execute()}
            variables={{ 'id': this.props.recordId }}>
            {(executeFunc, params) => {
                const { loading, error, called, data } = params;
                if (loading) {
                    return <p>Loading...</p>;
                } else if (called && !loading) {
                    if (!this.state.open) {
                        const responseData = data['executeBatch']['batch'];
                        this.setState({
                            'open': true,
                            'message': `Batch ${responseData.id}: ${responseData.status}`
                        });
                    }
                } else if (error) {
                    return <p>Error...</p>;
                }

                return (
                    <div>
                        <Snackbar
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'left',
                            }}
                            open={this.state.open}
                            autoHideDuration={6000}
                            message={<span>{this.state.message}</span>}
                            onClose={this.handleSnackbarClose.bind(this)}>
                        </Snackbar>
                        <IconButton key={`execute_${this.props.recordId}`} onClick={executeFunc} color="primary">
                            <PlayArrow />
                        </IconButton>
                    </div>
                );
            }}
        </Mutation>);
    }
}


export default function createExecuteRowButton(button, recordId) {
    return React.createElement(ExecuteRowButton, {
        'parameter': button.parameter,
        'recordId': recordId
    });
}
