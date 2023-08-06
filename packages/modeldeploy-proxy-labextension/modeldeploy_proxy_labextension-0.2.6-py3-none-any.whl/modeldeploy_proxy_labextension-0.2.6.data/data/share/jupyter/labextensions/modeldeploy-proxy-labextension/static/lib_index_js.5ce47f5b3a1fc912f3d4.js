(self["webpackChunkmodeldeploy_proxy_labextension"] = self["webpackChunkmodeldeploy_proxy_labextension"] || []).push([["lib_index_js"],{

/***/ "./lib/components/LightTooltip.js":
/*!****************************************!*\
  !*** ./lib/components/LightTooltip.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LightTooltip": () => (/* binding */ LightTooltip)
/* harmony export */ });
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/withStyles.js");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @material-ui/core */ "webpack/sharing/consume/default/@material-ui/core/@material-ui/core");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__);


const LightTooltip = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__["default"])((theme) => ({
    tooltip: {
        backgroundColor: theme.palette.common.white,
        color: 'rgba(0, 0, 0, 0.87)',
        boxShadow: theme.shadows[1],
        fontSize: 'var(--jp-ui-font-size1)',
    },
}))(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.Tooltip);


/***/ }),

/***/ "./lib/components/Select.js":
/*!**********************************!*\
  !*** ./lib/components/Select.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Select": () => (/* binding */ Select)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_TextField__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core/TextField */ "./node_modules/@material-ui/core/esm/TextField/TextField.js");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core */ "webpack/sharing/consume/default/@material-ui/core/@material-ui/core");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/makeStyles.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/createStyles.js");
/* harmony import */ var _LightTooltip__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./LightTooltip */ "./lib/components/LightTooltip.js");
var __rest = (undefined && undefined.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};





const useStyles = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_2__["default"])(() => (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_3__["default"])({
    label: {
        color: 'var(--jp-input-border-color)',
        fontSize: 'var(--jp-ui-font-size2)',
    },
    input: {
        color: 'var(--jp-ui-font-color1)',
    },
    textField: {
        width: '100%',
    },
    menu: {
        backgroundColor: 'var(--jp-layout-color1)',
        color: 'var(--jp-ui-font-color1)',
    },
    helperLabel: {
        color: 'var(--jp-info-color0)',
    },
}));
const Select = props => {
    const classes = useStyles({});
    const { index, value, values, helperText = null, variant = 'outlined', updateValue } = props, rest = __rest(props, ["index", "value", "values", "helperText", "variant", "updateValue"]);
    const disableMenuItem = (event, invalidOption) => {
        if (invalidOption) {
            event.stopPropagation();
        }
    };
    const getOptionClassNames = (option) => {
        const classNames = [];
        if (option.tooltip) {
            classNames.push('menu-item-tooltip');
        }
        return classNames.join(' ');
    };
    return (
    // @ts-ignore
    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core_TextField__WEBPACK_IMPORTED_MODULE_4__["default"], Object.assign({ select: true }, rest, { margin: "dense", value: value, variant: variant, className: classes.textField, onChange: evt => updateValue(evt.target.value, index), InputLabelProps: {
            classes: { root: classes.label },
            shrink: value !== '',
        }, InputProps: { classes: { root: classes.input } }, SelectProps: { MenuProps: { PaperProps: { className: classes.menu } } }, FormHelperTextProps: { classes: { root: classes.helperLabel } } }), values.map((option) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.MenuItem, { key: option.value, value: option.value, disabled: !!option.invalid, className: getOptionClassNames(option) }, option.tooltip ? (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_LightTooltip__WEBPACK_IMPORTED_MODULE_5__.LightTooltip, { title: option.tooltip, placement: "top-start", interactive: !(typeof option.tooltip === 'string'), TransitionComponent: _material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Zoom },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "menu-item-label", onClick: ev => disableMenuItem(ev, !!option.invalid) }, option.label))) : (option.label))))));
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _sidebar__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./sidebar */ "./lib/sidebar.js");
/* harmony import */ var _leftpanel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./leftpanel */ "./lib/leftpanel.js");
/* harmony import */ var _states__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./states */ "./lib/states.js");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./settings */ "./lib/settings.js");
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./notebook */ "./lib/notebook.js");





/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([_sidebar__WEBPACK_IMPORTED_MODULE_0__["default"], _leftpanel__WEBPACK_IMPORTED_MODULE_1__["default"], _settings__WEBPACK_IMPORTED_MODULE_2__["default"], _notebook__WEBPACK_IMPORTED_MODULE_3__["default"], _states__WEBPACK_IMPORTED_MODULE_4__["default"]]);


/***/ }),

/***/ "./lib/leftpanel.js":
/*!**************************!*\
  !*** ./lib/leftpanel.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _widgets_TransformerLeftPanel__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widgets/TransformerLeftPanel */ "./lib/widgets/TransformerLeftPanel.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./settings */ "./lib/settings.js");








let transformerSettings;
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
    id: 'modeldeploy-proxy-labextension:leftpanel',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    autoStart: true,
    activate: async (app, labShell, settingRegistry, restorer, toolbarRegistry, translator) => {
        Promise.all([settingRegistry.load(_settings__WEBPACK_IMPORTED_MODULE_6__.SETTINGS_ID)]).then(([settings]) => {
            transformerSettings = settings;
        });
        let widget;
        async function loadPanel() {
            if (!widget.isAttached) {
                labShell.add(widget, 'left');
            }
        }
        app.started.then(() => {
            widget = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_3__.createElement(_widgets_TransformerLeftPanel__WEBPACK_IMPORTED_MODULE_7__.TransformerLeftPanel, { transformerSettings: transformerSettings }));
            widget.id = 'modeldeploy-proxy-labextension/transformer-leftpanel-widget';
            widget.title.iconClass = 'transformer-logo jp-sidebar-tabicon-transformer';
            widget.title.caption = 'Transformer Panel';
            widget.node.classList.add('transformer-panel');
            restorer.add(widget, widget.id);
        });
        app.restored.then(() => {
            loadPanel();
        });
    },
});


/***/ }),

/***/ "./lib/lib/CellUtils.js":
/*!******************************!*\
  !*** ./lib/lib/CellUtils.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CellUtilities)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/nbformat */ "webpack/sharing/consume/default/@jupyterlab/nbformat");
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _NotebookUtils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./NotebookUtils */ "./lib/lib/NotebookUtils.js");




class CellUtilities {
    /**
     * @description Reads the output at a cell within the specified notebook and returns it as a string
     * @param notebook The notebook to get the cell from
     * @param index The index of the cell to read
     * @returns any - A string value of the cell output from the specified
     * notebook and cell index, or null if there is no output.
     * @throws An error message if there are issues in getting the output
     */
    static readOutput(notebook, index) {
        if (!notebook) {
            throw new Error('Notebook was null!');
        }
        if (index < 0 || index >= notebook.model.cells.length) {
            throw new Error('Cell index out of range.');
        }
        const cell = notebook.model.cells.get(index);
        if (!(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.isCodeCellModel)(cell)) {
            throw new Error('cell is not a code cell.');
        }
        if (cell.outputs.length < 1) {
            return null;
        }
        const out = cell.outputs.toJSON().pop();
        if ((0,_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__.isExecuteResult)(out)) {
            return out.data['text/plain'];
        }
        if ((0,_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__.isStream)(out)) {
            return out.text;
        }
        if ((0,_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__.isError)(out)) {
            const errData = out;
            throw new Error(`Code resulted in errors. Error name: ${errData.ename}.\nMessage: ${errData.evalue}.`);
        }
    }
    /**
     * @description Gets the value of a key from the specified cell's metadata.
     * @param notebook The notebook that contains the cell.
     * @param index The index of the cell.
     * @param key The key of the value.
     * @returns any - The value of the metadata. Returns null if the key doesn't exist.
     */
    static getCellMetaData(notebook, index, key) {
        if (!notebook) {
            throw new Error('Notebook was null!');
        }
        if (index < 0 || index >= notebook.model.cells.length) {
            throw new Error('Cell index out of range.');
        }
        const cell = notebook.model.cells.get(index);
        if (cell.metadata.has(key)) {
            return cell.metadata.get(key);
        }
        return null;
    }
    /**
     * @description Sets the key value pair in the notebook's metadata.
     * If the key doesn't exists it will add one.
     * @param notebookPanel The notebook to set meta data in.
     * @param index: The cell index to read metadata from
     * @param key The key of the value to create.
     * @param value The value to set.
     * @param save Default is false. Whether the notebook should be saved after the meta data is set.
     * Note: This function will not wait for the save to complete, it only sends a save request.
     * @returns any - The new value for the key.
     */
    static setCellMetaData(notebookPanel, index, key, value, save = false) {
        if (!notebookPanel) {
            throw new Error('Notebook was null!');
        }
        if (index < 0 || index >= notebookPanel.model.cells.length) {
            throw new Error('Cell index out of range.');
        }
        try {
            const cell = notebookPanel.model.cells.get(index);
            const newValue = value;
            cell.metadata.set(key, value);
            if (save) {
                return notebookPanel.context.save();
            }
            return Promise.resolve(newValue);
        }
        catch (error) {
            return Promise.reject(error);
        }
    }
    /**
     * @description Looks within the notebook for a cell containing the specified meta key
     * @param notebook The notebook to search in
     * @param key The metakey to search for
     * @returns [number, ICellModel] - A pair of values, the first is the index of where the cell was found
     * and the second is a reference to the cell itself. Returns [-1, null] if cell not found.
     */
    static findCellWithMetaKey(notebookPanel, key) {
        if (!notebookPanel) {
            throw new Error('Notebook was null!');
        }
        const cells = notebookPanel.model.cells;
        let cell;
        for (let idx = 0; idx < cells.length; idx += 1) {
            cell = cells.get(idx);
            if (cell.metadata.has(key)) {
                return [idx, cell];
            }
        }
        return [-1, null];
    }
    /**
     * @description Gets the cell object at specified index in the notebook.
     * @param notebook The notebook to get the cell from
     * @param index The index for the cell
     * @returns Cell - The cell at specified index, or null if not found
     */
    static getCell(notebook, index) {
        if (notebook && index >= 0 && index < notebook.model.cells.length) {
            return notebook.model.cells.get(index);
        }
        return null;
    }
    /**
     * @description Runs code in the notebook cell found at the given index.
     * @param command The command registry which can execute the run command.
     * @param notebook The notebook panel to run the cell in
     * @returns Promise<string> - A promise containing the output after the code has executed.
     */
    static async runCellAtIndex(notebookPanel, index) {
        if (notebookPanel === null) {
            throw new Error('Null or undefined parameter was given for command or notebook argument.');
        }
        const notebook = notebookPanel.content;
        if (index < 0 || index >= notebook.widgets.length) {
            throw new Error('The index was out of range.');
        }
        // Save the old index, then set the current active cell
        const oldIndex = notebook.activeCellIndex;
        notebook.activeCellIndex = index;
        try {
            await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.run(notebook, notebookPanel.sessionContext);
            // await command.execute("notebook:run-cell");
            const output = CellUtilities.readOutput(notebook, index);
            notebook.activeCellIndex = oldIndex;
            return output;
        }
        finally {
            notebook.activeCellIndex = oldIndex;
        }
    }
    /**
     * @description Deletes the cell at specified index in the open notebook
     * @param notebookPanel The notebook panel to delete the cell from
     * @param index The index that the cell will be deleted at
     * @returns void
     */
    static deleteCellAtIndex(notebook, index) {
        if (notebook === null) {
            throw new Error('Null or undefined parameter was given for notebook argument.');
        }
        if (index < 0 || index >= notebook.widgets.length) {
            throw new Error('The index was out of range.');
        }
        // Save the old index, then set the current active cell
        let oldIndex = notebook.activeCellIndex;
        notebook.model.cells.remove(index);
        // Adjust old index to account for deleted cell.
        if (oldIndex === index) {
            if (oldIndex > 0) {
                oldIndex -= 1;
            }
            else {
                oldIndex = 0;
            }
        }
        else if (oldIndex > index) {
            oldIndex -= 1;
        }
        notebook.activeCellIndex = oldIndex;
    }
    /**
     * @description Inserts a cell into the notebook, the new cell will be at the specified index.
     * @param notebook The notebook panel to insert the cell in
     * @param index The index of where the new cell will be inserted.
     * If the cell index is less than or equal to 0, it will be added at the top.
     * If the cell index is greater than the last index, it will be added at the bottom.
     * @returns number - The index it where the cell was inserted
     */
    static insertCellAtIndex(notebook, index) {
        // Create a new cell
        const cell = notebook.model.contentFactory.createCodeCell({});
        // Save the old index, then set the current active cell
        let oldIndex = notebook.activeCellIndex;
        // Adjust old index for cells inserted above active cell.
        if (oldIndex >= index) {
            oldIndex += 1;
        }
        if (index <= 0) {
            notebook.model.cells.insert(0, cell);
            notebook.activeCellIndex = oldIndex;
            return 0;
        }
        if (index >= notebook.widgets.length) {
            notebook.model.cells.insert(notebook.widgets.length - 1, cell);
            notebook.activeCellIndex = oldIndex;
            return notebook.widgets.length - 1;
        }
        notebook.model.cells.insert(index, cell);
        notebook.activeCellIndex = oldIndex;
        return index;
    }
    /**
     * @description Injects code into the specified cell of a notebook, does not run the code.
     * Warning: the existing cell's code/text will be overwritten.
     * @param notebook The notebook to select the cell from
     * @param index The index of the cell to inject the code into
     * @param code A string containing the code to inject into the CodeCell.
     * @param checkCodeCell To check if the cell is a CodeCellModel
     * @throws An error message if there are issues with injecting code at a particular cell
     * @returns void
     */
    static injectCodeAtIndex(notebook, index, code, checkCodeCell = false) {
        if (notebook === null) {
            throw new Error('Notebook was null or undefined.');
        }
        if (index < 0 || index >= notebook.model.cells.length) {
            throw new Error('Cell index out of range.');
        }
        const cell = notebook.model.cells.get(index);
        if (checkCodeCell && !(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.isCodeCellModel)(cell)) {
            throw new Error('Cell is not a code cell.');
        }
        cell.value.text = code;
        return;
    }
    /**
     * @description This will insert a new cell at the specified index and the inject the specified code into it.
     * @param notebook The notebook to insert the cell into
     * @param index The index of where the new cell will be inserted.
     * If the cell index is less than or equal to 0, it will be added at the top.
     * If the cell index is greater than the last index, it will be added at the bottom.
     * @param code The code to inject into the cell after it has been inserted
     * @returns number - index of where the cell was inserted
     */
    static insertInjectCode(notebook, index, code) {
        const newIndex = CellUtilities.insertCellAtIndex(notebook, index);
        CellUtilities.injectCodeAtIndex(notebook, newIndex, code);
        return newIndex;
    }
    /**
     * @description This will insert a new cell at the specified index, inject the specified code into it and the run the code.
     * Note: The code will be run but the results (output or errors) will not be displayed in the cell. Best for void functions.
     * @param notebookPanel The notebook to insert the cell into
     * @param index The index of where the new cell will be inserted and run.
     * If the cell index is less than or equal to 0, it will be added at the top.
     * If the cell index is greater than the last index, it will be added at the bottom.
     * @param code The code to inject into the cell after it has been inserted
     * @param deleteOnError If set to true, the cell will be deleted if the code results in an error
     * @returns Promise<[number, string]> - A promise for when the cell code has executed
     * containing the cell's index and output result
     */
    static async insertAndRun(notebookPanel, index, code, deleteOnError) {
        let insertionIndex;
        try {
            insertionIndex = CellUtilities.insertInjectCode(notebookPanel.content, index, code);
            const output = await _NotebookUtils__WEBPACK_IMPORTED_MODULE_3__["default"].sendKernelRequestFromNotebook(notebookPanel, code, { output: 'output' }, false);
            return [insertionIndex, output];
        }
        catch (error) {
            if (deleteOnError) {
                CellUtilities.deleteCellAtIndex(notebookPanel.content, insertionIndex);
            }
            throw error;
        }
    }
    /**
     * @description This will insert a new cell at the specified index, inject the specified code into it and the run the code.
     * Note: The code will be run and the result (output or errors) WILL BE DISPLAYED in the cell.
     * @param notebookPanel The notebook to insert the cell into
     * @param command The command registry which can execute the run command.
     * @param index The index of where the new cell will be inserted and run.
     * If the cell index is less than or equal to 0, it will be added at the top.
     * If the cell index is greater than the last index, it will be added at the bottom.
     * @param code The code to inject into the cell after it has been inserted
     * @param deleteOnError If set to true, the cell will be deleted if the code results in an error
     * @returns Promise<[number, string]> - A promise for when the cell code has executed
     * containing the cell's index and output result
     */
    static async insertRunShow(notebookPanel, index, code, deleteOnError) {
        let insertionIndex;
        try {
            insertionIndex = CellUtilities.insertInjectCode(notebookPanel.content, index, code);
            const output = await CellUtilities.runCellAtIndex(notebookPanel, insertionIndex);
            return [insertionIndex, output];
        }
        catch (error) {
            if (deleteOnError) {
                CellUtilities.deleteCellAtIndex(notebookPanel.content, insertionIndex);
            }
            throw error;
        }
    }
    /**
     * @deprecated Using NotebookUtilities.sendSimpleKernelRequest or NotebookUtilities.sendKernelRequest
     * will execute code directly in the kernel without the need to create a cell and delete it.
     * @description This will insert a cell with specified code at the top and run the code.
     * Once the code is run and output received, the cell is deleted, giving back cell's output.
     * If the code results in an error, the injected cell is still deleted but the promise will be rejected.
     * @param notebookPanel The notebook to run the code in
     * @param code The code to run in the cell
     * @param insertAtEnd True means the cell will be inserted at the bottom
     * @returns Promise<string> - A promise when the cell has been deleted, containing the execution result as a string
     */
    static async runAndDelete(notebookPanel, code, insertAtEnd = true) {
        let idx = -1;
        if (insertAtEnd) {
            idx = notebookPanel.content.model.cells.length;
        }
        const [index, result] = await CellUtilities.insertAndRun(notebookPanel, idx, code, true);
        CellUtilities.deleteCellAtIndex(notebookPanel.content, index);
        return result;
    }
    static isCellVoid(notebook, index) {
        if (notebook === null) {
            throw new Error('Notebook was null or undefined.');
        }
        if (index < 0 || index >= notebook.model.cells.length) {
            throw new Error('Cell index out of range.');
        }
        const cell = notebook.model.cells.get(index);
        if (cell.value.text) {
            if (cell.value.text.trim().length === 0) {
                return true;
            }
            return false;
        }
        return true;
    }
    static isTextInCell(notebook, index, regex) {
        if (notebook === null) {
            throw new Error('Notebook was null or undefined.');
        }
        if (index < 0 || index >= notebook.model.cells.length) {
            throw new Error('Cell index out of range.');
        }
        const cell = notebook.model.cells.get(index);
        if (cell.value.text) {
            let ind = cell.value.text.search(regex);
            if (ind >= 0) {
                return true;
            }
        }
        return false;
    }
}


