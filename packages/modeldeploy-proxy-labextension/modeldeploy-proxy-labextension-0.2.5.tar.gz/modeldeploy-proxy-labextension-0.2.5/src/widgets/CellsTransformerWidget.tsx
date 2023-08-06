import * as React from 'react';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IObservableList, IObservableUndoableList } from '@jupyterlab/observables';
import { Cell, ICellModel, isCodeCellModel, isRawCellModel } from '@jupyterlab/cells';
import { CellMetadataEditor, IProps as EditorProps } from './CellMetadataEditor';
import { Switch } from '@material-ui/core';
import TagsUtils from './../lib/TagsUtils';
import * as ReactDOM from 'react-dom';

interface IProps {
  notebookPanel: NotebookPanel;
  onTransformerEnable: (isEnabled: boolean) => void;
}

interface IState {
  prevBlockName?: string;
  checked?: boolean;
  editors?: EditorProps[];
  isEditorVisible: boolean;
}

const DefaultState: IState = {
  prevBlockName: null,
  checked: true,
  editors: [],
  isEditorVisible: false,
};

type SaveState = 'started' | 'completed' | 'failed';

export class CellsTransformerWidget {
  state = DefaultState;

  constructor(props: IProps) {
    super(props);
    this.onEditorVisibilityChange = this.onEditorVisibilityChange.bind(this);
  }

  componentDidMount = () => {
    if (this.props.notebookPanel) {
      this.connectAndInitWhenReady(this.props.notebookPanel);
    }
  };

  componentDidUpdate = async (prevProps: Readonly<IProps>, prevState: Readonly<IState>) => {
      if (! this.props.notebookPanel && prevProps.notebookPanel) {
          this.clearEditorsPropsAndInlineMetadata();
      }

      const preNotebookId = prevProps.notebookPanel? prevProps.notebookPanel.id : '';
      const notebookId = this.props.notebookPanel? this.props.notebookPanel.id : '';
      if (preNotebookId !== notebookId) {
          // notebook changed
          if (prevProps.notebookPanel) {
              this.disconnectHandlersFromNotebook(prevProps.notebookPanel);
          }
          if (this.props.notebookPanel) {
              this.connectAndInitWhenReady(this.props.notebookPanel);
          }
          // hide editor on notebook change
          this.setState({ isEditorVisible: false });
      }
  };

  connectAndInitWhenReady = (notebookPanel: NotebookPanel) => {
      console.log('connectAndInitWhenReady');
      notebookPanel.context.ready.then(() => {
          this.generateEditorsPropsAndInlineMetadata();
          this.state.editors.forEach((editor, index) => {
              const transformerTag = TagsUtils.getCellTransformerTag(notebookPanel, index)? TagsUtils.getCellTransformerTag(notebookPanel, index) : null;
              this.createCellTransformerWidgets(editor['notebookPanel'], editor['cellElement'], transformerTag);
          });

          this.setState({ isEditorVisible: false });
          this.connectHandlersToNotebook(this.props.notebookPanel);
          //this.refreshEditorsPropsAndInlineMetadata();
      });
  };

  createCellTransformerWidgets = (
      notebookPanel: NotebookPanel,
      cellElement: HTMLElement,
      transformerTag: string
  ) => {
      console.log('createCellTransformerWidgets');
      const newChildNode = document.createElement('div')
      newChildNode.className = "cell-transformer-widget";
      cellElement.insertAdjacentElement('afterbegin', newChildNode);
      ReactDOM.render(
          <CellMetadataEditor
              notebookPanel={notebookPanel}
              cellElement={cellElement}
              transformerTag={transformerTag}
          />,
          newChildNode
      );
  }

  connectHandlersToNotebook = (notebookPanel: NotebookPanel) => {
    notebookPanel.context.saveState.connect(this.handleSaveState);
    notebookPanel.content.activeCellChanged.connect(this.onActiveCellChanged);
    notebookPanel.model.cells.changed.connect(this.handleCellChange);
  };

