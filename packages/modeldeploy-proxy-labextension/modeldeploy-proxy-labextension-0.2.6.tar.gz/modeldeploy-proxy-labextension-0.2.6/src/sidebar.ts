import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IToolbarWidgetRegistry, createToolbarFactory } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { CellBarExtension } from '@jupyterlab/cell-toolbar';
import { treeViewIcon } from '@jupyterlab/ui-components';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { SETTINGS_ID, getTransformerEnabled } from './settings';
import { TRANSFORMER_NB_FILE_NAME } from './notebook';

const SIDEBAR_ID = 'modeldeploy-proxy-labextension:sidebar';
const TRANSFORMER_FACTORY = 'transformer';

let isTransformerEnabled: boolean = true;
const updateTransformerEnabled = (settings: ISettingRegistry.ISettings): void => {
    isTransformerEnabled = getTransformerEnabled();
};

let isTransformerNotebook: boolean = false;
const handleNotebookChanged = async (notebookTracker: INotebookTracker, notebookPanel: NotebookPanel) => {
    if (notebookPanel.title.label == TRANSFORMER_NB_FILE_NAME) {
        isTransformerNotebook = true;
    } else {
        isTransformerNotebook = false;
    }
}

const isEnabled = (): boolean => {
    return isTransformerEnabled && isTransformerNotebook;
};


export default {
    id: SIDEBAR_ID,
    requires: [INotebookTracker, ISettingRegistry],
    autoStart: true,
    activate: async (
        app: JupyterFrontEnd,
        notebookTracker: INotebookTracker,
        settingRegistry: ISettingRegistry | null,
        toolbarRegistry: IToolbarWidgetRegistry | null,
        translator: ITranslator | null
    ) => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(([settings]) => {
            settings.changed.connect(updateTransformerEnabled);
            isTransformerEnabled = getTransformerEnabled();
        });

        if(notebookTracker) {
            notebookTracker.currentChanged.connect(handleNotebookChanged);
        }

        app.commands.addCommand(
            'notebook:transformer', {
                label: 'Transformer',
                caption: 'Enable/disable transformer annotation widgets.',
                execute: args => {
                    let currentCellIndex: number = notebookTracker.currentWidget.content.activeCellIndex;
                    let toggle: HTMLElement = (<Element>notebookTracker.currentWidget.content.node.childNodes[currentCellIndex]).querySelector('.transformer-cell-metadata-editor-toggle') as HTMLElement;
                    toggle.click();
                },
                icon: args => (args.toolbar ? treeViewIcon : ''),
                isEnabled: isEnabled
        });
        const toolbarItems = settingRegistry && toolbarRegistry ? createToolbarFactory(
            toolbarRegistry,
            settingRegistry,
            TRANSFORMER_FACTORY,
            SIDEBAR_ID,
            translator ?? nullTranslator
        ) : undefined;

        app.docRegistry.addWidgetExtension(
            'Notebook',
            new CellBarExtension(app.commands, toolbarItems)
        );
    },
    optional: [IToolbarWidgetRegistry, ITranslator]
} as JupyterFrontEndPlugin<void>;