/***/ }),

/***/ "./lib/lib/NotebookUtils.js":
/*!**********************************!*\
  !*** ./lib/lib/NotebookUtils.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ NotebookUtilities)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _TagsUtils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./TagsUtils */ "./lib/lib/TagsUtils.js");


// @ts-ignore


//import { RESERVED_CELL_NAMES } from '../widgets/cell-metadata/CellMetadataEditor';

/** Contains utility functions for manipulating/handling notebooks in the application. */
class NotebookUtilities {
    /**
     * Clear the outputs of all the notebook' cells
     * @param notebook NotebookPanel
     */
    static clearCellOutputs(notebook) {
        for (let i = 0; i < notebook.model.cells.length; i++) {
            if (!(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.isCodeCellModel)(notebook.model.cells.get(i))) {
                continue;
            }
            notebook.model.cells.get(i).executionCount = null;
            notebook.model.cells.get(i).outputs.clear();
        }
    }
    /**
     * Scroll the notebook to the specified cell, making it active
     * @param notebook NotebookPanel
     * @param cell The cell to be activated
     */
    static selectAndScrollToCell(notebook, cell) {
        notebook.content.select(cell.cell);
        notebook.content.activeCellIndex = cell.index;
        const cellPosition = notebook.content.node.childNodes[cell.index].getBoundingClientRect();
        notebook.content.scrollToPosition(cellPosition.top);
    }
    /**
     * Builds an HTML container by sanitizing a list of strings and converting
     * them in valid HTML
     * @param msg A list of string with HTML formatting
     * @returns a HTMLDivElement composed of a list of spans with formatted text
     */
    static buildDialogBody(msg) {
        return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "dialog-body" }, msg.map((str, i) => {
            return (react__WEBPACK_IMPORTED_MODULE_2__.createElement(react__WEBPACK_IMPORTED_MODULE_2__.Fragment, { key: `msg-${i}` },
                react__WEBPACK_IMPORTED_MODULE_2__.createElement("p", null, str)));
        })));
    }
    /**
     * Opens a pop-up dialog in JupyterLab to display a simple message.
     * @param title The title for the message popup
     * @param msg The message as an array of strings
     * @param buttonLabel The label to use for the button. Default is 'OK'
     * @param buttonClassName The classname to give to the 'ok' button
     * @returns Promise<void> - A promise once the message is closed.
     */
    static async showMessage(title, msg, buttonLabel = 'Close', buttonClassName = '') {
        const buttons = [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: buttonLabel, className: buttonClassName }),
        ];
        const messageBody = this.buildDialogBody(msg);
        await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({ title, buttons, body: messageBody });
    }
    /**
     * Opens a pop-up dialog in JupyterLab to display a yes/no dialog.
     * @param title The title for the message popup
     * @param msg The message
     * @param acceptLabel The label to use for the accept button. Default is 'YES'
     * @param rejectLabel The label to use for the reject button. Default is 'NO'
     * @param yesButtonClassName The classname to give to the accept button.
     * @param noButtonClassName The  classname to give to the cancel button.
     * @returns Promise<void> - A promise once the message is closed.
     */
    static async showYesNoDialog(title, msg, acceptLabel = 'YES', rejectLabel = 'NO', yesButtonClassName = '', noButtonClassName = '') {
        const buttons = [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: acceptLabel, className: yesButtonClassName }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: rejectLabel, className: noButtonClassName }),
        ];
        const messageBody = this.buildDialogBody(msg);
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({ title, buttons, body: messageBody });
        return result.button.label === acceptLabel;
    }
    /**
     * Opens a pop-up dialog in JupyterLab with various information and button
     * triggering reloading the page.
     * @param title The title for the message popup
     * @param msg The message
     * @param refreshButtonLabel The label to use for the refresh button. Default is 'Refresh'
     * @param refreshButtonClassName The  classname to give to the refresh button
     * @param dismissButtonLabel The label to use for the dismiss button. Default is 'Dismiss'
     * @param dismissButtonClassName The classname to give to the dismiss button
     * @returns Promise<void> - A promise once the message is closed.
     */
    static async showRefreshDialog(title, msg, refreshButtonLabel = 'Refresh', dismissButtonLabel = 'Dismiss', refreshButtonClassName = '', dismissButtonClassName = '') {
        (await this.showYesNoDialog(title, msg, refreshButtonLabel, dismissButtonLabel, refreshButtonClassName, dismissButtonClassName)) && location.reload();
    }
    /**
     * @description Creates a new JupyterLab notebook for use by the application
     * @param command The command registry
     * @returns Promise<NotebookPanel> - A promise containing the notebook panel object that was created (if successful).
     */
    static async createNewNotebook(command) {
        const notebook = await command.execute('notebook:create-new', {
            activate: true,
            path: '',
            preferredLanguage: '',
        });
        await notebook.sessionContext.ready;
        return notebook;
    }
    /**
     * Safely saves the Jupyter notebook document contents to disk
     * @param notebookPanel The notebook panel containing the notebook to save
     * @param withPrompt Ask the user before saving the notebook
     * @param waitSave Await the save notebook operation
     */
    static async saveNotebook(notebookPanel, withPrompt = false, waitSave = false) {
        if (notebookPanel && notebookPanel.model.dirty) {
            await notebookPanel.context.ready;
            if (withPrompt &&
                !(await this.showYesNoDialog('Unsaved changes', [
                    'Do you want to save the notebook?',
                ]))) {
                return false;
            }
            waitSave
                ? await notebookPanel.context.save()
                : notebookPanel.context.save();
            return true;
        }
        return false;
    }
    /**
     * Convert the notebook contents to JSON
     * @param notebookPanel The notebook panel containing the notebook to serialize
     */
    static notebookToJSON(notebookPanel) {
        if (notebookPanel) {
            return notebookPanel.content.model.toJSON();
        }
        return null;
    }
    /**
     * @description Gets the value of a key from specified notebook's metadata.
     * @param notebookPanel The notebook to get meta data from.
     * @param key The key of the value.
     * @returns any -The value of the metadata. Returns null if the key doesn't exist.
     */
    static getMetaData(notebookPanel, key) {
        if (!notebookPanel) {
            throw new Error('The notebook is null or undefined. No meta data available.');
        }
        if (notebookPanel.model && notebookPanel.model.metadata.has(key)) {
            return notebookPanel.model.metadata.get(key);
        }
        return null;
    }
    /**
     * @description Sets the key value pair in the notebook's metadata.
     * If the key doesn't exists it will add one.
     * @param notebookPanel The notebook to set meta data in.
     * @param key The key of the value to create.
     * @param value The value to set.
     * @param save Default is false. Whether the notebook should be saved after the meta data is set.
     * Note: This function will not wait for the save to complete, it only sends a save request.
     * @returns The new value for the key.
     */
    static setMetaData(notebookPanel, key, value, save = false) {
        if (!notebookPanel) {
            throw new Error('The notebook is null or undefined. No meta data available.');
        }
        notebookPanel.model.metadata.set(key, value);
        if (save) {
            this.saveNotebook(notebookPanel);
        }
        return value;
    }
    static async runGlobalCells(notebook) {
        let cell = { cell: notebook.content.widgets[0], index: 0 };
        const reservedCellsToBeIgnored = ['skip', 'pipeline-metrics'];
        for (let i = 0; i < notebook.model.cells.length; i++) {
            if (!(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.isCodeCellModel)(notebook.model.cells.get(i))) {
                continue;
            }
            const blockName = _TagsUtils__WEBPACK_IMPORTED_MODULE_4__["default"].getCellTransformerTag(notebook, i);
            // If a cell of that type is found, run that
            // and all consequent cells getting merged to that one
            if (!reservedCellsToBeIgnored.includes(blockName)
            /* && RESERVED_CELL_NAMES.includes(blockName) */
            ) {
                while (i < notebook.model.cells.length) {
                    if (!(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.isCodeCellModel)(notebook.model.cells.get(i))) {
                        i++;
                        continue;
                    }
                    const cellName = _TagsUtils__WEBPACK_IMPORTED_MODULE_4__["default"].getCellTransformerTag(notebook, i);
                    if (cellName !== blockName && cellName !== '') {
                        // Decrement by 1 to parse that cell during the next for loop
                        i--;
                        break;
                    }
                    cell = { cell: notebook.content.widgets[i], index: i };
                    this.selectAndScrollToCell(notebook, cell);
                    // this.setState({ activeCellIndex: cell.index, activeCell: cell.cell });
                    const kernelMsg = (await _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCell.execute(notebook.content.widgets[i], notebook.sessionContext));
                    if (kernelMsg.content && kernelMsg.content.status === 'error') {
                        return {
                            status: 'error',
                            cellType: blockName,
                            cellIndex: i,
                            ename: kernelMsg.content.ename,
                            evalue: kernelMsg.content.evalue,
                        };
                    }
                    i++;
                }
            }
        }
        return { status: 'ok' };
    }
    /**
     * Get a new Kernel, not tied to a Notebook
     * Source code here: https://github.com/jupyterlab/jupyterlab/tree/473348d25bcb258ca2f0c127dd8fb5b193217135/packages/services
     */
    static async createNewKernel() {
        const defaultKernelSpec = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.KernelSpecAPI.getSpecs().then((res) => res.default);
        return await new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.KernelManager().startNew({ name: defaultKernelSpec });
    }
    static async executeWithNewKernel(action, args = []) {
        // create brand new kernel
        const _k = await this.createNewKernel();
        // execute action inside kernel
        const res = await action(_k, ...args);
        // close kernel
        _k.shutdown();
        // return result
        return res;
    }
    /**
     * @description This function runs code directly in the notebook's kernel and then evaluates the
     * result and returns it as a promise.
     * @param kernel The kernel to run the code in.
     * @param runCode The code to run in the kernel.
     * @param userExpressions The expressions used to capture the desired info from the executed code.
     * @param runSilent Default is false. If true, kernel will execute as quietly as possible.
     * store_history will be set to false, and no broadcast on IOPUB channel will be made.
     * @param storeHistory Default is false. If true, the code executed will be stored in the kernel's history
     * and the counter which is shown in the cells will be incremented to reflect code was run.
     * @param allowStdIn Default is false. If true, code running in kernel can prompt user for input using
     * an input_request message.
     * @param stopOnError Default is false. If True, does not abort the execution queue, if an exception is encountered.
     * This allows the queued execution of multiple execute_requests, even if they generate exceptions.
     * @returns Promise<any> - A promise containing the execution results of the code as an object with
     * keys based on the user_expressions.
     * @example
     * //The code
     * const code = "a=123\nb=456\nsum=a+b";
     * //The user expressions
     * const expr = {sum: "sum",prod: "a*b",args:"[a,b,sum]"};
     * //Async function call (returns a promise)
     * sendKernelRequest(notebookPanel, code, expr,false);
     * //Result when promise resolves:
     * {
     *  sum:{status:"ok",data:{"text/plain":"579"},metadata:{}},
     *  prod:{status:"ok",data:{"text/plain":"56088"},metadata:{}},
     *  args:{status:"ok",data:{"text/plain":"[123, 456, 579]"}}
     * }
     * @see For more information on JupyterLab messages:
     * https://jupyter-client.readthedocs.io/en/latest/messaging.html#execution-results
     */
    static async sendKernelRequest(kernel, runCode, userExpressions, runSilent = false, storeHistory = false, allowStdIn = false, stopOnError = false) {
        if (!kernel) {
            throw new Error('Kernel is null or undefined.');
        }
        const message = await kernel.requestExecute({
            allow_stdin: allowStdIn,
            code: runCode,
            silent: runSilent,
            stop_on_error: stopOnError,
            store_history: storeHistory,
            user_expressions: userExpressions,
        }).done;
        const content = message.content;
        if (content.status !== 'ok') {
            // If response is not 'ok', throw contents as error, log code
            const msg = `Code caused an error:\n${runCode}`;
            console.error(msg);
            if (content.traceback) {
                content.traceback.forEach((line) => console.log(line.replace(/[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, '')));
            }
            throw content;
        }
        // Return user_expressions of the content
        return content.user_expressions;
    }
    /**
     * Same as method sendKernelRequest but passing
     * a NotebookPanel instead of a Kernel
     */
    static async sendKernelRequestFromNotebook(notebookPanel, runCode, userExpressions, runSilent = false, storeHistory = false, allowStdIn = false, stopOnError = false) {
        if (!notebookPanel) {
            throw new Error('Notebook is null or undefined.');
        }
        // Wait for notebook panel to be ready
        await notebookPanel.sessionContext.ready;
        return this.sendKernelRequest(notebookPanel.sessionContext.session.kernel, runCode, userExpressions, runSilent, storeHistory, allowStdIn, stopOnError);
    }
}


