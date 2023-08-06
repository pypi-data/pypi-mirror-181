"use strict";
(self["webpackChunk_g2nb_jupyter_wysiwyg"] = self["webpackChunk_g2nb_jupyter_wysiwyg"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MODULE_NAME": () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_0__.MODULE_NAME),
/* harmony export */   "MODULE_VERSION": () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_0__.MODULE_VERSION),
/* harmony export */   "EditorContentFactory": () => (/* reexport safe */ _factory__WEBPACK_IMPORTED_MODULE_1__.EditorContentFactory),
/* harmony export */   "EditorWidget": () => (/* reexport safe */ _factory__WEBPACK_IMPORTED_MODULE_1__.EditorWidget),
/* harmony export */   "IEditorContentFactory": () => (/* reexport safe */ _factory__WEBPACK_IMPORTED_MODULE_1__.IEditorContentFactory),
/* harmony export */   "TinyMCEEditor": () => (/* reexport safe */ _editor__WEBPACK_IMPORTED_MODULE_2__.TinyMCEEditor),
/* harmony export */   "TinyMCEView": () => (/* reexport safe */ _editor__WEBPACK_IMPORTED_MODULE_2__.TinyMCEView)
/* harmony export */ });
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./factory */ "./lib/factory.js");
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./editor */ "./lib/editor.js");
// Copyright (c) 2021 Regents of the University of California & the Broad Institute
// Distributed under the terms of the Modified BSD License.





/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MODULE_VERSION": () => (/* binding */ MODULE_VERSION),
/* harmony export */   "MODULE_NAME": () => (/* binding */ MODULE_NAME)
/* harmony export */ });
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
const MODULE_VERSION = data.version;
/*
 * The current package name.
 */
const MODULE_NAME = data.name;


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"@g2nb/jupyter-wysiwyg","version":"22.12.0-beta.1","description":"WYSIWYG editing functionality for markdown/HTML cells in Jupyter","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.{js,css}","style/*.{js,css,png,svg}","dist/*.{js,css}","style/index.js"],"homepage":"https://github.com/g2nb/jupyter-wysiwyg","bugs":{"url":"https://github.com/g2nb/jupyter-wysiwyg/issues"},"license":"BSD-3-Clause","author":{"name":"Thorin Tabor","email":"tmtabor@cloud.ucsd.edu"},"main":"lib/index.js","types":"./lib/index.d.ts","style":"style/index.css","repository":{"type":"git","url":"https://github.com/g2nb/jupyter-wysiwyg"},"scripts":{"build":"jlpm run build:lib && jlpm run build:labextension:dev","build:all":"jlpm run build:lib && jlpm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","clean":"jlpm run clean:lib","clean:all":"jlpm run clean:lib && jlpm run clean:labextension","clean:labextension":"rimraf jupyter-wysiwyg/labextension","clean:lib":"rimraf lib tsconfig.tsbuildinfo","eslint":"eslint . --ext .ts,.tsx --fix","eslint:check":"eslint . --ext .ts,.tsx","install:extension":"jlpm run build","prepack":"jlpm run build:lib","prepare":"jlpm run clean && jlpm run build:all","test":"jlpm run test:firefox","test:chrome":"karma start --browsers=Chrome tests/karma.conf.js","test:debug":"karma start --browsers=Chrome --singleRun=false --debug=true tests/karma.conf.js","test:firefox":"karma start --browsers=Firefox tests/karma.conf.js","test:ie":"karma start --browsers=IE tests/karma.conf.js","watch":"run-p watch:src watch:labextension","watch:labextension":"jupyter labextension watch .","watch:lib":"tsc -w","watch:src":"tsc -w"},"dependencies":{"@jupyter-widgets/base":"^4.0.0","@jupyterlab/application":"^3.3.0","@jupyterlab/mainmenu":"^3.3.0","@jupyterlab/notebook":"^3.3.0","tinymce":"^5.9.2"},"devDependencies":{"@jupyterlab/apputils":"3.2.9","@jupyterlab/builder":"^3.3.0","@jupyterlab/codeeditor":"3.2.9","@jupyterlab/ui-components":"3.2.9","@lumino/application":"1.28.1","@lumino/widgets":"1.31.1","@types/backbone":"^1.4.4","@types/node":"^14.14.27","@typescript-eslint/eslint-plugin":"^4.8.1","@typescript-eslint/parser":"^4.8.1","backbone":"^1.2.3","css-loader":"^5.0.2","eslint":"^7.14.0","expect.js":"^0.3.1","file-loader":"^6.2.0","fs-extra":"^9.1.0","karma":"^6.1.1","karma-typescript":"^5.3.0","mkdirp":"^1.0.4","mocha":"^8.3.0","npm-run-all":"^4.1.5","rimraf":"^3.0.2","source-map-loader":"^2.0.1","style-loader":"^2.0.0","ts-loader":"^8.0.17","typescript":"~4.1.3","webpack":"^5.21.2","webpack-cli":"^4.5.0"},"jupyterlab":{"extension":"lib/plugin","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}},"discovery":{"kernel":[{"kernel_spec":{"language":"^python"},"base":{"name":"jupyter-wysiwyg"},"managers":["pip","conda"]}]},"outputDir":"jupyter-wysiwyg/labextension"},"styleModule":"style/index.js"}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.26c211cdf5957b515724.js.map