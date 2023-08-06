"use strict";
(self["webpackChunk_g2nb_jupyter_wysiwyg"] = self["webpackChunk_g2nb_jupyter_wysiwyg"] || []).push([["lib_editor_js-lib_factory_js"],{

/***/ "./lib/editor.js":
/*!***********************!*\
  !*** ./lib/editor.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TinyMCEEditor": () => (/* binding */ TinyMCEEditor),
/* harmony export */   "TinyMCEView": () => (/* binding */ TinyMCEView)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./factory */ "./lib/factory.js");
/* harmony import */ var tinymce__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! tinymce */ "webpack/sharing/consume/default/tinymce/tinymce");
/* harmony import */ var tinymce__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(tinymce__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var tinymce_icons_default__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! tinymce/icons/default */ "./node_modules/tinymce/icons/default/index.js");
/* harmony import */ var tinymce_icons_default__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(tinymce_icons_default__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var tinymce_themes_silver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! tinymce/themes/silver */ "./node_modules/tinymce/themes/silver/index.js");
/* harmony import */ var tinymce_themes_silver__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(tinymce_themes_silver__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var tinymce_skins_ui_oxide_skin_css__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! tinymce/skins/ui/oxide/skin.css */ "./node_modules/tinymce/skins/ui/oxide/skin.css");
/* harmony import */ var tinymce_plugins_advlist__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! tinymce/plugins/advlist */ "./node_modules/tinymce/plugins/advlist/index.js");
/* harmony import */ var tinymce_plugins_advlist__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(tinymce_plugins_advlist__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var tinymce_plugins_code__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! tinymce/plugins/code */ "./node_modules/tinymce/plugins/code/index.js");
/* harmony import */ var tinymce_plugins_code__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(tinymce_plugins_code__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var tinymce_plugins_emoticons__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! tinymce/plugins/emoticons */ "./node_modules/tinymce/plugins/emoticons/index.js");
/* harmony import */ var tinymce_plugins_emoticons__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(tinymce_plugins_emoticons__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var tinymce_plugins_emoticons_js_emojis__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! tinymce/plugins/emoticons/js/emojis */ "./node_modules/tinymce/plugins/emoticons/js/emojis.js");
/* harmony import */ var tinymce_plugins_emoticons_js_emojis__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(tinymce_plugins_emoticons_js_emojis__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var tinymce_plugins_link__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! tinymce/plugins/link */ "./node_modules/tinymce/plugins/link/index.js");
/* harmony import */ var tinymce_plugins_link__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(tinymce_plugins_link__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var tinymce_plugins_lists__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! tinymce/plugins/lists */ "./node_modules/tinymce/plugins/lists/index.js");
/* harmony import */ var tinymce_plugins_lists__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(tinymce_plugins_lists__WEBPACK_IMPORTED_MODULE_15__);
/* harmony import */ var tinymce_plugins_table__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! tinymce/plugins/table */ "./node_modules/tinymce/plugins/table/index.js");
/* harmony import */ var tinymce_plugins_table__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(tinymce_plugins_table__WEBPACK_IMPORTED_MODULE_16__);






// Import TinyMCE

 // Default icons are required for TinyMCE 5.3 or above
 // A theme is also required
 // Import the skin
 // Import plugins