/***/ }),

/***/ "./lib/lib/RPCUtils.js":
/*!*****************************!*\
  !*** ./lib/lib/RPCUtils.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BaseError": () => (/* binding */ BaseError),
/* harmony export */   "JSONParseError": () => (/* binding */ JSONParseError),
/* harmony export */   "KernelError": () => (/* binding */ KernelError),
/* harmony export */   "RPCError": () => (/* binding */ RPCError),
/* harmony export */   "RPC_CALL_STATUS": () => (/* binding */ RPC_CALL_STATUS),
/* harmony export */   "_legacy_executeRpc": () => (/* binding */ _legacy_executeRpc),
/* harmony export */   "_legacy_executeRpcAndShowRPCError": () => (/* binding */ _legacy_executeRpcAndShowRPCError),
/* harmony export */   "executeRpc": () => (/* binding */ executeRpc),
/* harmony export */   "globalUnhandledRejection": () => (/* binding */ globalUnhandledRejection),
/* harmony export */   "rokErrorTooltip": () => (/* binding */ rokErrorTooltip),
/* harmony export */   "showError": () => (/* binding */ showError),
/* harmony export */   "showRpcError": () => (/* binding */ showRpcError)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _NotebookUtils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./NotebookUtils */ "./lib/lib/NotebookUtils.js");



const globalUnhandledRejection = async (event) => {
    // console.error(event.reason);
    if (event.reason instanceof BaseError) {
        console.error(event.reason.message, event.reason.error);
        event.reason.showDialog().then();
    }
    else {
        showError('An unexpected error has occurred', 'JS', `${event.reason.name}: ${event.reason.message}`, 'Please see the console for more information', true).then();
    }
};
var RPC_CALL_STATUS;
(function (RPC_CALL_STATUS) {
    RPC_CALL_STATUS[RPC_CALL_STATUS["OK"] = 0] = "OK";
    RPC_CALL_STATUS[RPC_CALL_STATUS["ImportError"] = 1] = "ImportError";
    RPC_CALL_STATUS[RPC_CALL_STATUS["EncodingError"] = 2] = "EncodingError";
    RPC_CALL_STATUS[RPC_CALL_STATUS["NotFound"] = 3] = "NotFound";
    RPC_CALL_STATUS[RPC_CALL_STATUS["InternalError"] = 4] = "InternalError";
    RPC_CALL_STATUS[RPC_CALL_STATUS["ServiceUnavailable"] = 5] = "ServiceUnavailable";
    RPC_CALL_STATUS[RPC_CALL_STATUS["UnhandledError"] = 6] = "UnhandledError";
})(RPC_CALL_STATUS || (RPC_CALL_STATUS = {}));
const getRpcCodeName = (code) => {
    switch (code) {
        case RPC_CALL_STATUS.OK:
            return 'OK';
        case RPC_CALL_STATUS.ImportError:
            return 'ImportError';
        case RPC_CALL_STATUS.EncodingError:
            return 'EncodingError';
        case RPC_CALL_STATUS.NotFound:
            return 'NotFound';
        case RPC_CALL_STATUS.InternalError:
            return 'InternalError';
        case RPC_CALL_STATUS.ServiceUnavailable:
            return 'ServiceUnavailable';
        default:
            return 'UnhandledError';
    }
};
const rokErrorTooltip = (rokError) => {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
            "This feature requires Rok.",
            ' ',
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { onClick: _ => showRpcError(rokError) }, "More info..."))));
};
const serialize = (obj) => window.btoa(JSON.stringify(obj));
const deserialize = (raw_data) => window.atob(raw_data.substring(1, raw_data.length - 1));
/**
 * Execute modeldeploy_proxy_controller.rpc module functions
 * Example: func_result = await this.executeRpc(kernel | notebookPanel, "rpc_submodule.func", {arg1, arg2})
 *    where func_result is a JSON object
 * @param func Function name to be executed
 * @param kwargs Dictionary with arguments to be passed to the function
 * @param ctx Dictionary with the RPC context (e.g., nb_path)
 * @param env instance of Kernel or NotebookPanel
 */
const executeRpc = async (env, func, kwargs = {}, ctx = {}) => {
    const cmd = `from modeldeploy_proxy_controller.rpc.run import run as __controller_rpc_run\n` +
        `__controller_rpc_result = __controller_rpc_run("${func}", '${serialize(kwargs)}', '${serialize(ctx)}')`;
    console.log('Executing command: ' + cmd);
    const expressions = { result: '__controller_rpc_result' };
    let output = null;
    try {
        output =
            env instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookPanel
                ? await _NotebookUtils__WEBPACK_IMPORTED_MODULE_2__["default"].sendKernelRequestFromNotebook(env, cmd, expressions)
                : await _NotebookUtils__WEBPACK_IMPORTED_MODULE_2__["default"].sendKernelRequest(env, cmd, expressions);
    }
    catch (e) {
        console.warn(e);
        const error = {
            rpc: `${func}`,
            status: `${e.ename}: ${e.evalue}`,
            output: e.traceback,
        };
        throw new KernelError(error);
    }
    // const argsAsStr = Object.keys(kwargs).map(key => `${key}=${kwargs[key]}`).join(', ');
    let msg = [`RPC: ${func}`];
    // Log output
    if (output.result.status !== 'ok') {
        // `Kernel failed during code execution`
        msg = msg.concat([
            `Status: ${output.result.status}`,
            `Output: ${JSON.stringify(output, null, 3)}`,
        ]);
        const error = {
            rpc: `${func}`,
            status: output.result.status,
            output: output,
        };
        throw new KernelError(error);
    }
    // console.log(msg.concat([output]));
    const raw_data = output.result.data['text/plain'];
    const json_data = deserialize(raw_data);
    // Validate response is a JSON
    // If successful, run() method returns json.dumps() of any result
    let parsedResult = undefined;
    try {
        parsedResult = JSON.parse(json_data);
    }
    catch (error) {
        // `Failed to parse response as JSON`;
        msg = msg.concat([
            `Error: ${JSON.stringify(error, null, 3)}`,
            `Response data: ${json_data}`,
        ]);
        const jsonError = {
            rpc: `${func}`,
            err_message: 'Failed to parse response as JSON',
            error: error,
            jsonData: json_data,
        };
        throw new JSONParseError(jsonError);
    }
    if (parsedResult.code !== 0) {
        // `An error has occured`;
        msg = msg.concat([
            `Code: ${parsedResult.code} (${getRpcCodeName(parsedResult.code)})`,
            `Message: ${parsedResult.err_message}`,
            `Details: ${parsedResult.err_details}`,
        ]);
        let error = {
            rpc: `${func}`,
            code: parsedResult.code,
            err_message: parsedResult.err_message,
            err_details: parsedResult.err_details,
            err_cls: parsedResult.err_cls,
            trans_id: parsedResult.trans_id,
        };
        throw new RPCError(error);
    }
    else {
        // console.log(msg, parsedResult);
        return parsedResult.result;
    }
};
const showError = async (title, type, message, details, refresh = true, method = null, code = null, trans_id = null) => {
    let msg = [
        `Browser: ${navigator ? navigator.userAgent : 'other'}`,
        `Type: ${type}`,
    ];
    if (method) {
        msg.push(`Method: ${method}()`);
    }
    if (code) {
        msg.push(`Code: ${code} (${getRpcCodeName(code)})`);
    }
    if (trans_id) {
        msg.push(`Transaction ID: ${trans_id}`);
    }
    msg.push(`Message: ${message}`, `Details: ${details}`);
    if (refresh) {
        await _NotebookUtils__WEBPACK_IMPORTED_MODULE_2__["default"].showRefreshDialog(title, msg);
    }
    else {
        await _NotebookUtils__WEBPACK_IMPORTED_MODULE_2__["default"].showMessage(title, msg);
    }
};
const showRpcError = async (error, refresh = false) => {
    await showError('An RPC Error has occurred', 'RPC', error.err_message, error.err_details, refresh, error.rpc, error.code, error.trans_id);
};
// todo: refactor these legacy functions
const _legacy_executeRpc = async (notebook, kernel, func, args = {}, nb_path = null) => {
    if (!nb_path && notebook) {
        nb_path = notebook.context.path;
    }
    let retryRpc = true;
    let result = null;
    // Kerned aborts the execution if busy
    // If that is the case, retry the RPC
    while (retryRpc) {
        try {
            result = await executeRpc(kernel, func, args, { nb_path });
            retryRpc = false;
        }
        catch (error) {
            if (error instanceof KernelError && error.error.status === 'aborted') {
                continue;
            }
            // If kernel not busy, throw the error
            throw error;
        }
    }
    return result;
};
// Execute RPC and if an RPCError is caught, show dialog and return null
// This is our default behavior prior to this commit. This may probably
// change in the future, setting custom logic for each RPC call. For
// example, see getBaseImage().
const _legacy_executeRpcAndShowRPCError = async (notebook, kernel, func, args = {}, nb_path = null) => {
    try {
        const result = await _legacy_executeRpc(notebook, kernel, func, args, nb_path);
        return result;
    }
    catch (error) {
        if (error instanceof RPCError) {
            await error.showDialog();
            return null;
        }
        throw error;
    }
};
class BaseError extends Error {
    constructor(message, error) {
        super(message);
        this.error = error;
        this.name = this.constructor.name;
        this.stack = new Error(message).stack;
        Object.setPrototypeOf(this, BaseError.prototype);
    }
}
class KernelError extends BaseError {
    constructor(error) {
        super('Kernel error', error);
        Object.setPrototypeOf(this, KernelError.prototype);
    }
    async showDialog(refresh = true) {
        await showError('A Kernel Error has occurred', 'Kernel', this.error.status, JSON.stringify(this.error.output, null, 3), refresh, this.error.rpc);
    }
}
class JSONParseError extends BaseError {
    constructor(error) {
        super('JSON Parse error', error);
        Object.setPrototypeOf(this, JSONParseError.prototype);
    }
    async showDialog(refresh = false) {
        await showError('Failed to parse RPC response as JSON', 'JSONParse', this.error.error.message, this.error.json_data, refresh, this.error.rpc);
    }
}
class RPCError extends BaseError {
    constructor(error) {
        super('RPC Error', error);
        Object.setPrototypeOf(this, RPCError.prototype);
    }
    async showDialog(refresh = false) {
        await showRpcError(this.error, refresh);
    }
}


/***/ }),

/***/ "./lib/lib/TagsUtils.js":
/*!******************************!*\
  !*** ./lib/lib/TagsUtils.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ TagsUtils)
/* harmony export */ });
/* harmony import */ var _CellUtils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./CellUtils */ "./lib/lib/CellUtils.js");
/* harmony import */ var _widgets_CellMetadataEditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./../widgets/CellMetadataEditor */ "./lib/widgets/CellMetadataEditor.js");


