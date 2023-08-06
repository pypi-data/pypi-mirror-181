import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import TransformerCellSidebarPlugin from './sidebar';
import TransformerLeftPanelPlugin from './leftpanel';
import StatesPlugin from './states';
import SettingsPlugin from './settings';
import NotebookPlugin from './notebook';

export default [ TransformerCellSidebarPlugin, TransformerLeftPanelPlugin, SettingsPlugin, NotebookPlugin, StatesPlugin ] as JupyterFrontEndPlugin<any>[];