// import contentUiCss from 'tinymce/skins/ui/oxide/content.css'; // Import content CSS
// import contentCss from 'tinymce/skins/content/default/content.css';
class TinyMCEEditor {
    constructor(options, markdownModel) {
        this._uuid = '';
        this._is_disposed = false;
        this._keydownHandlers = new Array();
        this.is_markdown = false;
        this.edgeRequested = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this.host = options.host;
        this.host.classList.add("jp-RenderedHTMLCommon");
        this.host.classList.add('jp-TinyMCE');
        this.host.addEventListener('focus', this.blur, true);
        this.host.addEventListener('blur', this.focus, true);
        this.host.addEventListener('scroll', this.scroll, true);
        this._uuid = options.uuid || _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
        this._model = options.model;
        this.is_markdown = markdownModel.metadata.get("markdownMode");
        if (!!this.is_markdown)
            this.is_markdown = false;
        this._view = new TinyMCEView(this.host, this.model);
    }
    // Getters
    get view() { return this._view; }
    get uuid() { return this._uuid; }
    get is_disposed() { return this._is_disposed; }
    get model() { return this._model; }
    get lineCount() { return TinyMCEEditor.DEFAULT_NUMBER; }
    get selectionStyle() { return this._selection_style; }
    // Setters
    set uuid(value) { this._uuid = value; }
    set selectionStyle(value) { this._selection_style = value; }
    blur() { if (this._view)
        this._view.blur(); }
    focus() { if (this._view)
        this._view.focus(); }
    addKeydownHandler(handler) {
        this._keydownHandlers.push(handler);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_3__.DisposableDelegate(() => {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.ArrayExt.removeAllWhere(this._keydownHandlers, val => val === handler);
        });
    }
    dispose() {
        if (this._is_disposed)
            return;
        this._is_disposed = true;
        this.host.removeEventListener('focus', this.focus, true);
        this.host.removeEventListener('focus', this.blur, true);
        this.host.removeEventListener('focus', this.scroll, true);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    // Called when a markdown cell is either first rendered or toggled into editor mode
    refresh() {
        const active_cell = _factory__WEBPACK_IMPORTED_MODULE_5__.EditorWidget.instance().tracker.activeCell;
        if (active_cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCell && !active_cell.rendered && _factory__WEBPACK_IMPORTED_MODULE_5__.EditorWidget.instance().no_side_button()) {
            active_cell.editor.focus();
            _factory__WEBPACK_IMPORTED_MODULE_5__.EditorWidget.instance().render_side_button();
        }
    }
    // This is a dummy implementation that prevents an error in the console
    getCursorPosition() {
        return new class {
        }();
    }
    // Empty stubs necessary to implement CodeEditor.IEditor, full integration may require implementing these methods
    clearHistory() { }
    scroll() { }
    getCoordinateForPosition(position) { return undefined; }
    getLine(line) { return undefined; }
    getOffsetAt(position) { return 0; }
    getOption(option) { return undefined; }
    getPositionAt(offset) { return undefined; }
    getPositionForCoordinate(coordinate) { return undefined; }
    getSelection() { return undefined; }
    getSelections() { return []; }
    getTokenForPosition(position) { return undefined; }
    getTokens() { return []; }
    hasFocus() { return false; }
    newIndentedLine() { }
    redo() { }
    resizeToFit() { }
    revealPosition(position) { }
    revealSelection(selection) { }
    setCursorPosition(position) { }
    setOption(option, value) { }
    setOptions(options) { }
    setSelection(selection) { }
    setSelections(selections) { }
    setSize(size) { }
    undo() { }
}
TinyMCEEditor.DEFAULT_NUMBER = 0;
class TinyMCEView {
    constructor(host, model) {
        // Create the wrapper for TinyMCE
        const wrapper = document.createElement("div");
        host.appendChild(wrapper);
        // Wait for cell initialization before initializing editor
        setTimeout(() => {
            var _a;
            // Special case to remove anchor links before loading
            const render_node = (_a = host === null || host === void 0 ? void 0 : host.parentElement) === null || _a === void 0 ? void 0 : _a.querySelector('.jp-MarkdownOutput');
            if (render_node)
                render_node.querySelectorAll('.jp-InternalAnchorLink').forEach(e => e.remove());
            wrapper.innerHTML = (render_node === null || render_node === void 0 ? void 0 : render_node.innerHTML) || model.value.text;
            try {
                tinymce__WEBPACK_IMPORTED_MODULE_6___default().init({
                    target: wrapper,
                    skin: false,
                    content_css: false,
                    // content_style: contentUiCss.toString() + '\n' + contentCss.toString(),
                    branding: false,
                    contextmenu: false,
                    elementpath: false,
                    menubar: false,
                    height: 300,
                    resize: false,
                    plugins: 'emoticons lists link code',
                    toolbar: 'styleselect fontsizeselect | bold italic underline strikethrough | subscript superscript | link forecolor backcolor emoticons | bullist numlist outdent indent blockquote | code',
                    init_instance_callback: (editor) => editor.on('Change', () => model.value.text = editor.getContent())
                }).then(editor => {
                    if (!editor.length)
                        return; // If no valid editors, do nothing
                    editor[0].on("focus", () => {
                        const index = this.get_cell_index(model);
                        if (index !== null)
                            _factory__WEBPACK_IMPORTED_MODULE_5__.EditorWidget.instance().tracker.currentWidget.content.activeCellIndex = index;
                    });
                });
            }
            catch (e) {
                console.log("TinyMCE threw an error: " + e);
            }
        }, 500);
    }
    blur() { }
    focus() { }
    get_cell_index(model) {
        const id = model.modelDB.basePath;
        const all_cells = _factory__WEBPACK_IMPORTED_MODULE_5__.EditorWidget.instance().tracker.currentWidget.content.widgets;
        for (let i = 0; i < all_cells.length; i++) {
            const cell = all_cells[i];
            const cell_id = cell.model.modelDB.basePath;
            if (id === cell_id)
                return i;
        }
        return null;
    }
}


/***/ }),