class TagsUtils {
    static getCellTransformerTag(notebookPanel, index) {
        const tag = _CellUtils__WEBPACK_IMPORTED_MODULE_0__["default"].getCellMetaData(notebookPanel.content, index, 'transformer') || null;
        if (_widgets_CellMetadataEditor__WEBPACK_IMPORTED_MODULE_1__.RESERVED_CELL_NAMES.includes(tag)) {
            return tag;
        }
        return null;
    }
    static isTransformerTagExistedInOtherCells(notebookPanel, index, tag) {
        if (!tag) {
            return false;
        }
        for (let i = 0; i < notebookPanel.model.cells.length; i++) {
            if (index == i) {
                continue;
            }
            const cellTag = _CellUtils__WEBPACK_IMPORTED_MODULE_0__["default"].getCellMetaData(notebookPanel.content, i, 'transformer') || null;
            if (tag === cellTag) {
                console.log("Duplicate with " + index + " and " + i);
                return true;
            }
        }
        return false;
    }
    static setCellTransformerTag(notebookPanel, index, metadata, save = true) {
        return _CellUtils__WEBPACK_IMPORTED_MODULE_0__["default"].setCellMetaData(notebookPanel, index, 'transformer', metadata.transformerTag, true);
    }
    static resetCellTransformerTag(notebookPanel, index) {
        let cellMetadata = {
            transformerTag: '',
        };
        return TagsUtils.setCellTransformerTag(notebookPanel, index, cellMetadata);
    }
    static updateCellsTransformerTag(notebookPanel, transformerTag) {
        let i;
        const allPromises = [];
        for (i = 0; i < notebookPanel.model.cells.length; i++) {
            allPromises.push(_CellUtils__WEBPACK_IMPORTED_MODULE_0__["default"].setCellMetaData(notebookPanel, i, 'transformer', transformerTag, false));
        }
        Promise.all(allPromises).then(() => {
            notebookPanel.context.save();
        });
    }
    static cellsToArray(notebookPanel) {
        const cells = notebookPanel.model.cells;
        const cellsArray = [];
        for (let index = 0; index < cells.length; index += 1) {
            const cell = cells.get(index);
            cellsArray.push(cell);
        }
        return cellsArray;
    }
    static getCellByTransformerTag(notebookPanel, transformerTag) {
        for (let i = 0; i < notebookPanel.model.cells.length; i++) {
            const name = this.getCellTransformerTag(notebookPanel, i);
            if (name === transformerTag) {
                return { cell: notebookPanel.content.widgets[i], index: i };
            }
        }
    }
}


/***/ }),

/***/ "./lib/notebook.js":
/*!*************************!*\
  !*** ./lib/notebook.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TRANSFORMER_NB_FILE_NAME": () => (/* binding */ TRANSFORMER_NB_FILE_NAME),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "saveTransformerNotebook": () => (/* binding */ saveTransformerNotebook),
/* harmony export */   "showCurrentActiveCellTransformerWidget": () => (/* binding */ showCurrentActiveCellTransformerWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./settings */ "./lib/settings.js");
/* harmony import */ var _widgets_CellMetadataEditor__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widgets/CellMetadataEditor */ "./lib/widgets/CellMetadataEditor.js");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./lib/TagsUtils */ "./lib/lib/TagsUtils.js");









let transformerSettings;
const TRANSFORMER_NB_FILE_NAME = 'transformer.ipynb';
let editors = [];
let isTransformerEnabled;
let transformerNotebookPanel = null;
const saveTransformerNotebook = async () => {
    if (transformerNotebookPanel) {
        await transformerNotebookPanel.context.ready;
        await transformerNotebookPanel.context.save();
    }
};
const handleNotebookChanged = async (notebookTracker, notebookPanel) => {
    if (notebookPanel.title.label == TRANSFORMER_NB_FILE_NAME) {
        console.log("Now " + TRANSFORMER_NB_FILE_NAME + "...");
        if (editors.length != notebookPanel.model.cells.length) {
            makeCellTransformerWidgets(notebookPanel);
        }
        notebookPanel.content.activeCellChanged.connect((notebook, activeCell) => {
            let cellElement = notebook.node.childNodes[notebook.activeCellIndex];
            let transformerWidget = cellElement.querySelector('.cell-transformer-widget');
            if (!transformerWidget) {
                const transformerTag = _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].getCellTransformerTag(notebookPanel, notebook.activeCellIndex);
                let cellId = notebookPanel.model.cells.get(notebook.activeCellIndex).id;
                createCellTransformerWidgets(cellId, notebookPanel, cellElement, transformerTag, isTransformerEnabled);
            }
        });
        notebookPanel.model.cells.changed.connect((cells, change) => {
            makeCellTransformerWidgets(notebookPanel);
        });
        transformerNotebookPanel = notebookPanel;
    }
};
const makeCellTransformerWidgets = (notebookPanel) => {
    const cells = notebookPanel.model.cells;
    for (let index = 0; index < cells.length; index++) {
        let cellId = cells.get(index).id;
        let existedItems = editors.filter(item => item['cellId'] === cellId);
        if (existedItems.length > 0) {
            continue;
        }
        let isCodeCell = (0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.isCodeCellModel)(cells.get(index));
        let isRawCell = (0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.isRawCellModel)(cells.get(index));
        if ((!isCodeCell) && (!isRawCell)) {
            continue;
        }
        let transformerTag = _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].getCellTransformerTag(notebookPanel, index) ? _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].getCellTransformerTag(notebookPanel, index) : null;
        let cellElement = notebookPanel.content.node.childNodes[index];
        editors[index] = {
            cellId: cellId,
            notebookPanel: notebookPanel,
            transformerTag: transformerTag,
            cellElement: cellElement
        };
        createCellTransformerWidgets(cellId, notebookPanel, cellElement, transformerTag, isTransformerEnabled);
    }
};
const createCellTransformerWidgets = (cellId, notebookPanel, cellElement, transformerTag, isTransformerEnabled) => {
    const newChildNode = document.createElement('div');
    newChildNode.className = "cell-transformer-widget";
    let oldWidgets = cellElement.getElementsByClassName("cell-transformer-widget");
    for (let index = 0; index < oldWidgets.length; index++) {
        oldWidgets[index].remove();
    }
    cellElement.insertAdjacentElement('afterbegin', newChildNode);
    react_dom__WEBPACK_IMPORTED_MODULE_5__.render(react__WEBPACK_IMPORTED_MODULE_4__.createElement(_widgets_CellMetadataEditor__WEBPACK_IMPORTED_MODULE_7__.CellMetadataEditor, { cellId: cellId, notebookPanel: notebookPanel, cellElement: cellElement, transformerTag: transformerTag, transformerSettings: transformerSettings, isTransformerEnabled: isTransformerEnabled }), newChildNode);
};
const showCurrentActiveCellTransformerWidget = (notebookPanel) => {
    let notebook = notebookPanel.content;
    let cellElement = notebook.node.childNodes[notebook.activeCellIndex];
    let transformerMetaChip = cellElement.querySelector('.cell-transformer-widget .transformer-meta-chip');
    if (transformerMetaChip) {
        transformerMetaChip.click();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
    id: 'modeldeploy-proxy-labextension:notebook',
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager],
    autoStart: true,
    activate: async (app, settingRegistry, notebookTracker, docManager) => {
        Promise.all([settingRegistry.load(_settings__WEBPACK_IMPORTED_MODULE_8__.SETTINGS_ID)]).then(([settings]) => {
            transformerSettings = settings;
            isTransformerEnabled = (0,_settings__WEBPACK_IMPORTED_MODULE_8__.getTransformerEnabled)();
        });
        if (notebookTracker) {
            notebookTracker.currentChanged.connect(handleNotebookChanged);
        }
        app.started.then(() => {
        });
        app.restored.then(async () => {
        });
    },
});


/***/ }),

/***/ "./lib/settings.js":
/*!*************************!*\
  !*** ./lib/settings.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SETTINGS_ID": () => (/* binding */ SETTINGS_ID),
/* harmony export */   "addStatusChangeListener": () => (/* binding */ addStatusChangeListener),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "getTransformerEnabled": () => (/* binding */ getTransformerEnabled),
/* harmony export */   "getTransformerNotebookPath": () => (/* binding */ getTransformerNotebookPath),
/* harmony export */   "getTransformerProxyUrl": () => (/* binding */ getTransformerProxyUrl),
/* harmony export */   "setTransformerEnabled": () => (/* binding */ setTransformerEnabled),
/* harmony export */   "setTransformerNotebookPath": () => (/* binding */ setTransformerNotebookPath),
/* harmony export */   "setTransformerProxyUrl": () => (/* binding */ setTransformerProxyUrl),
/* harmony export */   "triggerStatusUpdate": () => (/* binding */ triggerStatusUpdate)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lib_NotebookUtils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./lib/NotebookUtils */ "./lib/lib/NotebookUtils.js");
/* harmony import */ var _lib_RPCUtils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./lib/RPCUtils */ "./lib/lib/RPCUtils.js");



const SETTINGS_ID = 'modeldeploy-proxy-labextension:settings';
const TRFANFORMER_CONFIG = 'transformerConfig';
let transformerEnabled = false;
let transformerNotebookPath = "";
let transformerNotebookPathOptions = [];
let transformerProxyUrl = "";
let transformerProxyStatus = "";
let statusChangeListeners = [];
const addStatusChangeListener = (callback) => {
    statusChangeListeners.push(callback);
    const current_status = {
        notebook_path: transformerNotebookPath,
        nb_path_options: transformerNotebookPathOptions,
        proxy_url: transformerProxyUrl,
        proxy_status: transformerProxyStatus
    };
    callback(current_status);
};
const triggerStatusUpdate = async (settings) => {
    await retrieveProxyInfo(settings);
};
const issueStatusChange = () => {
    const current_status = {
        notebook_path: transformerNotebookPath,
        nb_path_options: transformerNotebookPathOptions,
        proxy_url: transformerProxyUrl,
        proxy_status: transformerProxyStatus
    };
    statusChangeListeners.forEach(callback => {
        callback(current_status);
    });
};
const retrieveProxyInfo = async (settings) => {
    try {
        const kernel = await _lib_NotebookUtils__WEBPACK_IMPORTED_MODULE_1__["default"].createNewKernel();
        const proxy_info = await (0,_lib_RPCUtils__WEBPACK_IMPORTED_MODULE_2__.executeRpc)(kernel, 'proxy.info');
        kernel.shutdown();
        if (proxy_info.nb_paths) {
            if (!proxy_info.nb_paths.includes(transformerNotebookPath)) {
                console.log("Change notebook path to: " + proxy_info.nb_paths[0]);
                setTransformerNotebookPath(settings, proxy_info.nb_paths[0]);
            }
        }
        if (proxy_info.proxy_url && proxy_info.proxy_url !== transformerProxyUrl) {
            console.log("Change proxy URL to: " + proxy_info.proxy_url);
            setTransformerProxyUrl(settings, proxy_info.proxy_url);
        }
        console.log("Proxy status: " + proxy_info.proxy_status);
        transformerProxyStatus = proxy_info.proxy_status;
        transformerNotebookPathOptions = proxy_info.nb_paths;
        issueStatusChange();
    }
    catch (e) {
        console.warn("Unable to get settings form kernel!");
        console.warn(e);
    }
};
const getTransformerEnabled = () => {
    return transformerEnabled;
};
const setTransformerEnabled = (settings, enabled) => {
    transformerEnabled = enabled;
    let config = {
        enabled: enabled,
        notebookPath: transformerNotebookPath,
        proxyUrl: transformerProxyUrl
    };
    settings.set(TRFANFORMER_CONFIG, config).catch((reason) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};
const getTransformerNotebookPath = () => {
    return transformerNotebookPath;
};
const setTransformerNotebookPath = (settings, notebookPath) => {
    transformerNotebookPath = notebookPath;
    let config = {
        enabled: transformerEnabled,
        notebookPath: notebookPath,
        proxyUrl: transformerProxyUrl
    };
    settings.set(TRFANFORMER_CONFIG, config).catch((reason) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};
const getTransformerProxyUrl = () => {
    return transformerProxyUrl;
};
const setTransformerProxyUrl = (settings, proxyUrl) => {
    transformerProxyUrl = proxyUrl;
    let config = {
        enabled: transformerEnabled,
        notebookPath: transformerNotebookPath,
        proxyUrl: proxyUrl
    };
    settings.set(TRFANFORMER_CONFIG, config).catch((reason) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};
const defaultConfig = {
    enabled: false,
    notebookPath: "",
    proxyUrl: ""
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
    id: SETTINGS_ID,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry],
    autoStart: true,
    activate: (app, settingRegistry) => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(async ([settings]) => {
            try {
                let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite;
                if (typeof transformerSettings.enabled === 'string') {
                    if (transformerSettings.enabled === 'true') {
                        transformerEnabled = true;
                    }
                    else {
                        transformerEnabled = false;
                    }
                }
                else if (typeof transformerSettings.enabled === 'boolean') {
                    transformerEnabled = transformerSettings.enabled;
                }
                if (typeof transformerSettings.notebookPath === 'string') {
                    transformerNotebookPath = transformerSettings.notebookPath;
                }
                if (typeof transformerSettings.proxyUrl === 'string') {
                    transformerProxyUrl = transformerSettings.proxyUrl;
                }
                else if (typeof transformerSettings.proxyUrl === 'number') {
                    transformerProxyUrl = transformerSettings.proxyUrl.toString();
                }
                issueStatusChange();
            }
            catch (error) {
                settingRegistry.set(SETTINGS_ID, TRFANFORMER_CONFIG, defaultConfig).catch((reason) => {
                    console.error('Failed to set transformer config: ' + reason.message);
                });
            }
            retrieveProxyInfo(settings);
            console.log("Settings when starts up: enabled(" + transformerEnabled + "), NotebookPath(" + transformerNotebookPath + "), ProxyUrl(" + transformerProxyUrl + ")");
        });
    },
});


/***/ }),

/***/ "./lib/sidebar.js":
/*!************************!*\
  !*** ./lib/sidebar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cell-toolbar */ "webpack/sharing/consume/default/@jupyterlab/cell-toolbar");
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./settings */ "./lib/settings.js");
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./notebook */ "./lib/notebook.js");








