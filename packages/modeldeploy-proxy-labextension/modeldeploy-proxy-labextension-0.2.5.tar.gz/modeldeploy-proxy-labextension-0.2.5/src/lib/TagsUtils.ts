import { NotebookPanel } from '@jupyterlab/notebook';
import CellUtils from './CellUtils';
import { RESERVED_CELL_NAMES } from './../widgets/CellMetadataEditor';
import { Cell } from '@jupyterlab/cells';

interface ITransformerCellTag {
  transformerTag: string;
}

export default class TagsUtils {

    public static getCellTransformerTag(
        notebookPanel: NotebookPanel,
        index: number,
    ): string {
        const tag: string = CellUtils.getCellMetaData(notebookPanel.content, index, 'transformer') || null;
        if (RESERVED_CELL_NAMES.includes(tag)) {
            return tag;
        }
        return null;
    }

    public static isTransformerTagExistedInOtherCells(
        notebookPanel: NotebookPanel,
        index: number,
        tag: string,
    ): boolean {
        if (! tag) {
            return false;
        }
        for (let i = 0; i < notebookPanel.model.cells.length; i++) {
            if(index == i) {
                continue;
            }
            const cellTag: string = CellUtils.getCellMetaData(notebookPanel.content, i, 'transformer') || null;
            if (tag === cellTag) {
                console.log("Duplicate with " + index + " and " + i);
                return true;
            }
        }
        return false;
    }

  public static setCellTransformerTag(
      notebookPanel: NotebookPanel,
      index: number,
      metadata: ITransformerCellTag,
      save: boolean = true
  ): Promise<any> {
    return CellUtils.setCellMetaData(notebookPanel, index, 'transformer', metadata.transformerTag, true);
  }

  public static resetCellTransformerTag(
      notebookPanel: NotebookPanel,
      index: number,
  ) {
    let cellMetadata = {
      transformerTag: '',
    };
    return TagsUtils.setCellTransformerTag(notebookPanel, index, cellMetadata);
  }

  public static updateCellsTransformerTag(
    notebookPanel: NotebookPanel,
    transformerTag: string,
  ) {
    let i: number;
    const allPromises = [];
    for (i = 0; i < notebookPanel.model.cells.length; i++) {
      allPromises.push(
        CellUtils.setCellMetaData(notebookPanel, i, 'transformer', transformerTag, false),
      );
    }
    Promise.all(allPromises).then(() => {
      notebookPanel.context.save();
    });
  }

  public static cellsToArray(notebookPanel: NotebookPanel) {
    const cells = notebookPanel.model.cells;
    const cellsArray = [];
    for (let index = 0; index < cells.length; index += 1) {
      const cell = cells.get(index);
      cellsArray.push(cell);
    }
    return cellsArray;
  }

  public static getCellByTransformerTag(
    notebookPanel: NotebookPanel,
    transformerTag: string,
  ): { cell: Cell; index: number } {
    for (let i = 0; i < notebookPanel.model.cells.length; i++) {
      const name = this.getCellTransformerTag(notebookPanel, i);
      if (name === transformerTag) {
        return { cell: notebookPanel.content.widgets[i], index: i };
      }
    }
  }
}