/***/ "./lib/factory.js":
/*!************************!*\
  !*** ./lib/factory.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditorContentFactory": () => (/* binding */ EditorContentFactory),
/* harmony export */   "IEditorContentFactory": () => (/* binding */ IEditorContentFactory),
/* harmony export */   "EditorWidget": () => (/* binding */ EditorWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./editor */ "./lib/editor.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);






class EditorContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
    constructor(options) {
        super(options);
    }
    /**
     * Create a markdown cell with the WYSIWYG editor rather than CodeMirror
     *
     * @param options
     * @param parent
     */
    createMarkdownCell(options, parent) {
        const model = options.model;
        options.contentFactory = new EditorContentFactory({
            editorFactory: (options) => {
                return new _editor__WEBPACK_IMPORTED_MODULE_4__.TinyMCEEditor(options, model);
            }
        });
        return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.MarkdownCell(options).initializeState();
    }
}
const IEditorContentFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.Token("jupyter-wysiwyg");
class EditorWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor() {
        super();
    }
    static instance() {
        // Instantiate if necessary
        if (!EditorWidget._singleton)
            EditorWidget._singleton = new EditorWidget();
        return EditorWidget._singleton;
    }
    get tracker() {
        return this._tracker;
    }
    set tracker(tracker) {
        this._tracker = tracker;
    }
    get previous_cell() {
        return this._previous_cell;
    }
    set previous_cell(_previous_cell) {
        this._previous_cell = _previous_cell;
    }
    no_side_button() {
        var _a;
        return !((_a = this.sidebar(this._tracker.activeCell.node)) === null || _a === void 0 ? void 0 : _a.querySelector('.jp-RenderButton'));
    }
    render_side_button() {
        const sidebar = this.sidebar(this._tracker.activeCell.node);
        const run_button = this.run_button(this._tracker.activeCell, this._tracker.currentWidget);
        sidebar.append(run_button);
    }
    remove_side_button() {
        var _a;
        if (this._previous_cell) {
            const sidebar = this.sidebar(this._previous_cell.node);
            (_a = sidebar.querySelector(".jp-RenderButton")) === null || _a === void 0 ? void 0 : _a.remove();
        }
        this._previous_cell = this._tracker.activeCell;
    }
    sidebar(node) {
        var _a;
        return (_a = node.closest('.jp-Cell')) === null || _a === void 0 ? void 0 : _a.querySelector('.jp-InputArea-prompt');
    }
    run_button(cell, panel) {
        const button = document.createElement("button");
        button.classList.add("jp-ToolbarButtonComponent", "jp-Button", "jp-RenderButton");
        button.setAttribute("title", "Render this cell");
        button.innerHTML = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.runIcon.svgstr;
        button.addEventListener("click", () => {
            panel.content.select(cell);
            setTimeout(() => void _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.runAndAdvance(panel.content, panel.sessionContext), 200);
        });
        return button;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_editor_js-lib_factory_js.d5455cdffb44eb06174c.js.map