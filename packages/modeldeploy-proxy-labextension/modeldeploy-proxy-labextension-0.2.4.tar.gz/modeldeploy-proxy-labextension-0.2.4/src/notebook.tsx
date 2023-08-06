import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel, Notebook } from '@jupyterlab/notebook';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { SETTINGS_ID, getTransformerEnabled } from './settings';
import { CellMetadataEditor, IProps as EditorProps } from './widgets/CellMetadataEditor';
import { Cell, ICellModel, isCodeCellModel, isRawCellModel } from '@jupyterlab/cells';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import TagsUtils from './lib/TagsUtils';
import { IObservableList, IObservableUndoableList } from '@jupyterlab/observables';

let transformerSettings: ISettingRegistry.ISettings;
export const TRANSFORMER_NB_FILE_NAME = 'transformer.ipynb'

let editors: EditorProps[] = [];
let isTransformerEnabled: boolean;
let transformerNotebookPanel: NotebookPanel = null;
export const saveTransformerNotebook = async () => {
    if(transformerNotebookPanel) {
        await transformerNotebookPanel.context.ready;
        await transformerNotebookPanel.context.save();
    }
}
const handleNotebookChanged = async (notebookTracker: INotebookTracker, notebookPanel: NotebookPanel) => {
    if (notebookPanel.title.label == TRANSFORMER_NB_FILE_NAME) {
        console.log("Now " + TRANSFORMER_NB_FILE_NAME + "...");
        if(editors.length != notebookPanel.model.cells.length) {
            makeCellTransformerWidgets(notebookPanel);
        }
        notebookPanel.content.activeCellChanged.connect((notebook: Notebook, activeCell: Cell) => {
            let cellElement: HTMLElement = notebook.node.childNodes[notebook.activeCellIndex] as HTMLElement;
            let transformerWidget: HTMLElement = cellElement.querySelector('.cell-transformer-widget') as HTMLElement;
            if(! transformerWidget) {
                const transformerTag = TagsUtils.getCellTransformerTag(notebookPanel, notebook.activeCellIndex);
                let cellId = notebookPanel.model.cells.get(notebook.activeCellIndex).id;
                createCellTransformerWidgets(cellId, notebookPanel, cellElement, transformerTag, isTransformerEnabled);
            }
        });

        notebookPanel.model.cells.changed.connect((cells: IObservableUndoableList<ICellModel>, change: IObservableList.IChangedArgs<ICellModel>) => {
            makeCellTransformerWidgets(notebookPanel);
        });

        transformerNotebookPanel = notebookPanel;
    }
}

const makeCellTransformerWidgets = (notebookPanel: NotebookPanel) => {
    const cells = notebookPanel.model.cells;
    for (let index = 0; index < cells.length; index++) {
        let cellId: string = cells.get(index).id;
        let existedItems = editors.filter(item => item['cellId'] === cellId);
        if(existedItems.length > 0) {
            continue;
        }
        let isCodeCell: boolean = isCodeCellModel(cells.get(index));
        let isRawCell: boolean = isRawCellModel(cells.get(index));
        if ((! isCodeCell) && (! isRawCell)) {
            continue;
        }
        let transformerTag: string = TagsUtils.getCellTransformerTag(notebookPanel, index)? TagsUtils.getCellTransformerTag(notebookPanel, index) : null;

        let cellElement: HTMLElement = notebookPanel.content.node.childNodes[index] as HTMLElement;
        editors[index] = {
            cellId: cellId,
            notebookPanel: notebookPanel,
            transformerTag: transformerTag,
            cellElement: cellElement
        };
        createCellTransformerWidgets(cellId, notebookPanel, cellElement, transformerTag, isTransformerEnabled);
    }
}

const createCellTransformerWidgets = (cellId: string, notebookPanel: NotebookPanel, cellElement: HTMLElement, transformerTag: string, isTransformerEnabled: boolean) => {
    const newChildNode = document.createElement('div')
    newChildNode.className = "cell-transformer-widget";
    let oldWidgets = cellElement.getElementsByClassName("cell-transformer-widget");
    for (let index = 0; index < oldWidgets.length; index++) {
        oldWidgets[index].remove();
    }
    cellElement.insertAdjacentElement('afterbegin', newChildNode);
    ReactDOM.render(
        <CellMetadataEditor
            cellId={cellId}
            notebookPanel={notebookPanel}
            cellElement={cellElement}
            transformerTag={transformerTag}
            transformerSettings={transformerSettings}
            isTransformerEnabled={isTransformerEnabled}
        />,
        newChildNode
    );
}

export const showCurrentActiveCellTransformerWidget = (notebookPanel: NotebookPanel) => {
    let notebook: Notebook = notebookPanel.content;
    let cellElement: HTMLElement = notebook.node.childNodes[notebook.activeCellIndex] as HTMLElement;
    let transformerMetaChip: HTMLElement = cellElement.querySelector('.cell-transformer-widget .transformer-meta-chip') as HTMLElement;
    if(transformerMetaChip) {
        transformerMetaChip.click();
    }
}

export default {
    id: 'modeldeploy-proxy-labextension:notebook',
    requires: [ISettingRegistry, INotebookTracker, IDocumentManager],
    autoStart: true,
    activate: async (
        app: JupyterFrontEnd,
        settingRegistry: ISettingRegistry,
        notebookTracker: INotebookTracker,
        docManager: IDocumentManager,
    ) => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(([settings]) => {
            transformerSettings = settings;
            isTransformerEnabled = getTransformerEnabled();
        });

        if(notebookTracker) {
            notebookTracker.currentChanged.connect(handleNotebookChanged);
        }

        app.started.then(() => {
        });

        app.restored.then(async () => {
        });
    },
} as JupyterFrontEndPlugin<void>;