const SIDEBAR_ID = 'modeldeploy-proxy-labextension:sidebar';
const TRANSFORMER_FACTORY = 'transformer';
let isTransformerEnabled = true;
const updateTransformerEnabled = (settings) => {
    isTransformerEnabled = (0,_settings__WEBPACK_IMPORTED_MODULE_6__.getTransformerEnabled)();
};
let isTransformerNotebook = false;
const handleNotebookChanged = async (notebookTracker, notebookPanel) => {
    if (notebookPanel.title.label == _notebook__WEBPACK_IMPORTED_MODULE_7__.TRANSFORMER_NB_FILE_NAME) {
        isTransformerNotebook = true;
    }
    else {
        isTransformerNotebook = false;
    }
};
const isEnabled = () => {
    return isTransformerEnabled && isTransformerNotebook;
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
    id: SIDEBAR_ID,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__.INotebookTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    autoStart: true,
    activate: async (app, notebookTracker, settingRegistry, toolbarRegistry, translator) => {
        Promise.all([settingRegistry.load(_settings__WEBPACK_IMPORTED_MODULE_6__.SETTINGS_ID)]).then(([settings]) => {
            settings.changed.connect(updateTransformerEnabled);
            isTransformerEnabled = (0,_settings__WEBPACK_IMPORTED_MODULE_6__.getTransformerEnabled)();
        });
        if (notebookTracker) {
            notebookTracker.currentChanged.connect(handleNotebookChanged);
        }
        app.commands.addCommand('notebook:transformer', {
            label: 'Transformer',
            caption: 'Enable/disable transformer annotation widgets.',
            execute: args => {
                let currentCellIndex = notebookTracker.currentWidget.content.activeCellIndex;
                let toggle = notebookTracker.currentWidget.content.node.childNodes[currentCellIndex].querySelector('.transformer-cell-metadata-editor-toggle');
                toggle.click();
            },
            icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.treeViewIcon : ''),
            isEnabled: isEnabled
        });
        const toolbarItems = settingRegistry && toolbarRegistry ? (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.createToolbarFactory)(toolbarRegistry, settingRegistry, TRANSFORMER_FACTORY, SIDEBAR_ID, translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator) : undefined;
        app.docRegistry.addWidgetExtension('Notebook', new _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_3__.CellBarExtension(app.commands, toolbarItems));
    },
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IToolbarWidgetRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator]
});


/***/ }),

/***/ "./lib/states.js":
/*!***********************!*\
  !*** ./lib/states.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "addStatesChangeListener": () => (/* binding */ addStatesChangeListener),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "fetchTransformerStates": () => (/* binding */ fetchTransformerStates),
/* harmony export */   "issueTransformerStatesChange": () => (/* binding */ issueTransformerStatesChange)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const id = 'transformer-extension:ITransformerStates';
const ITransformerStates = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token(id);
let transformerStatesList = {};
const assertTransformerStates = (notebookPanelId) => {
    if (!transformerStatesList[notebookPanelId]) {
        let transformerStates = {
            isPredictTagged: false,
            isRequirementsTagged: false,
            isCVATInfoTagged: false,
            isCVATInvokeTagged: false
        };
        let stateChangeListeners = [];
        transformerStatesList[notebookPanelId] = {
            states: transformerStates,
            listeners: stateChangeListeners
        };
    }
};
const fetchTransformerStates = (notebookPanelId) => {
    if (!transformerStatesList[notebookPanelId]) {
        assertTransformerStates(notebookPanelId);
    }
    return transformerStatesList[notebookPanelId].states;
};
const issueTransformerStatesChange = (notebookPanelId, issuer, states) => {
    if (!transformerStatesList[notebookPanelId]) {
        assertTransformerStates(notebookPanelId);
    }
    Object.assign(transformerStatesList[notebookPanelId].states, states);
    transformerStatesList[notebookPanelId].listeners.forEach(callback => {
        callback(issuer, states);
    });
};
const addStatesChangeListener = (notebookPanelId, callback) => {
    if (!transformerStatesList[notebookPanelId]) {
        assertTransformerStates(notebookPanelId);
    }
    transformerStatesList[notebookPanelId].listeners.push(callback);
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
    id: 'modeldeploy-proxy-labextension:states',
    provides: ITransformerStates,
    autoStart: true,
    activate: (app) => {
        app.started.then(() => {
        });
        app.restored.then(async () => {
        });
    }
});


/***/ }),

/***/ "./lib/theme.js":
/*!**********************!*\
  !*** ./lib/theme.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "theme": () => (/* binding */ theme)
/* harmony export */ });
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/createTheme.js");

const theme = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_0__["default"])({
    palette: {
        secondary: {
            main: '#753BBD',
            dark: '#512984',
            light: '#9062ca',
        },
        primary: {
            main: '#2e82d7',
            dark: '#205b96',
            light: '#579bdf',
        },
    },
    transformer: {
        headers: {
            main: '#753BBD',
        },
    },
});


/***/ }),

/***/ "./lib/widgets/CellMetadataEditor.js":
/*!*******************************************!*\
  !*** ./lib/widgets/CellMetadataEditor.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CELL_TYPE_CVAT_INFO": () => (/* binding */ CELL_TYPE_CVAT_INFO),
/* harmony export */   "CELL_TYPE_CVAT_INVOKE": () => (/* binding */ CELL_TYPE_CVAT_INVOKE),
/* harmony export */   "CELL_TYPE_PREDICT": () => (/* binding */ CELL_TYPE_PREDICT),
/* harmony export */   "CELL_TYPE_REQUIREMENTS": () => (/* binding */ CELL_TYPE_REQUIREMENTS),
/* harmony export */   "CellMetadataEditor": () => (/* binding */ CellMetadataEditor),
/* harmony export */   "RESERVED_CELL_NAMES": () => (/* binding */ RESERVED_CELL_NAMES),
/* harmony export */   "RESERVED_CELL_NAMES_CHIP_COLOR": () => (/* binding */ RESERVED_CELL_NAMES_CHIP_COLOR),
/* harmony export */   "RESERVED_CELL_NAMES_HELP_TEXT": () => (/* binding */ RESERVED_CELL_NAMES_HELP_TEXT)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_icons_Close__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @material-ui/icons/Close */ "./node_modules/@material-ui/icons/Close.js");
/* harmony import */ var _material_ui_icons_Check__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @material-ui/icons/Check */ "./node_modules/@material-ui/icons/Check.js");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core */ "webpack/sharing/consume/default/@material-ui/core/@material-ui/core");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_Select__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./../components/Select */ "./lib/components/Select.js");
/* harmony import */ var _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./../lib/TagsUtils */ "./lib/lib/TagsUtils.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _CellMetadataEditorDialog__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./CellMetadataEditorDialog */ "./lib/widgets/CellMetadataEditorDialog.js");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../settings */ "./lib/settings.js");
/* harmony import */ var _states__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../states */ "./lib/states.js");
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../notebook */ "./lib/notebook.js");
/* harmony import */ var _lib_CellUtils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./../lib/CellUtils */ "./lib/lib/CellUtils.js");













const CELL_TYPE_NA = 'na';
const CELL_TYPE_NA_LABEL = '-';
const CELL_TYPE_PREDICT = 'predict';
const CELL_TYPE_REQUIREMENTS = 'requirements';
const CELL_TYPE_CVAT_INFO = 'cvat-info';
const CELL_TYPE_CVAT_INVOKE = 'cvat-invoke';
const CELL_TYPES = [
    {
        value: CELL_TYPE_NA,
        label: CELL_TYPE_NA_LABEL,
        helpText: null,
        chipColor: null
    },
    {
        value: CELL_TYPE_REQUIREMENTS,
        label: 'Requirements',
        helpText: 'The code in this cell will be parsed as requirements packages and install in system.',
        chipColor: '84ffff'
    },
    {
        value: CELL_TYPE_PREDICT,
        label: 'Predict',
        helpText: 'The code in this cell will be parsed as the handler of the predict API on proxy.',
        chipColor: 'b9f6ca'
    },
    {
        value: 'functions',
        label: 'Extra functions',
        helpText: 'The code in this cell will be parsed as referenced function for the predict or cvat_invoke functions.',
        chipColor: 'ccff90'
    },
    {
        value: CELL_TYPE_CVAT_INFO,
        label: 'CVAT Info',
        helpText: 'The code in this cell will be parsed as cvat_info callback function.',
        chipColor: 'c6ff00'
    },
    {
        value: CELL_TYPE_CVAT_INVOKE,
        label: 'CVAT invoke',
        helpText: 'The code in this cell will be parsed as the handler of the cvat_invoke API on proxy.',
        chipColor: 'f4ff81'
    }
];
const CELL_TYPE_SELECT_OPTIONS = CELL_TYPES
    //.filter(item => item['value'] !== CELL_TYPE_NA)
    .map(item => {
    const newItem = Object.assign({}, item);
    delete newItem['helpText'];
    delete newItem.chipColor;
    return newItem;
});
const RESERVED_CELL_NAMES = CELL_TYPES
    .filter(item => item['value'] !== CELL_TYPE_NA)
    .map(item => {
    return item['value'];
});
const RESERVED_CELL_NAMES_HELP_TEXT = CELL_TYPES
    .reduce((obj, item) => {
    obj[item.value] = item.helpText;
    return obj;
}, {});
const RESERVED_CELL_NAMES_CHIP_COLOR = CELL_TYPES
    .reduce((obj, item) => {
    obj[item.value] = item.chipColor;
    return obj;
}, {});
const PREDICT_DEF_REGEX = /\s*def\s+predict\s*\((\s*[\., \w]+\s*(:\s*[\., \s, \w]+\s*)?(=[\w\W]+)?,?){0,3}\)\s*(->\s*\S+\s*)?:\s*/i;
const PREDICT_DEFAULT_CODE_SNIPPET = `from typing import Dict
import flask
from prometheus_client import Counter, Gauge, Summary, Histogram
def predict(request: flask.Request, model_predict_url: str, predict_metric_type: Counter or Gauge or Summary or Histogram = None) -> Dict:
    # Notice: once you reconstruct the predict_metric_type object, return it as the second return value.
    return flask.redirect(model_predict_url)`;
const CVAT_INFO_DEF_REGEX = /\s*def\s+cvat_info\s*\((\s*[\., \w]+\s*(:\s*[\., \s, \w]+\s*)?(=[\w\W]+)?,?){0,1}\)\s*(->\s*\S+\s*)?:\s*/i;
const CVAT_INFO_DEFAULT_CODE_SNIPPET = `from typing import Dict
import flask
def cvat_info(request: flask.Request) -> Dict:
    return {
        "framework": "",
        "spec": None,
        "type": "",
        "description": ""
    }`;
const CVAT_INVOKE_DEF_REGEX = /\s*def\s+cvat_invoke\s*\((\s*[\., \w]+\s*(:\s*[\., \s, \w]+\s*)?(=[\w\W]+)?,?){0,3}\)\s*(->\s*\S+\s*)?:\s*/i;
const CVAT_INVOKE_DEFAULT_CODE_SNIPPET = `from typing import Dict
import flask
from prometheus_client import Counter, Gauge, Summary, Histogram
def cvat_invoke(request: flask.Request, model_predict_url: str, cvat_invoke_metric_type: Counter or Gauge or Summary or Histogram = None) -> Dict:
    # Notice: once you reconstruct the predict_metric_type object, return it as the second return value.
    return []`;