  disconnectHandlersFromNotebook = (notebookPanel: NotebookPanel) => {
    notebookPanel.context.saveState.disconnect(this.handleSaveState);
    notebookPanel.content.activeCellChanged.disconnect(this.onActiveCellChanged);
    // when closing the notebook tab, notebook.model becomes null
    if (notebookPanel.model) {
      notebookPanel.model.cells.changed.disconnect(this.handleCellChange);
    }
  };

  onActiveCellChanged = (notebook: Notebook, activeCell: Cell) => {
    console.log('onActiveCellChanged ' + notebook.activeCellIndex);
    let cellElement: HTMLElement = notebook.node.childNodes[notebook.activeCellIndex] as HTMLElement;
    let transformerWidget: HTMLElement = cellElement.querySelector('.cell-transformer-widget') as HTMLElement;
    if(! transformerWidget) {
        const transformerTag = TagsUtils.getCellTransformerTag(this.props.notebookPanel, notebook.activeCellIndex);
        this.createCellTransformerWidgets(this.props.notebookPanel, cellElement, transformerTag);
    }
  };

  handleSaveState = (context: DocumentRegistry.Context, state: SaveState) => {
    if (this.state.checked && state === 'completed') {
      this.generateEditorsPropsAndInlineMetadata();
    }
  };

  handleCellChange = (
    cells: IObservableUndoableList<ICellModel>,
    args: IObservableList.IChangedArgs<ICellModel>,
  ) => {
  };

  toggleGlobalTransformerSwitch(checked: boolean) {
    this.setState({ checked });
    this.props.onTransformerEnable(checked);

    if (checked) {
      this.generateEditorsPropsAndInlineMetadata();

      if (this.props.notebookPanel && this.props.notebookPanel.content.activeCellIndex) {
      }
    } else {
      this.setState({ isEditorVisible: false });
      this.clearEditorsPropsAndInlineMetadata();
    }
  }

  refreshEditorsPropsAndInlineMetadata() {
    if (this.state.checked) {
      this.clearEditorsPropsAndInlineMetadata(() => {
        this.generateEditorsPropsAndInlineMetadata();
      });
      this.setState({ isEditorVisible: false });
    }
  }

  clearEditorsPropsAndInlineMetadata = (callback?: () => void) => {
    // triggers cleanup in InlineMetadata
    this.setState({ editors: [] }, () => {
      if (callback) {
        callback();
      }
    });
  };

  generateEditorsPropsAndInlineMetadata = () => {
    if (! this.props.notebookPanel) {
      return;
    }
    const editors: EditorProps[] = [];
    const cells = this.props.notebookPanel.model.cells;
    for (let index = 0; index < cells.length; index++) {
        let isCodeCell: boolean = isCodeCellModel(this.props.notebookPanel.model.cells.get(index));
        let isRawCell: boolean = isRawCellModel(this.props.notebookPanel.model.cells.get(index));
        if ((! isCodeCell) && (! isRawCell)) {
            continue;
        }
        editors[index] = {
            notebookPanel: this.props.notebookPanel,
            transformerTag: '',
            cellElement: this.props.notebookPanel.content.node.childNodes[index],
        };
    }

    this.setState({
      editors: editors,
    });
  };

  /**
   * Callback passed to the CellMetadataEditor context
   */
  onEditorVisibilityChange(isEditorVisible: boolean) {
    this.setState({ isEditorVisible });
  }

  render() {
    // Get the editor props of the active cell, so that just one editor is
    // rendered at any given time.
    //const editorProps: EditorProps = {
    //  ...this.state.editors[this.state.activeCellIndex],
    //};
    return (
      <React.Fragment>
        <div className="toolbar input-container">
          <div className={'switch-label'}>Enable</div>
          <Switch
            checked={this.state.checked}
            onChange={c => this.toggleGlobalTransformerSwitch(c.target.checked)}
            color="primary"
            name="enable-transformer"
            inputProps={{ 'aria-label': 'primary checkbox' }}
            classes={{ root: 'material-switch' }}
          />
        </div>
      </React.Fragment>
    );
  }
}
