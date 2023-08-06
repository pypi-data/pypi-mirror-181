import * as React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import { theme } from './../theme';
import { executeRpc, globalUnhandledRejection } from './../lib/RPCUtils';
import NotebookUtils from './../lib/NotebookUtils';
import { Kernel } from '@jupyterlab/services';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getTransformerEnabled, setTransformerEnabled, addStatusChangeListener, StatusContent, triggerStatusUpdate, setTransformerNotebookPath } from './../settings';
import { saveTransformerNotebook } from './../notebook';
import {
    Switch,
    Divider,
    Typography,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Collapse,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    CircularProgress,
    Select,
    MenuItem
} from '@material-ui/core';
import InfoIcon from '@material-ui/icons/Info';
import ExpandMoreIcon from '@material-ui/icons/ExpandMoreRounded';
import RefreshIcon from '@material-ui/icons/Refresh';

interface IProps {
    transformerSettings: ISettingRegistry.ISettings
}

type ClickHandler = () => void;
interface IState {
    isEnabled: boolean;
    dialogTitle: string;
    dialogContent: string;
    isDialogVisible: boolean;
    isDialogCloseButtonVisible: boolean;
    closeButtonText: string;
    isDialogConfirmButtonVisible: boolean;
    dialogConfirmClickHandler: ClickHandler;
    showApplyTransformerDescription: boolean;
    showResetTransformerDescription: boolean;
    proxyUrl: string;
    proxyStatus: string;
    transformerNotebookPath: string;
    transformerNotebookPathOptions: string[];
    isStatusLoading: boolean;
}

interface IDialogParams {
    visible?: boolean;
    title?: string;
    content?: string;
    isCloseButtonVisible?: boolean;
    closeButtonText?: string;
    isConfirmButtonVisible?: boolean;
}

