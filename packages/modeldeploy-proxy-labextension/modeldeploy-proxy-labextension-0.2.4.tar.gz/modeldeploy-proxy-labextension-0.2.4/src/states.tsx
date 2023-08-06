import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { Token } from '@lumino/coreutils';

const id = 'transformer-extension:ITransformerStates';
const ITransformerStates = new Token<ITransformerStates>(id);
export interface ITransformerStates {
    isPredictTagged?: boolean;
    isRequirementsTagged?: boolean;
    isCVATInfoTagged?: boolean;
    isCVATInvokeTagged?: boolean;
}

let transformerStatesList: {
    [key: string]: {
        states: ITransformerStates,
        listeners: ((trigger: string, newStates: ITransformerStates) => void)[]
    }
} = {};
const assertTransformerStates = (notebookPanelId: string) => {
    if(! transformerStatesList[notebookPanelId]) {
        let transformerStates: ITransformerStates = {
            isPredictTagged: false,
            isRequirementsTagged: false,
            isCVATInfoTagged: false,
            isCVATInvokeTagged: false
        }
        let stateChangeListeners: ((trigger: string, newStates: ITransformerStates) => void)[] = [];
        transformerStatesList[notebookPanelId] = {
            states: transformerStates,
            listeners: stateChangeListeners
        };
    }
}

export const fetchTransformerStates = (notebookPanelId: string): ITransformerStates => {
    if(! transformerStatesList[notebookPanelId]) {
        assertTransformerStates(notebookPanelId);
    }
    return transformerStatesList[notebookPanelId].states;
}

export const issueTransformerStatesChange = (notebookPanelId: string, issuer: string, states: ITransformerStates): void => {
    if(! transformerStatesList[notebookPanelId]) {
        assertTransformerStates(notebookPanelId);
    }
    Object.assign(transformerStatesList[notebookPanelId].states, states)
    transformerStatesList[notebookPanelId].listeners.forEach(callback => {
        callback(issuer, states);
    });
}

export const addStatesChangeListener = (notebookPanelId: string, callback: (trigger: string, newStates: ITransformerStates) => void): void => {
    if(! transformerStatesList[notebookPanelId]) {
        assertTransformerStates(notebookPanelId);
    }
    transformerStatesList[notebookPanelId].listeners.push(callback);
}

export default {
    id: 'modeldeploy-proxy-labextension:states',
    provides: ITransformerStates,
    autoStart: true,
    activate: (
        app: JupyterFrontEnd,
    ): void => {
        app.started.then(() => {
        });

        app.restored.then(async () => {
        });
    }
} as JupyterFrontEndPlugin<ITransformerStates>;