class CellMetadataEditor extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.transformerStates = null;
        this.isTagged = (tag) => {
            if (tag === CELL_TYPE_PREDICT) {
                return this.transformerStates.isPredictTagged;
            }
            else if (tag === CELL_TYPE_REQUIREMENTS) {
                return this.transformerStates.isRequirementsTagged;
            }
            else if (tag === CELL_TYPE_CVAT_INFO) {
                return this.transformerStates.isCVATInfoTagged;
            }
            else if (tag === CELL_TYPE_CVAT_INVOKE) {
                return this.transformerStates.isCVATInvokeTagged;
            }
            return false;
        };
        this.updateLocalTransformerStates = (tag, tagged) => {
            if (tag === CELL_TYPE_PREDICT) {
                this.transformerStates.isPredictTagged = tagged;
            }
            else if (tag === CELL_TYPE_REQUIREMENTS) {
                this.transformerStates.isRequirementsTagged = tagged;
            }
            else if (tag === CELL_TYPE_CVAT_INFO) {
                this.transformerStates.isCVATInfoTagged = tagged;
            }
            else if (tag === CELL_TYPE_CVAT_INVOKE) {
                this.transformerStates.isCVATInvokeTagged = tagged;
            }
        };
        this.onStatesChangeCallback = (issuer, newStates) => {
            if (issuer == this.props.cellId) {
                return;
            }
            ;
            this.transformerStates = newStates;
            this.setState({ typeSelectOptions: this.getTypeSelectOptions([this.state.transformerTag]) });
        };
        this.updateTransformerEnabled = (settings) => {
            this.setState({ isTransformerEnabled: (0,_settings__WEBPACK_IMPORTED_MODULE_3__.getTransformerEnabled)() });
        };
        this.checkCellCodeDefinitionConfirmed = (notebook, cellIndex, tag) => {
            console.log("checkCellCodeDefinitionConfirmed");
            let regex = null;
            if (tag == CELL_TYPE_PREDICT) {
                regex = PREDICT_DEF_REGEX;
            }
            else if (tag == CELL_TYPE_CVAT_INFO) {
                regex = CVAT_INFO_DEF_REGEX;
            }
            else if (tag == CELL_TYPE_CVAT_INVOKE) {
                regex = CVAT_INVOKE_DEF_REGEX;
            }
            if (regex) {
                if (_lib_CellUtils__WEBPACK_IMPORTED_MODULE_4__["default"].isCellVoid(notebook, cellIndex)) {
                    return {
                        confirmed: false,
                        error: 0 /* VOID */
                    };
                }
                else if (!_lib_CellUtils__WEBPACK_IMPORTED_MODULE_4__["default"].isTextInCell(notebook, cellIndex, regex)) {
                    return {
                        confirmed: false,
                        error: 1 /* FUNC_DEF_ERROR */
                    };
                }
            }
            return {
                confirmed: true
            };
        };
        this.updateCurrentCellTag = async (value) => {
            if (value !== this.state.transformerTag) {
                let notebook = this.props.notebookPanel.content;
                let currentCellType = this.props.notebookPanel.model.cells.get(notebook.activeCellIndex).type;
                let targetCellType = currentCellType;
                if (value == CELL_TYPE_PREDICT || value == CELL_TYPE_CVAT_INFO || value == CELL_TYPE_CVAT_INVOKE) {
                    let confirmedResult = this.checkCellCodeDefinitionConfirmed(notebook, notebook.activeCellIndex, value);
                    if (!confirmedResult.confirmed) {
                        let codeSnippet = PREDICT_DEFAULT_CODE_SNIPPET;
                        if (value == CELL_TYPE_CVAT_INFO) {
                            codeSnippet = CVAT_INFO_DEFAULT_CODE_SNIPPET;
                        }
                        else if (value == CELL_TYPE_CVAT_INVOKE) {
                            codeSnippet = CVAT_INVOKE_DEFAULT_CODE_SNIPPET;
                        }
                        if (confirmedResult.error == 0 /* VOID */) {
                            _lib_CellUtils__WEBPACK_IMPORTED_MODULE_4__["default"].injectCodeAtIndex(notebook, notebook.activeCellIndex, codeSnippet);
                        }
                        else if (confirmedResult.error == 1 /* FUNC_DEF_ERROR */) {
                            let dialogTitle = "Function %s is not well defined!".replace(/%s/i, value);
                            let dialogContent = "Please define function %s as follows:".replace(/%s/i, value);
                            this.setState({
                                dialogTitle: dialogTitle,
                                dialogContent: dialogContent,
                                dialogCode: codeSnippet
                            });
                            this.toggleTagsEditorDialog();
                            return;
                        }
                    }
                    targetCellType = 'code';
                }
                else if (value == CELL_TYPE_REQUIREMENTS) {
                    targetCellType = 'raw';
                }
                this.updateLocalTransformerStates(this.state.transformerTag, false);
                this.updateLocalTransformerStates(value, true);
                (0,_states__WEBPACK_IMPORTED_MODULE_5__.issueTransformerStatesChange)(this.props.notebookPanel.id, this.props.cellId, this.transformerStates);
                if (RESERVED_CELL_NAMES.includes(value)) {
                    this.setState({ transformerTag: value });
                }
                else if (CELL_TYPE_NA === value) {
                    this.setState({ transformerTag: CELL_TYPE_NA });
                }
                if (currentCellType != targetCellType) {
                    console.log("Keep transformer metadata in cell metadata and replace cell widget...");
                    let cellMetadata = {
                        transformerTag: value,
                    };
                    _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].setCellTransformerTag(this.props.notebookPanel, notebook.activeCellIndex, cellMetadata, false).then(newValue => {
                        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.changeCellType(notebook, targetCellType);
                        (0,_notebook__WEBPACK_IMPORTED_MODULE_7__.showCurrentActiveCellTransformerWidget)(this.props.notebookPanel);
                    });
                }
            }
        };
        this.saveCellTagInNotebookFile = () => {
            console.log("saveCellTagInNotebookFile");
            let value = this.state.transformerTag;
            if (value == CELL_TYPE_PREDICT || value == CELL_TYPE_CVAT_INFO || value == CELL_TYPE_CVAT_INVOKE) {
                let notebook = this.props.notebookPanel.content;
                let confirmedResult = this.checkCellCodeDefinitionConfirmed(notebook, notebook.activeCellIndex, value);
                if (!confirmedResult.confirmed) {
                    if (confirmedResult.error == 0 /* VOID */) {
                        let dialogTitle = "Function %s is void!".replace(/%s/i, value);
                        let dialogContent = "Unable to apply the function %s defined here!".replace(/%s/i, value);
                        this.setState({
                            dialogTitle: dialogTitle,
                            dialogContent: dialogContent,
                            dialogCode: null
                        });
                        this.toggleTagsEditorDialog();
                        return;
                    }
                    if (confirmedResult.error == 1 /* FUNC_DEF_ERROR */) {
                        let codeSnippet = PREDICT_DEFAULT_CODE_SNIPPET;
                        if (value == CELL_TYPE_CVAT_INFO) {
                            codeSnippet = CVAT_INFO_DEFAULT_CODE_SNIPPET;
                        }
                        else if (value == CELL_TYPE_CVAT_INVOKE) {
                            codeSnippet = CVAT_INVOKE_DEFAULT_CODE_SNIPPET;
                        }
                        let dialogTitle = "Function %s is not well defined!".replace(/%s/i, value);
                        let dialogContent = "Please define function %s as follows:".replace(/%s/i, value);
                        this.setState({
                            dialogTitle: dialogTitle,
                            dialogContent: dialogContent,
                            dialogCode: codeSnippet
                        });
                        this.toggleTagsEditorDialog();
                        return;
                    }
                }
            }
            let isDuplicated = false;
            if (value == CELL_TYPE_PREDICT || value == CELL_TYPE_CVAT_INFO || value == CELL_TYPE_CVAT_INVOKE) {
                isDuplicated = _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].isTransformerTagExistedInOtherCells(this.props.notebookPanel, this.props.notebookPanel.content.activeCellIndex, value);
            }
            if (isDuplicated) {
                this.setState({
                    dialogTitle: "Error",
                    dialogContent: value + " is limited to be just one.",
                    dialogCode: null
                });
                this.toggleTagsEditorDialog();
            }
            else {
                if (RESERVED_CELL_NAMES.includes(value)) {
                    let cellMetadata = {
                        transformerTag: value,
                    };
                    _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].setCellTransformerTag(this.props.notebookPanel, this.props.notebookPanel.content.activeCellIndex, cellMetadata).then(newValue => {
                        this.hideSelector();
                    });
                }
                else if (CELL_TYPE_NA === value) {
                    _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].resetCellTransformerTag(this.props.notebookPanel, this.props.notebookPanel.content.activeCellIndex).then(newValue => {
                        this.hideSelector();
                    });
                }
            }
        };
        this.removeCellTagInNotebookFile = () => {
            this.updateLocalTransformerStates(this.state.transformerTag, false);
            (0,_states__WEBPACK_IMPORTED_MODULE_5__.issueTransformerStatesChange)(this.props.notebookPanel.id, this.props.cellId, this.transformerStates);
            _lib_TagsUtils__WEBPACK_IMPORTED_MODULE_6__["default"].resetCellTransformerTag(this.props.notebookPanel, this.props.notebookPanel.content.activeCellIndex).then(newValue => {
                // update transformerTag state HERE to avoid a tricky issue
                this.setState({ transformerTag: CELL_TYPE_NA });
                this.hideSelector();
            });
        };
        this.onBeforeUpdate = (value) => {
            if (value === this.props.transformerTag) {
                return false;
            }
            return false;
        };
        this.componentDidMount = () => {
        };
        this.getTypeSelectOptions = (keepTags) => {
            return CELL_TYPE_SELECT_OPTIONS
                .filter(item => (keepTags.includes(item['value']) || !this.isTagged(item['value'])))
                .map(item => {
                const newItem = Object.assign({}, item);
                delete newItem['helpText'];
                delete newItem.chipColor;
                return newItem;
            });
        };
        this.transformerStates = (0,_states__WEBPACK_IMPORTED_MODULE_5__.fetchTransformerStates)(this.props.notebookPanel.id);
        this.updateLocalTransformerStates(props.transformerTag, true);
        (0,_states__WEBPACK_IMPORTED_MODULE_5__.addStatesChangeListener)(this.props.notebookPanel.id, this.onStatesChangeCallback);
        (0,_states__WEBPACK_IMPORTED_MODULE_5__.issueTransformerStatesChange)(this.props.notebookPanel.id, this.props.cellId, this.transformerStates);
        const defaultState = {
            transformerTag: props.transformerTag ? props.transformerTag : CELL_TYPE_NA,
            isChipVisible: RESERVED_CELL_NAMES.includes(props.transformerTag) ? true : false,
            isSelectorVisible: false,
            cellMetadataEditorDialog: false,
            dialogTitle: 'Warning',
            dialogContent: '',
            dialogCode: null,
            isTransformerEnabled: this.props.isTransformerEnabled,
            typeSelectOptions: this.getTypeSelectOptions([props.transformerTag])
        };
        this.state = defaultState;
        this.updateCurrentCellTag = this.updateCurrentCellTag.bind(this);
        this.toggleTagsEditorDialog = this.toggleTagsEditorDialog.bind(this);
        if (this.props.transformerSettings) {
            this.props.transformerSettings.changed.connect(this.updateTransformerEnabled);
        }
    }
    isEqual(a, b) {
        return JSON.stringify(a) === JSON.stringify(b);
    }
    componentDidUpdate(prevProps, prevState) {
        this.hideEditorIfNotCodeCell();
    }
    hideEditorIfNotCodeCell() {
    }
    static getDerivedStateFromProps(props, state) {
        return null;
    }
    toggleSelector() {
        if (this.state.isSelectorVisible) {
            this.hideSelector();
        }
        else {
            this.showSelector();
        }
    }
    showSelector() {
        this.setState({
            isSelectorVisible: true,
            isChipVisible: false
        });
    }
    hideSelector() {
        this.setState({
            isSelectorVisible: false,
            isChipVisible: RESERVED_CELL_NAMES.includes(this.state.transformerTag) ? true : false
        });
    }
    onChipClick() {
        this.setState({ isSelectorVisible: true, isChipVisible: false });
    }
    toggleTagsEditorDialog() {
        this.setState({ cellMetadataEditorDialog: !this.state.cellMetadataEditorDialog });
    }
    render() {
        const cellColor = 'transparent';
        // add class names for styling
        if (!this.state.isTransformerEnabled) {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        }
        else if (this.state.isSelectorVisible) {
            this.props.cellElement.classList.add('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        }
        else if (this.state.isChipVisible) {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.add('with-transformer-chip');
        }
        else {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        }
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-inline-cell-metadata' + ((this.state.isTransformerEnabled && this.state.isChipVisible) ? '' : ' hidden') },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Tooltip, { placement: "top", key: this.state.transformerTag + 'tooltip', title: RESERVED_CELL_NAMES.includes(this.state.transformerTag) ?
                        RESERVED_CELL_NAMES_HELP_TEXT[this.state.transformerTag] :
                        'This cell starts the pipeline step: ' + this.state.transformerTag },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Chip, { className: 'transformer-meta-chip', key: this.state.transformerTag, label: this.state.transformerTag, onClick: () => this.onChipClick(), style: { backgroundColor: `#${RESERVED_CELL_NAMES_CHIP_COLOR[this.state.transformerTag]}` } }))),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-metadata-editor-wrapper' + ((this.state.isTransformerEnabled && this.state.isSelectorVisible) ? '' : ' hidden') },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-cell-metadata-editor', style: { borderLeft: `2px solid ${cellColor}` } },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_Select__WEBPACK_IMPORTED_MODULE_8__.Select, { updateValue: this.updateCurrentCellTag, values: this.state.typeSelectOptions, value: RESERVED_CELL_NAMES.includes(this.state.transformerTag) ? this.state.transformerTag : 'na', label: 'Cell tag', index: 0, variant: "outlined", style: { width: 'auto', minWidth: '14em' } }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.IconButton, { "aria-label": "remove", onClick: () => this.removeCellTagInNotebookFile() },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_Close__WEBPACK_IMPORTED_MODULE_9__["default"], { fontSize: "small" })),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.IconButton, { "aria-label": "apply", onClick: () => this.saveCellTagInNotebookFile() },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_Check__WEBPACK_IMPORTED_MODULE_10__["default"], { fontSize: "small" })),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.IconButton, { className: 'transformer-cell-metadata-editor-toggle', "aria-label": "toggle", onClick: () => this.toggleSelector(), style: { width: '0', height: '0', padding: '0' } })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-cell-metadata-editor-helper-text' + (this.state.isSelectorVisible ? '' : ' hidden') })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_CellMetadataEditorDialog__WEBPACK_IMPORTED_MODULE_11__.CellMetadataEditorDialog, { open: this.state.cellMetadataEditorDialog, toggleDialog: this.toggleTagsEditorDialog, title: this.state.dialogTitle, content: this.state.dialogContent, code: this.state.dialogCode })));
    }
}


/***/ }),

/***/ "./lib/widgets/CellMetadataEditorDialog.js":
/*!*************************************************!*\
  !*** ./lib/widgets/CellMetadataEditorDialog.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellMetadataEditorDialog": () => (/* binding */ CellMetadataEditorDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core */ "webpack/sharing/consume/default/@material-ui/core/@material-ui/core");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__);


const CellMetadataEditorDialog = props => {
    const handleClose = () => {
        props.toggleDialog();
    };
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Dialog, { open: props.open, onClose: handleClose, fullWidth: true, maxWidth: 'sm', scroll: "paper", "aria-labelledby": "scroll-dialog-title", "aria-describedby": "scroll-dialog-description" },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.DialogTitle, { id: "scroll-dialog-title" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: 'dialog-title' }, props.title)),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.DialogContent, { dividers: true },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, props.content),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'dialog-code-snippet' + ((props.code) ? '' : ' hidden') },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("code", { style: { whiteSpace: "pre" } }, props.code))),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.DialogActions, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Button, { onClick: handleClose, color: "primary" }, "Ok"))));
};


/***/ }),

/***/ "./lib/widgets/TransformerLeftPanel.js":
/*!*********************************************!*\
  !*** ./lib/widgets/TransformerLeftPanel.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TransformerLeftPanel": () => (/* binding */ TransformerLeftPanel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/styles/esm/ThemeProvider/ThemeProvider.js");
/* harmony import */ var _theme__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../theme */ "./lib/theme.js");
/* harmony import */ var _lib_RPCUtils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../lib/RPCUtils */ "./lib/lib/RPCUtils.js");
/* harmony import */ var _lib_NotebookUtils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./../lib/NotebookUtils */ "./lib/lib/NotebookUtils.js");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./../settings */ "./lib/settings.js");
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../notebook */ "./lib/notebook.js");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core */ "webpack/sharing/consume/default/@material-ui/core/@material-ui/core");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _material_ui_icons_Info__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @material-ui/icons/Info */ "./node_modules/@material-ui/icons/Info.js");
/* harmony import */ var _material_ui_icons_ExpandMoreRounded__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @material-ui/icons/ExpandMoreRounded */ "./node_modules/@material-ui/icons/ExpandMoreRounded.js");
/* harmony import */ var _material_ui_icons_Refresh__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @material-ui/icons/Refresh */ "./node_modules/@material-ui/icons/Refresh.js");