export class TransformerLeftPanel extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);
        this.onDialogCloseClick = this.onDialogCloseClick.bind(this);
        this.onDialogConfirmClick = this.onDialogConfirmClick.bind(this);
        this.doResetTransformer = this.doResetTransformer.bind(this);
        this.doReloadPage = this.doReloadPage.bind(this);
        this.refreshStatus = this.refreshStatus.bind(this);
        this.changetransformerNotebookPath = this.changetransformerNotebookPath.bind(this);
        const defaultState: IState = {
            isEnabled: getTransformerEnabled(),
            isDialogVisible: false,
            isDialogCloseButtonVisible: true,
            dialogTitle: '',
            dialogContent: '',
            closeButtonText: 'Ok',
            isDialogConfirmButtonVisible: false,
            dialogConfirmClickHandler: this.onDialogConfirmClick,
            showApplyTransformerDescription: false,
            showResetTransformerDescription: false,
            proxyUrl: '',
            proxyStatus: 'Unavailable',
            transformerNotebookPath: '',
            transformerNotebookPathOptions: [],
            isStatusLoading: true
        };
        this.state = defaultState;
    }

    renderDialog({
        visible,
        title,
        content,
        isCloseButtonVisible,
        closeButtonText,
        isConfirmButtonVisible
    }: IDialogParams) {
        this.setState({
            isDialogVisible: visible !== undefined? visible: true,
            dialogTitle: title !== undefined? title: '',
            dialogContent: content !== undefined? content: '',
            isDialogCloseButtonVisible: isCloseButtonVisible !== undefined? isCloseButtonVisible: true,
            closeButtonText: closeButtonText !== undefined? closeButtonText: 'Ok',
            isDialogConfirmButtonVisible: isConfirmButtonVisible !== undefined? isConfirmButtonVisible: false
        });
    }

    changetransformerNotebookPath(value: string) {
        this.setState({
            transformerNotebookPath: value
        });
        setTransformerNotebookPath(this.props.transformerSettings, value);
    }

    refreshStatus() {
        this.setState({
            isStatusLoading: true
        });
        triggerStatusUpdate(this.props.transformerSettings);
    }

    onDialogCloseClick() {
        this.renderDialog({
            visible: !this.state.isDialogVisible
        });
    }

    onDialogConfirmClick() {
        console.log("onDialogConfirmClick");
        this.renderDialog({
            visible: !this.state.isDialogVisible
        });
    }

    componentDidMount = () => {
        addStatusChangeListener((status: StatusContent) => {
            this.setState({
                proxyUrl: status.proxy_url,
                proxyStatus: status.proxy_status,
                transformerNotebookPath: status.notebook_path,
                transformerNotebookPathOptions: status.nb_path_options,
                isStatusLoading: false
            });
        });
    };

    componentDidUpdate = (
        prevProps: Readonly<IProps>,
        prevState: Readonly<IState>,
    ) => {
    };

    applyTransformerToProxy = async () => {
        console.log('applyTransformerToProxy');
        this.renderDialog({
            title: 'Info',
            content: 'This will save the changes and apply them to proxy!',
            isCloseButtonVisible: true,
            closeButtonText: 'Cancel',
            isConfirmButtonVisible: true
        });
        this.setState({ dialogConfirmClickHandler: this.doApplyTransformer });
    };

    doApplyTransformer = async () => {
        this.renderDialog({
            title: 'Running',
            content: 'This will take few seconds!',
            isCloseButtonVisible: false
        });
        saveTransformerNotebook();

        let proxyUrl: string = this.state.proxyUrl;
        if(! proxyUrl) {
            this.renderDialog({
                title: 'Error',
                content: 'Unable to get the proxy URL!'
            });
            this.setState({ dialogConfirmClickHandler: this.onDialogConfirmClick });
            return;
        }

        try {
            const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
            const args = {
                proxy_url: proxyUrl,
                source_notebook_path: this.state.transformerNotebookPath
            }
            await executeRpc(kernel, 'proxy.apply', args);
            kernel.shutdown();
            this.renderDialog({
                title: 'Done',
                content: 'The transforming is completed!!'
            });
        } catch (error) {
            globalUnhandledRejection({ reason: error });
            this.renderDialog({
                visible: false
            });
        }
        this.setState({ dialogConfirmClickHandler: this.onDialogConfirmClick });
    };

    resetTransformer = () => {
        console.log('resetTransformer');
        this.renderDialog({
            title: 'Warning',
            content: 'This will reset transformer.ipynb and you may lose your code!',
            closeButtonText: 'Cancel',
            isConfirmButtonVisible: true
        });
        this.setState({ dialogConfirmClickHandler: this.doResetTransformer });
    };

    doResetTransformer = async () => {
        console.log("doResetTransformer");
        let proxyUrl: string = this.state.proxyUrl;
        if(! proxyUrl) {
            this.renderDialog({
                title: 'Error',
                content: 'Unable to get the proxy URL!'
            });
            this.setState({ dialogConfirmClickHandler: this.onDialogConfirmClick });
            return;
        }

        try {
            this.renderDialog({
                title: 'Running',
                content: 'This will take few seconds!'
            });
            const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
            const args = {
                proxy_url: proxyUrl,
                source_notebook_path: this.state.transformerNotebookPath
            }
            await executeRpc(kernel, 'proxy.reset', args);
            kernel.shutdown();
            this.renderDialog({
                title: 'Reset is done',
                content: 'You need to reload the page!',
                isCloseButtonVisible: false,
                isConfirmButtonVisible: true
            });
            this.setState({ dialogConfirmClickHandler: this.doReloadPage });
            return;
        } catch (error) {
            globalUnhandledRejection({ reason: error });
            this.renderDialog({
                visible: false
            });
        }
    };

    doReloadPage = async () => {
        this.renderDialog({
            visible: false
        });
        window.location.reload();
    };

    onTransformerEnableChanged = (enabled: boolean) => {
        this.setState({ isEnabled: enabled });
        setTransformerEnabled(this.props.transformerSettings, enabled);
    };

    render() {
        return (
            <ThemeProvider theme={theme}>
                <div className={'leftpanel-transformer-widget'} key="transformer-widget" style={{padding: 'var(--jp-code-padding)'}}>
                    <div className={'leftpanel-transformer-widget-content'}>
                        <Typography variant="h5" gutterBottom>Transformer Panel</Typography>

                        <div className='transformer-component' >
                            <Typography variant="body1" gutterBottom style={{ color: theme.transformer.headers.main }}>
                                Transformer is the extension for model inference, it helps you customizing the proxy API handlers by defining the corresponding functions on <strong style={{ fontWeight: '600' }}>transformer.ipynb</strong> notebook.
                            </Typography>
                        </div>

                        <div className="transformer-toggler">
                            <React.Fragment>
                                <div className="toolbar input-container">
                                    <Switch
                                        checked={this.state.isEnabled}
                                        onChange={c => this.onTransformerEnableChanged(c.target.checked)}
                                        color="primary"
                                        name="enable-transformer"
                                        inputProps={{ 'aria-label': 'primary checkbox' }}
                                        classes={{ root: 'material-switch' }}
                                    />
                                    <div className={'switch-label'} style={{ display: 'inline-block' }}>
                                        <Typography variant="overline" display="block">{(this.state.isEnabled ? 'Disable' : 'Enable') + ' widgets'}</Typography>
                                    </div>
                                </div>
                            </React.Fragment>
                        </div>
                        <div className={ 'transformer-component' + (this.state.isEnabled ? '' : ' hidden') } style={{ marginTop: '1em' }}>
                            <Divider variant="middle" style={{ margin: '1em 0' }} />
                            <Typography variant="subtitle2" display="block" gutterBottom>
                                STATUS
                                <span>
                                    {this.state.isStatusLoading && <CircularProgress size={16} style={{ position: "relative", top: "0.2em", left: "0.5em"}}/>}
                                    {!this.state.isStatusLoading && <RefreshIcon onClick={this.refreshStatus} color="primary" fontSize="small" style={{ position: "relative", top: "0.25em", left: "0.2em", cursor: "pointer" }}/>}
                                </span>
                            </Typography>
                            <Accordion style={{ margin: '0 0.2em' }}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls="panel1a-content"
                                >
                                    <Typography variant="subtitle2"
                                        style={{ color: this.state.proxyUrl? 'green': 'red' }}
                                    >Proxy URL: {this.state.proxyUrl? 'Set': 'Empty'}</Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Typography variant="body2" gutterBottom>
                                        {this.state.proxyUrl? 'Proxy URL is now: ' + this.state.proxyUrl: 'Unable to retrieve proxy URL from system settings.'}
                                    </Typography>
                                </AccordionDetails>
                            </Accordion>
                            <Accordion style={{ margin: '0 0.2em' }}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls="panel1a-content"
                                >
                                    <Typography variant="subtitle2"
                                        style={{ color: this.state.proxyStatus === 'healthy'? 'green': 'red' }}
                                    >Proxy status: {this.state.proxyStatus === 'healthy'? 'Available': 'Unavailable'}</Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Typography variant="body2" gutterBottom>
                                        {this.state.proxyStatus === 'healthy'? 'Ready to apply transformer to proxy.': 'Lose connection to proxy server!'}
                                    </Typography>
                                </AccordionDetails>
                            </Accordion>
                            <Accordion style={{ margin: '0 0.2em' }}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls="panel1a-content"
                                >
                                    <Typography variant="subtitle2"
                                        style={{ color: this.state.transformerNotebookPath? 'green': 'red' }}
                                    >Transformer NB: {this.state.transformerNotebookPath? 'Set': 'Unknown'}</Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <div>
                                        <Select
                                            value={this.state.transformerNotebookPath}
                                            onChange={e => this.changetransformerNotebookPath(e.target.value as string)}
                                        >
                                        {this.state.transformerNotebookPathOptions.map((value) => (
                                            <MenuItem key={value} value={value}>{value}</MenuItem>
                                        ))}
                                        </Select>
                                        <Typography variant="body2" display="block" gutterBottom>
                                            {this.state.transformerNotebookPath? 'Notebook(' + this.state.transformerNotebookPath + ') will be applied.': 'Notebook transformer.ipynb is not found!'}
                                        </Typography>
                                    </div>
                                </AccordionDetails>
                            </Accordion>
                        </div>
                        <div className={ 'transformer-component' + (this.state.isEnabled ? '' : ' hidden') } style={{ marginTop: '1em' }}>
                            <Divider variant="middle" style={{ margin: '1em 0' }} />
                            <Typography variant="subtitle2" display="block" gutterBottom>
                                APPLY TRANSFORMER
                                <InfoIcon
                                    onClick={() => this.setState({
                                        showApplyTransformerDescription: !this.state.showApplyTransformerDescription
                                    }) }
                                    aria-label="show more"
                                    style={{ position: "relative", top: "0.25em", margin: "0 0.2em", cursor: "pointer" }}
                                />
                            </Typography>
                            <Collapse in={this.state.showApplyTransformerDescription} timeout="auto" unmountOnExit>
                                <Typography variant="body1" gutterBottom style={{ color: theme.transformer.headers.main }}>
                                    Convert <strong style={{ fontWeight: '600' }}>transformer.ipynb</strong> to runnable handlers and apply them on proxy.
                                </Typography>
                            </Collapse>
                            <div className="input-container add-button">
                                <Button
                                    variant="contained"
                                    color="primary"
                                    size="small"
                                    title="Apply the changes."
                                    onClick={this.applyTransformerToProxy}
                                    disabled={ false }
                                >Now Apply</Button>
                            </div>
                        </div>
                        <div className={ 'transformer-component' + (this.state.isEnabled ? '' : ' hidden') } style={{ marginTop: '1em' }}>
                            <Divider variant="middle" style={{ margin: '1em 0' }} />
                            <Typography variant="subtitle2" display="block" gutterBottom>
                                RESET TRANSFORMER
                                <InfoIcon
                                    onClick={() => this.setState({
                                        showResetTransformerDescription: !this.state.showResetTransformerDescription
                                    }) }
                                    aria-label="show more"
                                    style={{ position: "relative", top: "0.25em", margin: "0 0.2em", cursor: "pointer" }}
                                />
                            </Typography>
                            <Collapse in={this.state.showResetTransformerDescription} timeout="auto" unmountOnExit>
                                <Typography variant="body1" gutterBottom style={{ color: theme.transformer.headers.main }}>
                                    <strong style={{ fontWeight: '600' }}>Reset {this.state.transformerNotebookPath? this.state.transformerNotebookPath: 'transformer.ipynb'}</strong>
                                    <br />
                                    This action also reset the API handlers on proxy.
                                </Typography>
                            </Collapse>
                            <div className="input-container add-button">
                                <Button
                                    variant="contained"
                                    color="secondary"
                                    size="small"
                                    title="Reset Transformer"
                                    onClick={this.resetTransformer}
                                    disabled={ false }
                                >Now Reset</Button>
                            </div>
                        </div>
                    </div>
                </div>
                <Dialog
                    open={this.state.isDialogVisible}
                    fullWidth={true}
                    maxWidth={'sm'}
                    scroll="paper"
                    aria-labelledby="scroll-dialog-title"
                    aria-describedby="scroll-dialog-description"
                >
                    <DialogTitle id="scroll-dialog-title">
                        <p className={'dialog-title'} >{this.state.dialogTitle}</p>
                    </DialogTitle>
                    <DialogContent dividers={true}>
                        <p>{this.state.dialogContent}</p>
                    </DialogContent>
                    <DialogActions>
                        <Button
                            className={ 'transformer-dialog ' + (this.state.isDialogConfirmButtonVisible ? '' : 'hidden') }
                            color="secondary"
                            onClick={this.state.dialogConfirmClickHandler}
                        >Confirm</Button>
                        <Button
                            className={ 'transformer-dialog ' + (this.state.isDialogCloseButtonVisible ? '' : 'hidden') }
                            color="primary"
                            onClick={this.onDialogCloseClick}
                        >{this.state.closeButtonText}</Button>
                    </DialogActions>
                </Dialog>
            </ThemeProvider>
        );
    }
}
