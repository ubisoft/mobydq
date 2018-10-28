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

    handleSnackbarClose = () => this.setState({ 'open': false });

    execute = (func) => {
        func();
        this.setState({ 'open': true });
    }

    render() {
        return (<Mutation
            mutation={this.props.parameter.repository.execute()}
            variables={{ 'id': this.props.recordId }}>
            {(executeFunc, params) => {
                const { loading, error, called, data } = params;
                if (loading) {
                    return <p>Loading...</p>;
                }
                if (error) {
                    return <p>Error...</p>;
                }
                if (called && data) {
                    const responseData = data['executeBatch']['batch'];
                    if (responseData.id !== this.state.currentBatchId) {
                        this.setState({
                            'message': `Batch ${responseData.id}: ${responseData.status}`,
                            'currentBatchId': responseData.id
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
                            autoHideDuration={5000}
                            message={<span>{this.state.message}</span>}
                            onClose={this.handleSnackbarClose}>
                        </Snackbar>
                        <IconButton key={`execute_${this.props.recordId}`} onClick={() => this.execute(executeFunc)} color="primary">
                            <PlayArrow />
                        </IconButton>
                    </div>
                );
            }}
        </Mutation>);
    }
}


export default function createExecuteRowButton(button, recordId) {
    return <ExecuteRowButton
        key={`execute_${recordId}`}
        parameter={button.parameter}
        recordId={recordId}>
    </ExecuteRowButton>;
}