class TransformerLeftPanel extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.componentDidMount = () => {
            (0,_settings__WEBPACK_IMPORTED_MODULE_2__.addStatusChangeListener)((status) => {
                this.setState({
                    proxyUrl: status.proxy_url,
                    proxyStatus: status.proxy_status,
                    transformerNotebookPath: status.notebook_path,
                    transformerNotebookPathOptions: status.nb_path_options,
                    isStatusLoading: false
                });
            });
        };
        this.componentDidUpdate = (prevProps, prevState) => {
        };
        this.applyTransformerToProxy = async () => {
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
        this.doApplyTransformer = async () => {
            this.renderDialog({
                title: 'Running',
                content: 'This will take few seconds!',
                isCloseButtonVisible: false
            });
            (0,_notebook__WEBPACK_IMPORTED_MODULE_3__.saveTransformerNotebook)();
            let proxyUrl = this.state.proxyUrl;
            if (!proxyUrl) {
                this.renderDialog({
                    title: 'Error',
                    content: 'Unable to get the proxy URL!'
                });
                this.setState({ dialogConfirmClickHandler: this.onDialogConfirmClick });
                return;
            }
            try {
                const kernel = await _lib_NotebookUtils__WEBPACK_IMPORTED_MODULE_4__["default"].createNewKernel();
                const args = {
                    proxy_url: proxyUrl,
                    source_notebook_path: this.state.transformerNotebookPath
                };
                await (0,_lib_RPCUtils__WEBPACK_IMPORTED_MODULE_5__.executeRpc)(kernel, 'proxy.apply', args);
                kernel.shutdown();
                this.renderDialog({
                    title: 'Done',
                    content: 'The transforming is completed!!'
                });
            }
            catch (error) {
                (0,_lib_RPCUtils__WEBPACK_IMPORTED_MODULE_5__.globalUnhandledRejection)({ reason: error });
                this.renderDialog({
                    visible: false
                });
            }
            this.setState({ dialogConfirmClickHandler: this.onDialogConfirmClick });
        };
        this.resetTransformer = () => {
            console.log('resetTransformer');
            this.renderDialog({
                title: 'Warning',
                content: 'This will reset transformer.ipynb and you may lose your code!',
                closeButtonText: 'Cancel',
                isConfirmButtonVisible: true
            });
            this.setState({ dialogConfirmClickHandler: this.doResetTransformer });
        };
        this.doResetTransformer = async () => {
            console.log("doResetTransformer");
            let proxyUrl = this.state.proxyUrl;
            if (!proxyUrl) {
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
                const kernel = await _lib_NotebookUtils__WEBPACK_IMPORTED_MODULE_4__["default"].createNewKernel();
                const args = {
                    proxy_url: proxyUrl,
                    source_notebook_path: this.state.transformerNotebookPath
                };
                await (0,_lib_RPCUtils__WEBPACK_IMPORTED_MODULE_5__.executeRpc)(kernel, 'proxy.reset', args);
                kernel.shutdown();
                this.renderDialog({
                    title: 'Reset is done',
                    content: 'You need to reload the page!',
                    isCloseButtonVisible: false,
                    isConfirmButtonVisible: true
                });
                this.setState({ dialogConfirmClickHandler: this.doReloadPage });
                return;
            }
            catch (error) {
                (0,_lib_RPCUtils__WEBPACK_IMPORTED_MODULE_5__.globalUnhandledRejection)({ reason: error });
                this.renderDialog({
                    visible: false
                });
            }
        };
        this.doReloadPage = async () => {
            this.renderDialog({
                visible: false
            });
            window.location.reload();
        };
        this.onTransformerEnableChanged = (enabled) => {
            this.setState({ isEnabled: enabled });
            (0,_settings__WEBPACK_IMPORTED_MODULE_2__.setTransformerEnabled)(this.props.transformerSettings, enabled);
        };
        this.onDialogCloseClick = this.onDialogCloseClick.bind(this);
        this.onDialogConfirmClick = this.onDialogConfirmClick.bind(this);
        this.doResetTransformer = this.doResetTransformer.bind(this);
        this.doReloadPage = this.doReloadPage.bind(this);
        this.refreshStatus = this.refreshStatus.bind(this);
        this.changetransformerNotebookPath = this.changetransformerNotebookPath.bind(this);
        const defaultState = {
            isEnabled: (0,_settings__WEBPACK_IMPORTED_MODULE_2__.getTransformerEnabled)(),
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
    renderDialog({ visible, title, content, isCloseButtonVisible, closeButtonText, isConfirmButtonVisible }) {
        this.setState({
            isDialogVisible: visible !== undefined ? visible : true,
            dialogTitle: title !== undefined ? title : '',
            dialogContent: content !== undefined ? content : '',
            isDialogCloseButtonVisible: isCloseButtonVisible !== undefined ? isCloseButtonVisible : true,
            closeButtonText: closeButtonText !== undefined ? closeButtonText : 'Ok',
            isDialogConfirmButtonVisible: isConfirmButtonVisible !== undefined ? isConfirmButtonVisible : false
        });
    }
    changetransformerNotebookPath(value) {
        this.setState({
            transformerNotebookPath: value
        });
        (0,_settings__WEBPACK_IMPORTED_MODULE_2__.setTransformerNotebookPath)(this.props.transformerSettings, value);
    }
    refreshStatus() {
        this.setState({
            isStatusLoading: true
        });
        (0,_settings__WEBPACK_IMPORTED_MODULE_2__.triggerStatusUpdate)(this.props.transformerSettings);
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
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_6__["default"], { theme: _theme__WEBPACK_IMPORTED_MODULE_7__.theme },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'leftpanel-transformer-widget', key: "transformer-widget", style: { padding: 'var(--jp-code-padding)' } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'leftpanel-transformer-widget-content' },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "h5", gutterBottom: true }, "Transformer Panel"),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-component' },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "body1", gutterBottom: true, style: { color: _theme__WEBPACK_IMPORTED_MODULE_7__.theme.transformer.headers.main } },
                            "Transformer is the extension for model inference, it helps you customizing the proxy API handlers by defining the corresponding functions on ",
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement("strong", { style: { fontWeight: '600' } }, "transformer.ipynb"),
                            " notebook.")),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "transformer-toggler" },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "toolbar input-container" },
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Switch, { checked: this.state.isEnabled, onChange: c => this.onTransformerEnableChanged(c.target.checked), color: "primary", name: "enable-transformer", inputProps: { 'aria-label': 'primary checkbox' }, classes: { root: 'material-switch' } }),
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'switch-label', style: { display: 'inline-block' } },
                                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "overline", display: "block" }, (this.state.isEnabled ? 'Disable' : 'Enable') + ' widgets'))))),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-component' + (this.state.isEnabled ? '' : ' hidden'), style: { marginTop: '1em' } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Divider, { variant: "middle", style: { margin: '1em 0' } }),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "subtitle2", display: "block", gutterBottom: true },
                            "STATUS",
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null,
                                this.state.isStatusLoading && react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.CircularProgress, { size: 16, style: { position: "relative", top: "0.2em", left: "0.5em" } }),
                                !this.state.isStatusLoading && react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_Refresh__WEBPACK_IMPORTED_MODULE_8__["default"], { onClick: this.refreshStatus, color: "primary", fontSize: "small", style: { position: "relative", top: "0.25em", left: "0.2em", cursor: "pointer" } }))),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Accordion, { style: { margin: '0 0.2em' } },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.AccordionSummary, { expandIcon: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_ExpandMoreRounded__WEBPACK_IMPORTED_MODULE_9__["default"], null), "aria-controls": "panel1a-content" },
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "subtitle2", style: { color: this.state.proxyUrl ? 'green' : 'red' } },
                                    "Proxy URL: ",
                                    this.state.proxyUrl ? 'Set' : 'Empty')),
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.AccordionDetails, null,
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "body2", gutterBottom: true }, this.state.proxyUrl ? 'Proxy URL is now: ' + this.state.proxyUrl : 'Unable to retrieve proxy URL from system settings.'))),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Accordion, { style: { margin: '0 0.2em' } },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.AccordionSummary, { expandIcon: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_ExpandMoreRounded__WEBPACK_IMPORTED_MODULE_9__["default"], null), "aria-controls": "panel1a-content" },
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "subtitle2", style: { color: this.state.proxyStatus === 'healthy' ? 'green' : 'red' } },
                                    "Proxy status: ",
                                    this.state.proxyStatus === 'healthy' ? 'Available' : 'Unavailable')),
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.AccordionDetails, null,
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "body2", gutterBottom: true }, this.state.proxyStatus === 'healthy' ? 'Ready to apply transformer to proxy.' : 'Lose connection to proxy server!'))),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Accordion, { style: { margin: '0 0.2em' } },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.AccordionSummary, { expandIcon: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_ExpandMoreRounded__WEBPACK_IMPORTED_MODULE_9__["default"], null), "aria-controls": "panel1a-content" },
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "subtitle2", style: { color: this.state.transformerNotebookPath ? 'green' : 'red' } },
                                    "Transformer NB: ",
                                    this.state.transformerNotebookPath ? 'Set' : 'Unknown')),
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.AccordionDetails, null,
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
                                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Select, { value: this.state.transformerNotebookPath, onChange: e => this.changetransformerNotebookPath(e.target.value) }, this.state.transformerNotebookPathOptions.map((value) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.MenuItem, { key: value, value: value }, value)))),
                                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "body2", display: "block", gutterBottom: true }, this.state.transformerNotebookPath ? 'Notebook(' + this.state.transformerNotebookPath + ') will be applied.' : 'Notebook transformer.ipynb is not found!'))))),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-component' + (this.state.isEnabled ? '' : ' hidden'), style: { marginTop: '1em' } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Divider, { variant: "middle", style: { margin: '1em 0' } }),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "subtitle2", display: "block", gutterBottom: true },
                            "APPLY TRANSFORMER",
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_Info__WEBPACK_IMPORTED_MODULE_10__["default"], { onClick: () => this.setState({
                                    showApplyTransformerDescription: !this.state.showApplyTransformerDescription
                                }), "aria-label": "show more", style: { position: "relative", top: "0.25em", margin: "0 0.2em", cursor: "pointer" } })),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Collapse, { in: this.state.showApplyTransformerDescription, timeout: "auto", unmountOnExit: true },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "body1", gutterBottom: true, style: { color: _theme__WEBPACK_IMPORTED_MODULE_7__.theme.transformer.headers.main } },
                                "Convert ",
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("strong", { style: { fontWeight: '600' } }, "transformer.ipynb"),
                                " to runnable handlers and apply them on proxy.")),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "input-container add-button" },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Button, { variant: "contained", color: "primary", size: "small", title: "Apply the changes.", onClick: this.applyTransformerToProxy, disabled: false }, "Now Apply"))),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'transformer-component' + (this.state.isEnabled ? '' : ' hidden'), style: { marginTop: '1em' } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Divider, { variant: "middle", style: { margin: '1em 0' } }),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "subtitle2", display: "block", gutterBottom: true },
                            "RESET TRANSFORMER",
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_icons_Info__WEBPACK_IMPORTED_MODULE_10__["default"], { onClick: () => this.setState({
                                    showResetTransformerDescription: !this.state.showResetTransformerDescription
                                }), "aria-label": "show more", style: { position: "relative", top: "0.25em", margin: "0 0.2em", cursor: "pointer" } })),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Collapse, { in: this.state.showResetTransformerDescription, timeout: "auto", unmountOnExit: true },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "body1", gutterBottom: true, style: { color: _theme__WEBPACK_IMPORTED_MODULE_7__.theme.transformer.headers.main } },
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("strong", { style: { fontWeight: '600' } },
                                    "Reset ",
                                    this.state.transformerNotebookPath ? this.state.transformerNotebookPath : 'transformer.ipynb'),
                                react__WEBPACK_IMPORTED_MODULE_0__.createElement("br", null),
                                "This action also reset the API handlers on proxy.")),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "input-container add-button" },
                            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Button, { variant: "contained", color: "secondary", size: "small", title: "Reset Transformer", onClick: this.resetTransformer, disabled: false }, "Now Reset"))))),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Dialog, { open: this.state.isDialogVisible, fullWidth: true, maxWidth: 'sm', scroll: "paper", "aria-labelledby": "scroll-dialog-title", "aria-describedby": "scroll-dialog-description" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.DialogTitle, { id: "scroll-dialog-title" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: 'dialog-title' }, this.state.dialogTitle)),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.DialogContent, { dividers: true },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, this.state.dialogContent)),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.DialogActions, null,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Button, { className: 'transformer-dialog ' + (this.state.isDialogConfirmButtonVisible ? '' : 'hidden'), color: "secondary", onClick: this.state.dialogConfirmClickHandler }, "Confirm"),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_1__.Button, { className: 'transformer-dialog ' + (this.state.isDialogCloseButtonVisible ? '' : 'hidden'), color: "primary", onClick: this.onDialogCloseClick }, this.state.closeButtonText)))));
    }
}


/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/interopRequireDefault.js":
/*!**********************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/interopRequireDefault.js ***!
  \**********************************************************************/
/***/ ((module) => {

function _interopRequireDefault(obj) {
  return obj && obj.__esModule ? obj : {
    "default": obj
  };
}

module.exports = _interopRequireDefault, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/interopRequireWildcard.js":
/*!***********************************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/interopRequireWildcard.js ***!
  \***********************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var _typeof = (__webpack_require__(/*! ./typeof.js */ "./node_modules/@babel/runtime/helpers/typeof.js")["default"]);

function _getRequireWildcardCache(nodeInterop) {
  if (typeof WeakMap !== "function") return null;
  var cacheBabelInterop = new WeakMap();
  var cacheNodeInterop = new WeakMap();
  return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) {
    return nodeInterop ? cacheNodeInterop : cacheBabelInterop;
  })(nodeInterop);
}

