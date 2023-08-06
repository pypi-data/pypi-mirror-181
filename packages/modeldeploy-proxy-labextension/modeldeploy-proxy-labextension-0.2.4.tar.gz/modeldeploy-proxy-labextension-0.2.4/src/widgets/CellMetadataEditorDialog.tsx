import * as React from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from '@material-ui/core';

interface ICellMetadataEditorDialog {
    open: boolean;
    title: string;
    content: string;
    code: string;
    toggleDialog: Function;
}

export const CellMetadataEditorDialog: React.FunctionComponent<ICellMetadataEditorDialog> = props => {
    const handleClose = () => {
        props.toggleDialog();
    };

    return (
        <Dialog
            open={props.open}
            onClose={handleClose}
            fullWidth={true}
            maxWidth={'sm'}
            scroll="paper"
            aria-labelledby="scroll-dialog-title"
            aria-describedby="scroll-dialog-description"
        >
            <DialogTitle id="scroll-dialog-title">
                <p className={'dialog-title'} >{props.title}</p>
            </DialogTitle>
            <DialogContent dividers={true}>
                <p>
                    {props.content}
                </p>
                <div className={ 'dialog-code-snippet' + ((props.code)? '' : ' hidden') }>
                    <code style={{ whiteSpace: "pre"}}>
                        {props.code}
                    </code>
                </div>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose} color="primary">Ok</Button>
            </DialogActions>
        </Dialog>
    );
};
