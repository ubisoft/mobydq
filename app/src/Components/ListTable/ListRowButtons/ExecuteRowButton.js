import React from 'react';
import { Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import PlayArrow from '@material-ui/icons/PlayArrow';


export default function createExecuteRowButton(button, recordId) {
    const { } = button.parameter;
    return (
        <Mutation
            key={`execute_${recordId}`}
            mutation={button.parameter.repository.execute()}
            variables={{ 'id': recordId }}>
            {(deleteFunc, { loading, error }) => {
                console.log(deleteFunc);
                if (loading) {
                    return <p>Loading...</p>;
                }
                if (error) {
                    return <p>Error...</p>;
                }
                return (
                    <IconButton key={`execute_${recordId}`} onClick={() => {
                        deleteFunc();
                    }} color="primary">
                        <PlayArrow />
                    </IconButton>
                );
            }}
        </Mutation>
    );
}