function _interopRequireWildcard(obj, nodeInterop) {
  if (!nodeInterop && obj && obj.__esModule) {
    return obj;
  }

  if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") {
    return {
      "default": obj
    };
  }

  var cache = _getRequireWildcardCache(nodeInterop);

  if (cache && cache.has(obj)) {
    return cache.get(obj);
  }

  var newObj = {};
  var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor;

  for (var key in obj) {
    if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) {
      var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null;

      if (desc && (desc.get || desc.set)) {
        Object.defineProperty(newObj, key, desc);
      } else {
        newObj[key] = obj[key];
      }
    }
  }

  newObj["default"] = obj;

  if (cache) {
    cache.set(obj, newObj);
  }

  return newObj;
}

module.exports = _interopRequireWildcard, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ "./node_modules/@babel/runtime/helpers/typeof.js":
/*!*******************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/typeof.js ***!
  \*******************************************************/
/***/ ((module) => {

function _typeof(obj) {
  "@babel/helpers - typeof";

  return (module.exports = _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) {
    return typeof obj;
  } : function (obj) {
    return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
  }, module.exports.__esModule = true, module.exports["default"] = module.exports), _typeof(obj);
}

module.exports = _typeof, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ "./node_modules/@material-ui/icons/Check.js":
/*!**************************************************!*\
  !*** ./node_modules/@material-ui/icons/Check.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ "./node_modules/@babel/runtime/helpers/interopRequireDefault.js");

var _interopRequireWildcard = __webpack_require__(/*! @babel/runtime/helpers/interopRequireWildcard */ "./node_modules/@babel/runtime/helpers/interopRequireWildcard.js");

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var React = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _createSvgIcon = _interopRequireDefault(__webpack_require__(/*! ./utils/createSvgIcon */ "./node_modules/@material-ui/icons/utils/createSvgIcon.js"));

var _default = (0, _createSvgIcon.default)( /*#__PURE__*/React.createElement("path", {
  d: "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
}), 'Check');

exports["default"] = _default;

/***/ }),

/***/ "./node_modules/@material-ui/icons/Close.js":
/*!**************************************************!*\
  !*** ./node_modules/@material-ui/icons/Close.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ "./node_modules/@babel/runtime/helpers/interopRequireDefault.js");

var _interopRequireWildcard = __webpack_require__(/*! @babel/runtime/helpers/interopRequireWildcard */ "./node_modules/@babel/runtime/helpers/interopRequireWildcard.js");

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var React = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _createSvgIcon = _interopRequireDefault(__webpack_require__(/*! ./utils/createSvgIcon */ "./node_modules/@material-ui/icons/utils/createSvgIcon.js"));

var _default = (0, _createSvgIcon.default)( /*#__PURE__*/React.createElement("path", {
  d: "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
}), 'Close');

exports["default"] = _default;

/***/ }),

/***/ "./node_modules/@material-ui/icons/ExpandMoreRounded.js":
/*!**************************************************************!*\
  !*** ./node_modules/@material-ui/icons/ExpandMoreRounded.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ "./node_modules/@babel/runtime/helpers/interopRequireDefault.js");

var _interopRequireWildcard = __webpack_require__(/*! @babel/runtime/helpers/interopRequireWildcard */ "./node_modules/@babel/runtime/helpers/interopRequireWildcard.js");

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var React = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _createSvgIcon = _interopRequireDefault(__webpack_require__(/*! ./utils/createSvgIcon */ "./node_modules/@material-ui/icons/utils/createSvgIcon.js"));

var _default = (0, _createSvgIcon.default)( /*#__PURE__*/React.createElement("path", {
  d: "M15.88 9.29L12 13.17 8.12 9.29a.9959.9959 0 00-1.41 0c-.39.39-.39 1.02 0 1.41l4.59 4.59c.39.39 1.02.39 1.41 0l4.59-4.59c.39-.39.39-1.02 0-1.41-.39-.38-1.03-.39-1.42 0z"
}), 'ExpandMoreRounded');

exports["default"] = _default;

/***/ }),

/***/ "./node_modules/@material-ui/icons/Info.js":
/*!*************************************************!*\
  !*** ./node_modules/@material-ui/icons/Info.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ "./node_modules/@babel/runtime/helpers/interopRequireDefault.js");

var _interopRequireWildcard = __webpack_require__(/*! @babel/runtime/helpers/interopRequireWildcard */ "./node_modules/@babel/runtime/helpers/interopRequireWildcard.js");

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var React = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _createSvgIcon = _interopRequireDefault(__webpack_require__(/*! ./utils/createSvgIcon */ "./node_modules/@material-ui/icons/utils/createSvgIcon.js"));

var _default = (0, _createSvgIcon.default)( /*#__PURE__*/React.createElement("path", {
  d: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
}), 'Info');

exports["default"] = _default;

/***/ }),

/***/ "./node_modules/@material-ui/icons/Refresh.js":
/*!****************************************************!*\
  !*** ./node_modules/@material-ui/icons/Refresh.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ "./node_modules/@babel/runtime/helpers/interopRequireDefault.js");

var _interopRequireWildcard = __webpack_require__(/*! @babel/runtime/helpers/interopRequireWildcard */ "./node_modules/@babel/runtime/helpers/interopRequireWildcard.js");

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var React = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _createSvgIcon = _interopRequireDefault(__webpack_require__(/*! ./utils/createSvgIcon */ "./node_modules/@material-ui/icons/utils/createSvgIcon.js"));

var _default = (0, _createSvgIcon.default)( /*#__PURE__*/React.createElement("path", {
  d: "M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
}), 'Refresh');

exports["default"] = _default;

/***/ }),

/***/ "./node_modules/@material-ui/icons/utils/createSvgIcon.js":
/*!****************************************************************!*\
  !*** ./node_modules/@material-ui/icons/utils/createSvgIcon.js ***!
  \****************************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
Object.defineProperty(exports, "default", ({
  enumerable: true,
  get: function get() {
    return _utils.createSvgIcon;
  }
}));

var _utils = __webpack_require__(/*! @material-ui/core/utils */ "./node_modules/@material-ui/core/esm/utils/index.js");

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;;;;CAIC","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _icons_toolbar_tree_view_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./icons/toolbar/tree-view.svg */ "./style/icons/toolbar/tree-view.svg");
/* harmony import */ var _icons_toolbar_tree_view_svg__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_icons_toolbar_tree_view_svg__WEBPACK_IMPORTED_MODULE_4__);
// Imports





var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3___default()((_icons_toolbar_tree_view_svg__WEBPACK_IMPORTED_MODULE_4___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".transformer-logo {\n    background-image: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ");\n}\n\n.leftpanel-transformer-widget {\n    flex-direction: column;\n    min-width: var(--jp-sidebar-min-width);\n    color: var(--jp-ui-font-color1);\n    background: var(--jp-layout-color1);\n    font-size: var(--jp-ui-font-size1);\n    overflow: auto;\n    height: 100%;\n    display: -webkit-box; /* OLD - iOS 6-, Safari 3.1-6 */\n    display: -moz-box; /* OLD - Firefox 19- (buggy but mostly works) */\n    display: -ms-flexbox; /* TWEENER - IE 10 */\n    display: -webkit-flex; /* NEW - Chrome */\n    display: flex;\n}\n\n.leftpanel-transformer-widget-content {\n    min-width: var(--jp-sidebar-min-width);\n    /* height: calc(100% - 42px); */\n    overflow: auto;\n    /* border-bottom: 1px solid var(--jp-border-color2); */\n}\n\n.transformer-component.hidden {\n    display: none !important;\n}\n\n.transformer-metadata-editor-wrapper,\n.transformer-inline-cell-metadata {\n  /* FIXME: find a way to calculate margin */\n  margin-left: 73px;\n  margin-top: 8px;\n  margin-bottom: 4px;\n  display: flex;\n  align-items: center;\n}\n\n.transformer-inline-cell-metadata {\n    position: absolute;\n    top: -40px;\n}\n.transformer-metadata-editor-wrapper {\n    display: inline-block;\n    position: absolute;\n    top: -60px;\n}\n\n.transformer-inline-cell-metadata.hidden,\n.transformer-metadata-editor-wrapper.hidden,\n.transformer-cell-metadata-editor.hidden {\n    display: none !important;\n}\n\n.transformer-metadata-editor-wrapper .transformer-cell-metadata-editor button {\n    padding: 8px;\n}\n\n.jp-Toolbar-item button[data-command=\"notebook:transformer\"]:disabled { \n    display: none;\n}\n\n.jp-Cell.with-transformer-editor {\n    margin-top: 52px;\n}\n.jp-Cell.with-transformer-chip {\n    margin-top: 38px;\n}\n\n.dialog-code-snippet {\n    padding: 0.8em 0.4em;\n    background-color: lightyellow;\n}\n\n.dialog-code-snippet.hidden {\n    display: none !important;\n}\n\nbutton.transformer-dialog.hidden {\n    display: none !important;\n}\n", "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAEA;IACI,yDAAoD;AACxD;;AAEA;IACI,sBAAsB;IACtB,sCAAsC;IACtC,+BAA+B;IAC/B,mCAAmC;IACnC,kCAAkC;IAClC,cAAc;IACd,YAAY;IACZ,oBAAoB,EAAE,+BAA+B;IACrD,iBAAiB,EAAE,+CAA+C;IAClE,oBAAoB,EAAE,oBAAoB;IAC1C,qBAAqB,EAAE,iBAAiB;IACxC,aAAa;AACjB;;AAEA;IACI,sCAAsC;IACtC,+BAA+B;IAC/B,cAAc;IACd,sDAAsD;AAC1D;;AAEA;IACI,wBAAwB;AAC5B;;AAEA;;EAEE,0CAA0C;EAC1C,iBAAiB;EACjB,eAAe;EACf,kBAAkB;EAClB,aAAa;EACb,mBAAmB;AACrB;;AAEA;IACI,kBAAkB;IAClB,UAAU;AACd;AACA;IACI,qBAAqB;IACrB,kBAAkB;IAClB,UAAU;AACd;;AAEA;;;IAGI,wBAAwB;AAC5B;;AAEA;IACI,YAAY;AAChB;;AAEA;IACI,aAAa;AACjB;;AAEA;IACI,gBAAgB;AACpB;AACA;IACI,gBAAgB;AACpB;;AAEA;IACI,oBAAoB;IACpB,6BAA6B;AACjC;;AAEA;IACI,wBAAwB;AAC5B;;AAEA;IACI,wBAAwB;AAC5B","sourcesContent":["@import url('base.css');\n\n.transformer-logo {\n    background-image: url('icons/toolbar/tree-view.svg');\n}\n\n.leftpanel-transformer-widget {\n    flex-direction: column;\n    min-width: var(--jp-sidebar-min-width);\n    color: var(--jp-ui-font-color1);\n    background: var(--jp-layout-color1);\n    font-size: var(--jp-ui-font-size1);\n    overflow: auto;\n    height: 100%;\n    display: -webkit-box; /* OLD - iOS 6-, Safari 3.1-6 */\n    display: -moz-box; /* OLD - Firefox 19- (buggy but mostly works) */\n    display: -ms-flexbox; /* TWEENER - IE 10 */\n    display: -webkit-flex; /* NEW - Chrome */\n    display: flex;\n}\n\n.leftpanel-transformer-widget-content {\n    min-width: var(--jp-sidebar-min-width);\n    /* height: calc(100% - 42px); */\n    overflow: auto;\n    /* border-bottom: 1px solid var(--jp-border-color2); */\n}\n\n.transformer-component.hidden {\n    display: none !important;\n}\n\n.transformer-metadata-editor-wrapper,\n.transformer-inline-cell-metadata {\n  /* FIXME: find a way to calculate margin */\n  margin-left: 73px;\n  margin-top: 8px;\n  margin-bottom: 4px;\n  display: flex;\n  align-items: center;\n}\n\n.transformer-inline-cell-metadata {\n    position: absolute;\n    top: -40px;\n}\n.transformer-metadata-editor-wrapper {\n    display: inline-block;\n    position: absolute;\n    top: -60px;\n}\n\n.transformer-inline-cell-metadata.hidden,\n.transformer-metadata-editor-wrapper.hidden,\n.transformer-cell-metadata-editor.hidden {\n    display: none !important;\n}\n\n.transformer-metadata-editor-wrapper .transformer-cell-metadata-editor button {\n    padding: 8px;\n}\n\n.jp-Toolbar-item button[data-command=\"notebook:transformer\"]:disabled { \n    display: none;\n}\n\n.jp-Cell.with-transformer-editor {\n    margin-top: 52px;\n}\n.jp-Cell.with-transformer-chip {\n    margin-top: 38px;\n}\n\n.dialog-code-snippet {\n    padding: 0.8em 0.4em;\n    background-color: lightyellow;\n}\n\n.dialog-code-snippet.hidden {\n    display: none !important;\n}\n\nbutton.transformer-dialog.hidden {\n    display: none !important;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/getUrl.js":
/*!********************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/getUrl.js ***!
  \********************************************************/
/***/ ((module) => {

"use strict";


module.exports = function (url, options) {
  if (!options) {
    // eslint-disable-next-line no-param-reassign
    options = {};
  } // eslint-disable-next-line no-underscore-dangle, no-param-reassign


  url = url && url.__esModule ? url.default : url;

  if (typeof url !== "string") {
    return url;
  } // If url is already wrapped in quotes, remove them


  if (/^['"].*['"]$/.test(url)) {
    // eslint-disable-next-line no-param-reassign
    url = url.slice(1, -1);
  }

  if (options.hash) {
    // eslint-disable-next-line no-param-reassign
    url += options.hash;
  } // Should url be wrapped?
  // See https://drafts.csswg.org/css-values-3/#urls


  if (/["'() \t\n]/.test(url) || options.needQuotes) {
    return "\"".concat(url.replace(/"/g, '\\"').replace(/\n/g, "\\n"), "\"");
  }

  return url;
};

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./style/icons/toolbar/tree-view.svg":
/*!*******************************************!*\
  !*** ./style/icons/toolbar/tree-view.svg ***!
  \*******************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3Csvg height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'%3E %3Cg class='jp-icon3' fill='%23616161'%3E %3Cpath d='M0 0h24v24H0z' fill='none'/%3E %3Cpath d='M22 11V3h-7v3H9V3H2v8h7V8h2v10h4v3h7v-8h-7v3h-2V8h2v3z'/%3E %3C/g%3E %3C/svg%3E"

/***/ })

}]);
//# sourceMappingURL=lib_index_js.5ce47f5b3a1fc912f3d4.js.map