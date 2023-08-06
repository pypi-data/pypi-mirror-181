(self["webpackChunk_g2nb_nbtools"] = self["webpackChunk_g2nb_nbtools"] || []).push([["lib_registry_js-lib_uibuilder_js-lib_uioutput_js"],{

/***/ "./lib/basewidget.js":
/*!***************************!*\
  !*** ./lib/basewidget.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BaseWidgetModel": () => (/* binding */ BaseWidgetModel),
/* harmony export */   "BaseWidgetView": () => (/* binding */ BaseWidgetView)
/* harmony export */ });
/* harmony import */ var _style_basewidget_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../style/basewidget.css */ "./style/basewidget.css");
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _toolbox__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./toolbox */ "./lib/toolbox.js");






// noinspection JSAnnotator
class BaseWidgetModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_3__.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _id: '', origin: '', name: '', subtitle: '', description: '', collapsed: false, color: 'var(--jp-layout-color4)', logo: _context__WEBPACK_IMPORTED_MODULE_1__.ContextManager.context().default_logo(), info: '', error: '', extra_menu_items: {} });
    }
}
BaseWidgetModel.model_name = 'BaseWidgetModel';
BaseWidgetModel.model_module = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_NAME;
BaseWidgetModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_VERSION;
BaseWidgetModel.view_name = 'BaseWidgetView';
BaseWidgetModel.view_module = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_NAME;
BaseWidgetModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_VERSION;
BaseWidgetModel.serializers = Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_3__.DOMWidgetModel.serializers);
// noinspection JSAnnotator
class BaseWidgetView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_3__.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.dom_class = '';
        this.element = document.createElement('div');
        this.traitlets = ['name', 'subtitle', 'description', 'info', 'error'];
        this.renderers = {
            "description": this.render_description,
            "error": this.render_error,
            "info": this.render_info
        };
        this.template = `<div class="nbtools">
                           <div class="nbtools-header"></div>
                           <div class="nbtools-body"></div>
                       </div>`;
        this.header = `<img class="nbtools-logo" src="" />
                     <label class="nbtools-title" data-traitlet="name"></label>
                     <label class="nbtools-subtitle" data-traitlet="subtitle"></label>
                     <div class="nbtools-controls">
                         <button class="nbtools-collapse">
                             <span class="fa fa-minus"></span>
                         </button>
                         <button class="nbtools-gear">
                             <span class="fa fa-cog"></span>
                             <span class="fa fa-caret-down"></span>
                         </button>
                         <ul class="nbtools-menu" style="display: none;"></ul>
                     </div>`;
        this.body = `<div class="nbtools-description" data-traitlet="description"></div>
                   <div class="nbtools-error" data-traitlet="error"></div>
                   <div class="nbtools-info" data-traitlet="info"></div>`;
        this.disconnected = `<div class="nbtools-disconnected">
                               <div class="nbtools-panel">
                                   <div class="nbtools-header">Widget Disconnected From Kernel</div>
                                   <div class="nbtools-body">
                                       <p>You need to run this cell before it can connect to the notebook kernel. Please click the Connect to Kernel button below.</p>
                                       <div class="nbtools-connect nbtools-panel-button"><button class="nbtools-connect nbtools-panel-button">Connect to Kernel</button></div>
                                   </div>
                               </div>
                           </div>`;
    }
    render() {
        super.render();
        // Build the widget
        this.build();
        // Apply the color
        this.set_color();
        this.model.on('change:color', this.set_color, this);
        // Apply the logo
        this.set_logo();
        this.model.on('change:logo', this.set_logo, this);
        // Set the traitlet values
        this.traitlets.forEach(traitlet => this.traitlet_changed(traitlet));
        // Hook in the traitlet change events
        this.traitlets.forEach(traitlet => this.model.on(`change:${traitlet}`, this.traitlet_changed, this));
        // Hook in the expand / collapse events
        this.model.on('change:collapsed', this.toggle_collapse, this);
        if (this.model.get('collapsed'))
            this.toggle_collapse();
        // Hide the code
        this.toggle_code(false);
        // Attach the extra menu options
        this.attach_menu_options();
        this.model.on('change:extra_menu_items', this.attach_menu_options, this);
        // Allow menus to overflow the container
        this.float_menus();
        // Initialize the widget
        this.initialize({ options: {} });
        // Call any post render events
        this.post_render();
    }
    build() {
        // Parse the template
        this.element = new DOMParser().parseFromString(this.template, "text/html")
            .querySelector('div.nbtools');
        // Apply the DOM class
        if (this.dom_class)
            this.element.classList.add(this.dom_class);
        // Apply the header
        this.element.querySelector('div.nbtools-header').innerHTML = this.header;
        // Attach collapse event
        const collapse = this.element.querySelector("button.nbtools-collapse");
        collapse.addEventListener("click", () => {
            this.model.set('collapsed', !this.model.get('collapsed'));
            this.model.save_changes();
        });
        // Attach the gear event
        const gear = this.element.querySelector("button.nbtools-gear");
        gear.addEventListener("click", () => this.toggle_menu());
        // Attach toggle code event
        this.add_menu_item('Toggle Code View', () => this.toggle_code());
        // Apply the body
        this.element.querySelector('div.nbtools-body').innerHTML = this.body;
        // Attach the disconnected cover
        this.element.appendChild(new DOMParser().parseFromString(this.disconnected, "text/html")
            .querySelector('body > :first-child'));
        this.attach_connect_event();
        this.disconnected_sync_fix();
        // Set the element
        this.setElement(this.element);
    }
    set_logo() {
        // Get custom logo
        let logo = this.model.get('logo');
        const logo_element = this.element.querySelector("img.nbtools-logo");
        // Fall back to default logo if no custom logo is set
        if (!logo) {
            logo = _context__WEBPACK_IMPORTED_MODULE_1__.ContextManager.context().default_logo();
            this.model.set('logo', logo);
            this.model.save();
        }
        // Special case for "None" logo
        if (logo.toLowerCase() === "none")
            logo_element.classList.add('nbtools-logo-hidden');
        else
            logo_element.classList.remove('nbtools-logo-hidden');
        // Set the logo
        logo_element.src = logo;
    }
    set_color() {
        const color = this.model.get('color').trim();
        this.element.style.borderColor = color;
        this.element.querySelectorAll('.nbtools-body button, .nbtools-header').forEach((e) => {
            e.style.backgroundColor = color;
        });
    }
    render_description(description, widget) {
        return widget._render_or_hide('.nbtools-description', description, widget);
    }
    render_error(message, widget) {
        return widget._render_or_hide('.nbtools-error', message, widget);
    }
    render_info(message, widget) {
        return widget._render_or_hide('.nbtools-info', message, widget);
    }
    _render_or_hide(selector, message, widget) {
        widget.element.querySelector(selector).style.display = message.trim() ? 'block' : 'none';
        return message;
    }
    attach_connect_event() {
        const button = this.element.querySelector('button.nbtools-connect');
        button.addEventListener("click", () => {
            // Run all cells with disconnected nbtools widgets
            _context__WEBPACK_IMPORTED_MODULE_1__.ContextManager.context().run_tool_cells();
        });
    }
    disconnected_sync_fix() {
        // Fix a bug that can occur when a disconnected widget and a connected widget are somehow rendered in the same cell
        setTimeout(() => {
            const cell = this.element.closest('.jp-Cell, .cell');
            if (!cell)
                return; // No cell found, bug cannot occur
            // Do both connected and disconnected widgets appear in the cell?
            const contains_disconnected = !!cell.querySelectorAll('.nbtools.jupyter-widgets-disconnected').length;
            const contains_connected = !!cell.querySelectorAll('.nbtools:not(.jupyter-widgets-disconnected)').length;
            // If they do, hide the irrelevant disconnected widgets
            if (contains_disconnected && contains_connected) {
                cell.querySelectorAll('.nbtools.jupyter-widgets-disconnected').forEach((e) => {
                    e.style.display = 'none';
                });
            }
        }, 100);
    }
    add_menu_item(label, callback, dom_class = null, menu = null, prepend = true) {
        // Create the menu item
        const item = new DOMParser().parseFromString(`<li>${label}</li>`, "text/html")
            .querySelector('li');
        // Apply the class if one is specified
        if (dom_class)
            item.classList.add(dom_class);
        // Attach the menu item
        if (!menu)
            menu = this.element.querySelector('.nbtools-menu');
        if (prepend)
            menu.prepend(item);
        else
            menu.append(item);
        // Attach the click event
        item.addEventListener('click', () => callback());
        return item;
    }
    traitlet_changed(event) {
        const widget = this;
        const name = typeof event === "string" ? event : Object.keys(event.changed)[0];
        const elements = this.element.querySelectorAll(`[data-traitlet=${name}]`);
        elements.forEach(element => {
            if (name in this.renderers)
                element.innerHTML = this.renderers[name](this.model.get(name), widget);
            else
                element.innerHTML = this.model.get(name);
        });
    }
    toggle_code(display) {
        const element = this.element;
        _context__WEBPACK_IMPORTED_MODULE_1__.ContextManager.context().toggle_code(element, display);
    }
    toggle_collapse() {
        const body = this.element.querySelector(".nbtools-body");
        const collapsed = body.style.display === "none" || body.style.height == "0px";
        // Toggle the collapse button
        const button = this.element.querySelector(".nbtools-collapse > span");
        if (collapsed) {
            button.classList.add('fa-minus');
            button.classList.remove('fa-plus');
        }
        else {
            button.classList.remove('fa-minus');
            button.classList.add('fa-plus');
        }
        // Hide or show widget body
        (0,_utils__WEBPACK_IMPORTED_MODULE_2__.toggle)(body);
    }
    toggle_menu() {
        const gear = this.element.querySelector("button.nbtools-gear");
        const menu = this.element.querySelector(".nbtools-menu");
        const collapsed = menu.style.display === "none";
        // Hide or show the menu
        if (collapsed)
            menu.style.display = "block";
        else
            menu.style.display = "none";
        // Hide the menu with the next click
        const hide_next_click = function (event) {
            if (gear.contains(event.target))
                return;
            menu.style.display = "none";
            document.removeEventListener('click', hide_next_click);
        };
        document.addEventListener('click', hide_next_click);
    }
    create_menu_callback(item, template_vars = {}) {
        // Create callback for string literal
        if (typeof item === 'string')
            return new Function((0,_utils__WEBPACK_IMPORTED_MODULE_2__.process_template)(item, template_vars));
        // Create callback for javascript event type
        else if (item['action'] === 'javascript')
            return () => eval((0,_utils__WEBPACK_IMPORTED_MODULE_2__.process_template)(item['code'], template_vars));
        // Create callback for cell event type
        else if (item['action'] === 'cell')
            return () => _toolbox__WEBPACK_IMPORTED_MODULE_5__.Toolbox.add_code_cell((0,_utils__WEBPACK_IMPORTED_MODULE_2__.process_template)(item['code'], template_vars));
        // Create callback for method event type
        else if (item['action'] === 'method')
            return () => {
                if (!item['params'])
                    this.send({ event: 'method', method: (0,_utils__WEBPACK_IMPORTED_MODULE_2__.process_template)(item['code'], template_vars) });
                else
                    this.send({ event: 'method', method: (0,_utils__WEBPACK_IMPORTED_MODULE_2__.process_template)(item['code'], template_vars), params: (0,_utils__WEBPACK_IMPORTED_MODULE_2__.process_template)(item['params'], template_vars) });
            };
        // Create callback for custom event type
        else
            return new Function((0,_utils__WEBPACK_IMPORTED_MODULE_2__.process_template)(item['code'], template_vars));
    }
    attach_menu_options() {
        // Clear any existing menu
        const menu = this.element.querySelector('.nbtools-menu');
        menu.querySelectorAll('.nbtools-menu-extra').forEach((e) => e.remove());
        const menu_items = this.model.get('extra_menu_items');
        Object.keys(menu_items).forEach((name) => {
            const item = menu_items[name];
            const callback = this.create_menu_callback(item);
            this.add_menu_item(name, callback, 'nbtools-menu-extra');
        });
    }
    float_menus() {
        const fix_cell = () => {
            const elements = [
                this.el.closest('.lm-Widget.jp-OutputPrompt.jp-OutputArea-prompt'),
                this.el.closest('.lm-Widget.lm-Panel.jp-OutputArea'),
                this.el.closest('.lm-Widget.lm-Panel.jp-OutputArea-child'),
                this.el.closest('.lm-Widget.lm-Panel.jp-OutputArea-output'),
                this.el.closest('.lm-Widget.jp-OutputArea.jp-Cell-outputArea')
            ];
            elements.forEach((e) => {
                if (e)
                    e.style.overflow = 'visible';
            });
        };
        this.el.addEventListener('click', fix_cell, { once: true });
    }
    /**
     * Recursively trigger the 'displayed' event for all child widgets
     *
     * @param {DOMWidgetModel} model
     * @param {DOMWidgetView | any} view
     * @private
     */
    static _initialize_display(model, view) {
        // Trigger the display for this widget
        view.trigger('displayed');
        // Recursively trigger the display for all child widgets
        if ('children_views' in view) {
            view.children_views.update(model.get('children')).then((children) => {
                children.forEach((child) => {
                    BaseWidgetView._initialize_display(child.model, child);
                    child.el.widget = child;
                });
            });
        }
    }
    /**
     * Add the specified child widget to the view and initialize
     *
     * @param {string} element_selector
     * @param {string} model_name
     */
    attach_child_widget(element_selector, model_name) {
        const element = this.element.querySelector(element_selector);
        const model = this.model.get(model_name);
        this.create_child_view(model).then((view) => {
            element.appendChild(view.el);
            BaseWidgetView._initialize_display(model, view);
            return view;
        }).catch((0,_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_3__.reject)(`Could not add ${model_name} to ${element_selector}`, true));
    }
    basics() { return this.traitlets; } // Return the list of basic traitlets
    post_render() { } // Empty function, can be overridden in subclasses
}


/***/ }),

/***/ "./lib/context.js":
/*!************************!*\
  !*** ./lib/context.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ContextManager": () => (/* binding */ ContextManager)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__);



class ContextManager {
    static context() {
        if (!ContextManager._context) {
            if (ContextManager.is_lab())
                ContextManager._context = new LabContext();
            else if (ContextManager.is_notebook())
                ContextManager._context = new NotebookContext();
            else
                ContextManager._context = new EmbedContext();
        }
        return ContextManager._context;
    }
    /**
     * Determine is this is running in JupyterLab
     *
      * @returns {boolean}
     */
    static is_lab() {
        // The assumption is that only JupyterLab will provide an initialized NotebookTracker object
        // If a better way to detect the environment becomes available, use that instead
        return !!ContextManager.notebook_tracker;
        // A previous implementation replied on checking the DOM
        // return !!document.querySelector("#main.jp-LabShell")
    }
    /**
     * Determine if this is running in the classic Jupyter Notebook
     *
     * @returns {boolean}
     */
    static is_notebook() {
        // Check if the Jupyter global variable has been defined
        return !!(window['Jupyter']);
    }
}
/**
 * Abstract base class representing the context in which the widgets are running.
 * Contexts include: JupyterLab, Jupyter Notebook and Embedded.
 */
class Context {
}
/**
 * Context handler for JupyterLab
 */
class LabContext extends Context {
    /**
     * Toggle hiding or or showing the code for the specified cell
     *
     * @param {HTMLElement} element
     * @param {boolean} display
     */
    toggle_code(element, display) {
        setTimeout(() => {
            let input_block = element.closest('.jp-Cell');
            if (input_block)
                input_block = input_block.querySelector('.jp-Cell-inputWrapper');
            // Set display to toggle if not specified
            if (!!display)
                (0,_utils__WEBPACK_IMPORTED_MODULE_0__.show)(input_block);
            else if (display === false)
                (0,_utils__WEBPACK_IMPORTED_MODULE_0__.hide)(input_block, '30px');
            else
                (0,_utils__WEBPACK_IMPORTED_MODULE_0__.toggle)(input_block, '30px');
        }, 100);
    }
    /**
     * Execute the indicated cell in the notebook
     *
     * @param cell
     */
    run_cell(cell = null) {
        if (!ContextManager.notebook_tracker)
            return; // If no notebook_tracker, do nothing
        // If cell is falsy, default to the active cell
        if (!cell)
            cell = ContextManager.notebook_tracker.activeCell;
        // If this is a code cell
        if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell) {
            const current = ContextManager.notebook_tracker.currentWidget;
            if (current) {
                _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell.execute(cell, current.context.sessionContext);
            }
        }
        // If this is a markdown cell
        // if (ContextManager.notebook_tracker.activeCell instanceof MarkdownCell)
        //     MarkdownCell.renderInput(ContextManager.notebook_tracker.activeCell)
    }
    /**
     * Execute all cells with nbtools widgets in the current notebook
     */
    run_tool_cells() {
        if (!ContextManager.notebook_tracker)
            return; // If no notebook_tracker, do nothing
        if (!ContextManager.notebook_tracker.currentWidget)
            return; // If no notebook selected, do nothing
        const cell_widgets = ContextManager.notebook_tracker.currentWidget.content.widgets;
        cell_widgets.forEach((widget) => {
            if (this.is_tool_cell(widget))
                this.run_cell(widget);
        });
    }
    /**
     * Get the relative path to the current notebook
     */
    notebook_path() {
        if (!ContextManager.notebook_tracker)
            return ''; // If no notebook_tracker, do nothing
        if (!ContextManager.notebook_tracker.currentWidget)
            return ''; // If no active notebook, do nothing
        if (!ContextManager.notebook_tracker.currentWidget.context)
            return ''; // If no context, do nothing
        const notebook_context = ContextManager.notebook_tracker.currentWidget.context;
        const notebook_path = notebook_context.path;
        const directory_path = notebook_path.substring(0, notebook_path.lastIndexOf("/") + 1);
        return directory_path;
    }
    /**
     * Determines if the given cell contains a notebook tool widget
     *
     * @param cell
     * @returns boolean
     */
    is_tool_cell(cell) {
        const dom_node = cell.node || cell.element;
        if (!!dom_node)
            return !!dom_node.querySelector('.nbtools');
        else
            return false;
    }
    /**
     * Path to the default GenePattern logo
     */
    default_logo() {
        return __webpack_require__(/*! ../style/g2nb_logo.png */ "./style/g2nb_logo.png").default;
    }
    /**
     * Path to the default GenePattern icon
     */
    default_icon() {
        return __webpack_require__(/*! ../style/icon.svg */ "./style/icon.svg").default;
    }
    /**
     * Return the id of the current notebook's kernel
     *
     * @param notebook
     */
    kernel_id(notebook) {
        // If the current widget isn't a notebook, there is no kernel
        if (!(notebook instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookPanel))
            return null;
        // Protect against null
        if (!notebook ||
            !notebook.context ||
            !notebook.context.sessionContext ||
            !notebook.context.sessionContext.session ||
            !notebook.context.sessionContext.session.kernel)
            return null;
        return notebook.context.sessionContext.session.kernel.id;
    }
    /**
     * Function to execute when the notebook is opened and selected
     *
     * @param callback
     */
    notebook_focus(callback) {
        const notebook_tracker = ContextManager.notebook_tracker;
        notebook_tracker && notebook_tracker.activeCellChanged.connect(() => {
            const current_widget = notebook_tracker.currentWidget;
            callback(current_widget);
        });
    }
    /**
     * Execute the callback when the current kernel is ready
     *
     * @param current
     * @param callback
     */
    kernel_ready(current, callback) {
        // If the current widget isn't a notebook, there is no kernel
        if (!(current instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookPanel))
            return;
        current.context.sessionContext.ready.then(() => callback());
    }
    /**
     * Execute the callback every time the kernel is changed or restarts
     *
     * @param current
     * @param callback
     */
    kernel_changed(current, callback) {
        current.context.sessionContext.kernelChanged.connect(() => callback());
    }
    /**
     * Send the provided code to the kernel
     *
     * @param notebook
     * @param code
     */
    execute_code(notebook, code) {
        const current = notebook;
        if (!current.context.sessionContext.session ||
            !current.context.sessionContext.session.kernel)
            return; // Protect against null kernels
        // Import the default tools
        current.context.sessionContext.session.kernel.requestExecute({ code: code });
    }
    /**
     * Create a new comm
     *
     * @param current
     * @param name
     * @param callback
     */
    create_comm(current, name, callback) {
        const kernel = current.context.sessionContext.session.kernel;
        const comm = kernel.createComm(name);
        comm.onMsg = callback;
        comm.open({}); // Open the comm
        return comm;
    }
}
/**
 * Context handler for the classic Jupyter Notebook
 */
class NotebookContext extends Context {
    /**
     * Toggle hiding or or showing the code for the specified cell
     *
     * @param {HTMLElement} element
     * @param {boolean} display
     */
    toggle_code(element, display) {
        setTimeout(() => {
            const cell_element = element.closest(".cell");
            if (!cell_element)
                return; // Widget has not yet been added to the DOM
            const code = cell_element.querySelector(".input");
            // Set display to toggle if not specified
            if (!!display)
                (0,_utils__WEBPACK_IMPORTED_MODULE_0__.show)(code);
            else if (display === false)
                (0,_utils__WEBPACK_IMPORTED_MODULE_0__.hide)(code);
            else
                (0,_utils__WEBPACK_IMPORTED_MODULE_0__.toggle)(code);
        }, 10);
    }
    /**
     * Execute the indicated cell in the notebook
     *
     * @param cell
     */
    run_cell(cell) {
        window.Jupyter.notebook.execute_cell(cell);
    }
    /**
     * Execute all cells with nbtools widgets in the current notebook
     */
    run_tool_cells() {
        const cells_to_run = [];
        window.Jupyter.notebook.get_cells().forEach((cell, index) => {
            if (this.is_tool_cell(cell))
                cells_to_run.push(index);
        });
        window.Jupyter.notebook.execute_cells(cells_to_run);
    }
    notebook_path() {
        return window.Jupyter.notebook.path;
    }
    base_path() {
        const body = document.querySelector('body');
        if (!body)
            return ''; // If there is no body, unable to get path
        return body.getAttribute('data-base-url') + 'nbextensions/nbtools/';
    }
    /**
     * Determines if the given cell contains a notebook tool widget
     *
     * @param cell
     * @returns boolean
     */
    is_tool_cell(cell) {
        const dom_node = cell.node || cell.element;
        if (!!dom_node)
            return !!dom_node.find('.nbtools').length;
        else
            return false;
    }
    /**
     * Path to the default GenePattern logo
     */
    default_logo() {
        return this.base_path() + __webpack_require__(/*! ../style/g2nb_logo.png */ "./style/g2nb_logo.png").default;
    }
    /**
     * Path to the default GenePattern icon
     */
    default_icon() {
        return this.base_path() + __webpack_require__(/*! ../style/icon.svg */ "./style/icon.svg").default;
    }
    /**
     * Return the id of the current notebook's kernel
     *
     * @param notebook
     */
    kernel_id(notebook) {
        return window.Jupyter.notebook.kernel.id;
    }
    /**
     * Function to execute when the notebook is opened and selected
     *
     * @param callback
     */
    notebook_focus(callback) {
        window.Jupyter.notebook.events.ready(() => {
            callback(window.Jupyter.notebook);
        });
    }
    /**
     * Execute the callback when the current kernel is ready
     *
     * @param current
     * @param callback
     */
    kernel_ready(current, callback) {
        setTimeout(() => {
            if (window.Jupyter.notebook.kernel.is_connected())
                callback(window.Jupyter.notebook);
            else
                window.Jupyter.notebook.events.one('kernel_ready.Kernel', () => {
                    callback(window.Jupyter.notebook);
                });
        }, 100);
    }
    /**
     * Execute the callback every time the kernel is changed or restarts
     *
     * @param current
     * @param callback
     */
    kernel_changed(current, callback) {
        window.Jupyter.notebook.events.on('kernel_ready.Kernel', () => {
            callback(window.Jupyter.notebook);
        });
    }
    /**
     * Send the provided code to the kernel
     *
     * @param notebook
     * @param code
     */
    execute_code(notebook, code) {
        window.Jupyter.notebook.kernel.execute(code);
    }
    /**
     * Create a new comm
     *
     * @param current
     * @param name
     * @param callback
     */
    create_comm(current, name, callback) {
        let comm = window.Jupyter.notebook.kernel.comm_manager.new_comm(name);
        comm.on_msg(callback);
        return comm;
    }
}
/**
 * Context handler for embedded widgets
 */
class EmbedContext extends Context {
    /**
     * No cells in this context, so do nothing
     *
     * @param {HTMLElement} element
     * @param {boolean} display
     */
    toggle_code(element, display) { }
    /**
     * No cells in this context, so do nothing
     * @param cell
     */
    run_cell(cell) { }
    /**
     * No cells in this context, so do nothing
     */
    run_tool_cells() { }
    /**
     * No notebook in this context
     */
    notebook_path() { return ''; }
    base_path() {
        const body = document.querySelector('body');
        if (!body)
            return ''; // If there is no body, unable to get path
        return body.getAttribute('data-base-url') + 'nbextensions/nbtools/';
    }
    /**
     * Determines if the given cell contains a notebook tool widget
     *
     * @param cell
     * @returns boolean
     */
    is_tool_cell(cell) {
        const dom_node = cell.node || cell.element;
        if (!!dom_node)
            return !!dom_node.querySelector('.nbtools');
        else
            return false;
    }
    /**
     * Path to the default GenePattern logo
     */
    default_logo() {
        return this.base_path() + __webpack_require__(/*! ../style/g2nb_logo.png */ "./style/g2nb_logo.png").default;
    }
    /**
     * Path to the default GenePattern icon
     */
    default_icon() {
        return __webpack_require__(/*! ../style/icon.svg */ "./style/icon.svg").default;
    }
    /**
     * Return the id of the current notebook's kernel
     *
     * @param notebook
     */
    kernel_id(notebook) {
        return null;
    }
    /**
     * Function to execute when the notebook is opened and selected
     *
     * @param callback
     */
    notebook_focus(callback) { }
    /**
     * Execute the callback when the current kernel is ready
     *
     * @param current
     * @param callback
     */
    kernel_ready(current, callback) { }
    /**
     * Execute the callback every time the kernel is changed or restarts
     *
     * @param current
     * @param callback
     */
    kernel_changed(current, callback) {
        // FIXME: Global Jupyter variable may not be accessible in newer version of voila
        window.Jupyter.notebook.events.on('kernel_ready.Kernel', () => {
            callback(window.Jupyter.notebook);
        });
    }
    /**
     * Send the provided code to the kernel
     *
     * @param notebook
     * @param code
     */
    execute_code(notebook, code) {
        // FIXME: Global Jupyter variable may not be accessible in newer version of voila
        window.Jupyter.notebook.kernel.execute(code);
    }
    /**
     * Create a new comm
     *
     * @param current
     * @param name
     * @param callback
     */
    create_comm(current, name, callback) {
        // FIXME: Global Jupyter variable may not be accessible in newer version of voila
        let comm = window.Jupyter.notebook.kernel.comm_manager.new_comm(name);
        comm.on_msg(callback);
        return comm;
    }
}


/***/ }),

/***/ "./lib/dataregistry.js":
/*!*****************************!*\
  !*** ./lib/dataregistry.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IDataRegistry": () => (/* binding */ IDataRegistry),
/* harmony export */   "DataRegistry": () => (/* binding */ DataRegistry),
/* harmony export */   "Data": () => (/* binding */ Data)
/* harmony export */ });
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");



const IDataRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token("nbtools.data");
class DataRegistry {
    // { 'kernel_id': { 'origin': { 'identifier': data } } }
    /**
     * Initialize the DataRegistry and connect event handlers
     */
    constructor() {
        this.current = null; // Reference to the currently selected notebook or other widget
        this.kernel_data_cache = {}; // Keep a cache of kernels to registered data
        // Lazily assign the data registry to the context
        if (!_context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.data_registry)
            _context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.data_registry = this;
        _context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.context().notebook_focus((current_widget) => {
            // Current notebook hasn't changed, no need to do anything, return
            if (this.current === current_widget)
                return;
            // Otherwise, update the current notebook reference
            this.current = current_widget;
        });
    }
    /**
     * Register data for the sent to/come from menus
     * Return whether registration was successful or not
     *
     * @param origin
     * @param identifier
     * @param kind
     * @param data
     */
    register({ origin = null, uri = null, kind = null, data = null }) {
        // Use origin, identifier and kind to initialize data, if needed
        if (!data)
            data = new Data(origin, uri, kind);
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return false; // If no kernel, do nothing
        // Lazily initialize dict for kernel cache
        let cache = this.kernel_data_cache[kernel_id];
        if (!cache)
            cache = this.kernel_data_cache[kernel_id] = {};
        // Lazily initialize dict for origin
        let origin_data = cache[data.origin];
        if (!origin_data)
            origin_data = cache[data.origin] = {};
        // Add to cache and return
        origin_data[data.uri] = data;
        return true;
    }
    /**
     * Unregister data with the given origin and identifier
     * Return the unregistered data object
     * Return null if un-registration was unsuccessful
     *
     * @param origin
     * @param identifier
     * @param kind
     * @param data
     */
    unregister({ origin = null, uri = null, kind = null, data = null }) {
        // Use origin, identifier and kind to initialize data, if needed
        if (!data)
            data = new Data(origin, uri, kind);
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return null; // If no kernel, do nothing
        // If unable to retrieve cache, return null
        const cache = this.kernel_data_cache[kernel_id];
        if (!cache)
            return null;
        // If unable to retrieve origin, return null
        const origin_data = cache[data.origin];
        if (!origin_data)
            return null;
        // If unable to find identifier, return null;
        const found = origin_data[data.uri];
        if (!found)
            return null;
        // Remove from the registry and return
        delete origin_data[data.uri];
        return found;
    }
    /**
     * Get all data that matches one of the specified kinds or origins
     * If kinds or origins is null or empty, accept all kinds or origins, respectively
     *
     * @param kinds
     * @param origins
     */
    get_data({ kinds = null, origins = null }) {
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return {}; // If no kernel, return empty
        // If unable to retrieve cache, return empty
        const cache = this.kernel_data_cache[kernel_id];
        if (!cache)
            return {};
        // Compile map of data with a matching origin and kind
        const matching = {};
        for (let origin of Object.keys(cache)) {
            if (origins === null || origins.length === 0 || origins.includes(origin)) {
                const hits = {};
                for (let data of Object.values(cache[origin])) {
                    if (kinds === null || kinds.length === 0 || kinds.includes(data.kind))
                        hits[data.label] = data.uri;
                }
                if (Object.keys(hits).length > 0)
                    matching[origin] = hits;
            }
        }
        return matching;
    }
    /**
     * Retrieve the kernel ID from the currently selected notebook
     * Return null if no kernel or no notebook selected
     */
    current_kernel_id() {
        return _context__WEBPACK_IMPORTED_MODULE_0__.ContextManager.context().kernel_id(this.current);
    }
}
class Data {
    constructor(origin, uri, label = null, kind = null) {
        this.origin = origin;
        this.uri = uri;
        this.label = !!label ? label : (0,_utils__WEBPACK_IMPORTED_MODULE_2__.extract_file_name)(uri);
        this.kind = !!kind ? kind : (0,_utils__WEBPACK_IMPORTED_MODULE_2__.extract_file_type)(uri);
    }
}


/***/ }),

/***/ "./lib/registry.js":
/*!*************************!*\
  !*** ./lib/registry.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IToolRegistry": () => (/* binding */ IToolRegistry),
/* harmony export */   "ToolRegistry": () => (/* binding */ ToolRegistry)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);




const IToolRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.Token("nbtools");
class ToolRegistry {
    /**
     * Initialize the ToolRegistry and connect event handlers
     */
    constructor() {
        this.current = null; // Reference to the currently selected notebook or other widget
        this._update_callbacks = []; // Functions to call when an update happens
        this.kernel_tool_cache = {}; // Keep a cache of kernels to registered tools
        this.kernel_import_cache = {}; // Keep a cache of whether nbtools has been imported
        // Lazily assign the tool registry to the context
        if (!_context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry)
            _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry = this;
        _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().notebook_focus((current_widget) => {
            // Current notebook hasn't changed, no need to do anything, return
            if (this.current === current_widget)
                return;
            // Otherwise, update the current notebook reference
            this.current = current_widget;
            // If the current selected widget isn't a notebook, no comm is needed
            if (!(this.current instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel) && _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.is_lab())
                return;
            // Initialize the comm
            this.init_comm();
            // Load the default tools
            this.import_default_tools();
        });
    }
    import_default_tools() {
        _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().kernel_changed(this.current, () => {
            _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().execute_code(this.current, 'from nbtools import import_defaults\nimport_defaults()');
        });
    }
    /**
     * Initialize the comm between the notebook widget kernel and the ToolManager
     */
    init_comm() {
        _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().kernel_ready(this.current, () => {
            const current = this.current;
            // Create a new comm that connects to the nbtools_comm target
            const connect_comm = () => {
                const comm = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().create_comm(current, 'nbtools_comm', (msg) => {
                    // Handle message sent by the kernel
                    const data = msg.content.data;
                    if (data.func === 'update')
                        this.update_tools(data.payload);
                    else if (data.func === 'notification')
                        (0,_utils__WEBPACK_IMPORTED_MODULE_1__.send_notification)(data.payload.message, data.payload.sender, _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().default_logo());
                    else
                        console.error('ToolRegistry received unknown message: ' + data);
                });
                window.comm = comm;
                // Request the current tool list
                comm.send({
                    'func': 'request_update'
                });
            };
            // When the kernel restarts or is changed, reconnect the comm
            _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().kernel_changed(current, () => connect_comm());
            // Connect to the comm upon initial startup
            connect_comm();
            // Update tools from the cache
            this.update_from_cache();
        });
    }
    /**
     * Get tools from the cache and make registered callbacks
     */
    update_from_cache() {
        // Get the kernel ID
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return; // Do nothing if null
        // Get tools from the cache
        const tool_list = this.kernel_tool_cache[kernel_id];
        // Make registered callbacks for when tools are updated
        this._update_callbacks.forEach((callback) => {
            callback(tool_list);
        });
    }
    /**
     * Message the kernel, requesting an update to the tools cache
     *
     * @param comm
     */
    request_update(comm) {
        comm.send({ 'func': 'request_update' });
    }
    /**
     * Register an update callback with the ToolRegistry
     *
     * @param callback
     */
    on_update(callback) {
        this._update_callbacks.push(callback);
    }
    /**
     * Retrieve the kernel ID from the currently selected notebook
     * Return null if no kernel or no notebook selected
     */
    current_kernel_id() {
        return _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.context().kernel_id(this.current);
    }
    /**
     * Update the tools cache for the current kernel
     *
     * @param message
     */
    update_tools(message) {
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return; // Do nothing if no kernel
        // Parse the message
        const tool_list = message['tools'];
        const needs_import = !!message['import'];
        // Update the cache
        this.kernel_tool_cache[kernel_id] = tool_list;
        this.kernel_import_cache[kernel_id] = needs_import;
        // Make registered callbacks when tools are updated
        this._update_callbacks.forEach((callback) => {
            callback(tool_list);
        });
    }
    /**
     * Query whether nbtools has been imported in this kernel
     */
    needs_import() {
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return true; // Assume true if no kernel
        // Get import status from the cache and protect against undefined
        return !this.kernel_import_cache[kernel_id];
    }
    /**
     * Returns a list of all currently registered tools
     *
     * @returns {Array} - A list of registered tools
     */
    list() {
        const kernel_id = this.current_kernel_id();
        if (!kernel_id)
            return []; // Empty list if no kernel
        // Get tools from the cache and protect against undefined
        const tools = this.kernel_tool_cache[kernel_id];
        if (!tools)
            return [];
        return Object.keys(tools).map(function (key) {
            return tools[key];
        });
    }
    /**
     * Has this tool already been registered?
     *
     * @param origin
     * @param id
     * @returns {boolean}
     */
    has_tool(origin, id) {
        let found_tool = false;
        this.list().forEach(tool => {
            if (tool.id === id && tool.origin === origin)
                found_tool = true;
        });
        return found_tool;
    }
}


/***/ }),

/***/ "./lib/toolbox.js":
/*!************************!*\
  !*** ./lib/toolbox.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ToolBrowser": () => (/* binding */ ToolBrowser),
/* harmony export */   "Toolbox": () => (/* binding */ Toolbox),
/* harmony export */   "SearchBox": () => (/* binding */ SearchBox)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);




class ToolBrowser extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.search = null;
        this.toolbox = null;
        this.addClass('nbtools-browser');
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout();
        this.search = new SearchBox();
        this.toolbox = new Toolbox(this.search);
        this.layout.addWidget(this.search);
        this.layout.addWidget(this.toolbox);
    }
}
class Toolbox extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(associated_search) {
        super();
        this.last_update = 0;
        this.update_waiting = false;
        this.search = associated_search;
        this.addClass('nbtools-toolbox');
        this.addClass('nbtools-wrapper');
        // Update the toolbox when the tool registry changes
        _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry.on_update(() => {
            // If the last update was more than 10 seconds ago, update the toolbox
            if (this.update_stale())
                this.fill_toolbox();
            else
                this.queue_update(); // Otherwise, queue an update if not already waiting for one
        });
        // Fill the toolbox with the registered tools
        this.fill_toolbox();
    }
    update_stale() {
        return this.last_update + (3 * 1000) < Date.now();
    }
    queue_update() {
        // If no update is waiting, queue an update
        if (!this.update_waiting) {
            setTimeout(() => {
                this.fill_toolbox(); // Fill the toolbox
                this.update_waiting = false; // And mark as no update queued
            }, Math.abs(this.last_update + (3 * 1000) - Date.now())); // Queue for 3 seconds since last update
            this.update_waiting = true; // And mark as queued
        }
    }
    static add_tool_cell(tool) {
        // Check to see if nbtools needs to be imported
        const import_line = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry.needs_import() ? 'import nbtools\n\n' : '';
        // Add and run a code cell with the generated tool code
        Toolbox.add_code_cell(import_line + `nbtools.tool(id='${tool.id}', origin='${tool.origin}')`);
    }
    static add_code_cell(code) {
        if (!_context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.notebook_tracker)
            return; // If no NotebookTracker, do nothing
        const current = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry.current;
        if (!current || !(current instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.NotebookPanel))
            return; // If no notebook is currently selected, return
        let cell = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.notebook_tracker.activeCell;
        if (!cell)
            return; // If no cell is selected, do nothing
        // If the currently selected cell isn't empty, insert a new one below and select it
        const current_cell_code = cell.model.value.text.trim();
        if (!!current_cell_code)
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.NotebookActions.insertBelow(current.content);
        // Fill the cell with the tool's code
        cell = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.notebook_tracker.activeCell; // The active cell may just have been updated
        if (cell)
            cell.model.value.text = code;
        // Run the cell
        return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.NotebookActions.run(current.content, current.context.sessionContext);
    }
    fill_toolbox() {
        this.last_update = Date.now();
        // First empty the toolbox
        this.empty_toolbox();
        // Get the list of tools
        const tools = _context__WEBPACK_IMPORTED_MODULE_2__.ContextManager.tool_registry.list();
        // Organize by origin and sort
        const organized_tools = this.organize_tools(tools);
        const origins = Object.keys(organized_tools);
        origins.sort((a, b) => {
            const a_name = a.toLowerCase();
            const b_name = b.toLowerCase();
            return (a_name < b_name) ? -1 : (a_name > b_name) ? 1 : 0;
        });
        // Add each origin
        origins.forEach((origin) => {
            const origin_box = this.add_origin(origin);
            organized_tools[origin].forEach((tool) => {
                this.add_tool(origin_box, tool);
            });
        });
        // Apply search filter after refresh
        this.search.filter(this.search.node.querySelector('input.nbtools-search'));
    }
    organize_tools(tool_list) {
        const organized = {};
        // Group tools by origin
        tool_list.forEach((tool) => {
            if (tool.origin in organized)
                organized[tool.origin].push(tool); // Add tool to origin
            else
                organized[tool.origin] = [tool]; // Lazily create origin
        });
        // Sort the tools in each origin
        Object.keys(organized).forEach((origin) => {
            organized[origin].sort((a, b) => {
                const a_name = a.name.toLowerCase();
                const b_name = b.name.toLowerCase();
                return (a_name < b_name) ? -1 : (a_name > b_name) ? 1 : 0;
            });
        });
        // Return the organized set of notebooks
        return organized;
    }
    empty_toolbox() {
        this.node.innerHTML = '';
    }
    add_origin(name) {
        // Create the HTML DOM element
        const origin_wrapper = document.createElement('div');
        origin_wrapper.innerHTML = `
            <header class="nbtools-origin" title="${name}">
                <span class="nbtools-expanded nbtools-collapse jp-Icon jp-Icon-16 jp-ToolbarButtonComponent-icon"></span>
                ${name}
            </header>
            <ul class="nbtools-origin" title="${name}"></ul>`;
        // Attach the expand / collapse functionality
        const collapse = origin_wrapper.querySelector('span.nbtools-collapse');
        collapse.addEventListener("click", () => this.toggle_collapse(origin_wrapper));
        // Add to the toolbox
        this.node.append(origin_wrapper);
        return origin_wrapper;
    }
    add_tool(origin, tool) {
        const list = origin.querySelector('ul');
        const tool_wrapper = document.createElement('li');
        tool_wrapper.classList.add('nbtools-tool');
        tool_wrapper.setAttribute('title', 'Click to add to notebook');
        tool_wrapper.innerHTML = `
            <div class="nbtools-add">+</div>
            <div class="nbtools-header">${tool.name}</div>
            <div class="nbtools-description">${tool.description}</div>`;
        if (list)
            list.append(tool_wrapper);
        // Add the click event
        tool_wrapper.addEventListener("click", () => {
            Toolbox.add_tool_cell(tool);
        });
    }
    toggle_collapse(origin_wrapper) {
        const list = origin_wrapper.querySelector("ul.nbtools-origin");
        const collapsed = list.classList.contains('nbtools-hidden');
        // Toggle the collapse button
        const collapse = origin_wrapper.querySelector('span.nbtools-collapse');
        if (collapsed) {
            collapse.classList.add('nbtools-expanded');
            collapse.classList.remove('nbtools-collapsed');
        }
        else {
            collapse.classList.remove('nbtools-expanded');
            collapse.classList.add('nbtools-collapsed');
        }
        // Hide or show widget body
        (0,_utils__WEBPACK_IMPORTED_MODULE_1__.toggle)(list);
    }
}
class SearchBox extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.value = '';
        this.node.innerHTML = `
            <div class="nbtools-wrapper">
                <div class="nbtools-outline">
                    <input type="search" class="nbtools-search" spellcheck="false" placeholder="SEARCH" />
                </div>
            </div>
        `;
        this.attach_events();
    }
    attach_events() {
        // Attach the change event to the search box
        const search_box = this.node.querySelector('input.nbtools-search');
        search_box.addEventListener("keyup", () => this.filter(search_box));
    }
    filter(search_box) {
        // Update the value state
        this.value = search_box.value.toLowerCase().replace(/[^a-z0-9]/g, '');
        // Get the toolbox
        const toolbox = document.querySelector('#nbtools-browser > .nbtools-toolbox');
        if (!toolbox)
            return; // Do nothing if the toolbox is null
        // Show any tool that matches and hide anything else
        toolbox.querySelectorAll('li.nbtools-tool').forEach((tool) => {
            if (tool.textContent.toLowerCase().replace(/[^a-z0-9]/g, '').includes(this.value))
                tool.style.display = 'block';
            else
                tool.style.display = 'none';
        });
    }
}


/***/ }),

/***/ "./lib/uibuilder.js":
/*!**************************!*\
  !*** ./lib/uibuilder.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "UIBuilderModel": () => (/* binding */ UIBuilderModel),
/* harmony export */   "UIBuilderView": () => (/* binding */ UIBuilderView)
/* harmony export */ });
/* harmony import */ var _style_uibuilder_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../style/uibuilder.css */ "./style/uibuilder.css");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _basewidget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./basewidget */ "./lib/basewidget.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/**
 * Define the UI Builder widget for Jupyter Notebook
 *
 * @author Thorin Tabor
 *
 * Copyright 2020 Regents of the University of California and the Broad Institute
 */






// noinspection JSAnnotator
class UIBuilderModel extends _basewidget__WEBPACK_IMPORTED_MODULE_3__.BaseWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: UIBuilderModel.model_name, _model_module: UIBuilderModel.model_module, _model_module_version: UIBuilderModel.model_module_version, _view_name: UIBuilderModel.view_name, _view_module: UIBuilderModel.view_module, _view_module_version: UIBuilderModel.view_module_version, name: 'Python Function', description: '', _parameters: [], parameter_groups: [], accept_origins: [], function_import: '', register_tool: true, collapse: true, events: {}, buttons: {}, license: {}, display_header: true, display_footer: true, busy: false, run_label: 'Run', form: undefined, output: undefined });
    }
}
UIBuilderModel.model_name = 'UIBuilderModel';
UIBuilderModel.model_module = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME;
UIBuilderModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;
UIBuilderModel.view_name = 'UIBuilderView';
UIBuilderModel.view_module = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME;
UIBuilderModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;
UIBuilderModel.serializers = Object.assign(Object.assign({}, _basewidget__WEBPACK_IMPORTED_MODULE_3__.BaseWidgetModel.serializers), { form: {
        deserialize: (value, manager) => (0,_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__.unpack_models)(value, manager)
    } });
// noinspection JSAnnotator
class UIBuilderView extends _basewidget__WEBPACK_IMPORTED_MODULE_3__.BaseWidgetView {
    constructor() {
        super(...arguments);
        this.dom_class = 'nbtools-uibuilder';
        this.traitlets = [...super.basics(), 'origin', '_parameters', 'function_import', 'register_tool', 'collapse',
            'events', 'run_label', 'form', 'output'];
        this.renderers = {
            "error": this.render_error,
            "info": this.render_info
        };
        this.body = `
        <div class="nbtools-buttons">
            <button class="nbtools-run" data-traitlet="run_label"></button>
        </div>
        <div class="nbtools-description" data-traitlet="description"></div>
        <div class="nbtools-busy">
            <div>
                <i class="fas fa-circle-notch fa-spin"></i>
            </div>
        </div>
        <div class="nbtools-error" data-traitlet="error"></div>
        <div class="nbtools-info" data-traitlet="info"></div>
        <div class="nbtools-form"></div>
        <div class="nbtools-footer"></div>
        <div class="nbtools-buttons">
            <button class="nbtools-run" data-traitlet="run_label"></button>
        </div>`;
        this.dialog = `<div class="nbtools-dialog">
                           <div class="nbtools-panel">
                               <div class="nbtools-header"></div>
                               <div class="nbtools-body">
                                   <p></p>
                                   <div class="nbtools-panel-button">
                                       <button class="nbtools-panel-cancel">Cancel</button>
                                       <button class="nbtools-panel-button"></button>
                                   </div>
                               </div>
                           </div>
                       </div>`;
    }
    render() {
        super.render();
        // Hide the header or footer, if necessary
        this.display_header_changed();
        this.display_footer_changed();
        this.model.on(`change:display_header`, this.display_header_changed, this);
        this.model.on(`change:display_footer`, this.display_footer_changed, this);
        // Show or hide the "busy" UI
        this.busy_changed();
        this.model.on(`change:busy`, this.busy_changed, this);
        // Attach the Reset Parameters gear option
        this.add_menu_item('Reset Parameters', () => this.reset_parameters());
        // Attach the Run button callbacks
        this.activate_run_buttons();
        // Attach custom buttons
        this.activate_custom_buttons();
        // Display the license, if any
        this.display_license();
        // Add the interactive form widget
        this.attach_child_widget('.nbtools-form', 'form');
        // After the view is rendered
        (0,_utils__WEBPACK_IMPORTED_MODULE_4__.element_rendered)(this.el).then(() => {
            // Attach ID and event callbacks
            this._attach_callbacks();
            // Create parameter groups
            this._init_parameter_groups();
            // Attach the Advanced Options gear option, if necessary
            if (this.has_advanced())
                this.add_menu_item('Advanced Options', () => this.toggle_advanced());
        });
    }
    busy_changed() {
        const display = this.model.get('busy') ? 'block' : 'none';
        this.element.querySelector('.nbtools-busy').style.display = display;
    }
    display_header_changed() {
        const display = this.model.get('display_header') ? 'block' : 'none';
        this.element.querySelector('.nbtools-buttons:first-of-type').style.display = display;
        this.element.querySelector('.nbtools-description').style.display = display;
    }
    display_footer_changed() {
        const display = this.model.get('display_footer') ? 'block' : 'none';
        this.element.querySelector('.nbtools-buttons:last-of-type').style.display = display;
        this.element.querySelector('.nbtools-footer').style.display = display;
        // If there is an output_var element, hide or show it as necessary
        if (!this.output_var_displayed())
            return;
        this.element.querySelector('.nbtools-input:last-of-type').style.display = display;
    }
    output_var_displayed() {
        const output_var = this.model.get('_parameters')['output_var'];
        return !!(output_var && output_var['hide'] == false);
    }
    /**
     * Displays a EULA to the user, who must agree before continuing.
     *
     * License should be a dict with the following keys:
     *      text: The text of the license
     *      title: The name of the license (optional)
     *      callback: Whether the license has been agreed to (boolean)
     */
    display_license() {
        const license = this.model.get('license'); // Get the license model
        if (!license || !license['text'])
            return; // If there is no license, skip
        this.widget_dialog({ title: license['title'] ||
                'You must agree below to the following end-user license agreement',
            body: license['text'],
            button_label: 'Agree',
            callback: () => {
                license['callback'] = true; // Set to true to trigger callback function
                this.model.set('license', license);
                this.model.save();
            } });
    }
    activate_custom_buttons() {
        this.el.querySelectorAll('.nbtools-buttons').forEach((box) => {
            const buttons = this.model.get('buttons');
            Object.keys(buttons).forEach((label) => {
                const button = new DOMParser().parseFromString(`<button>${label}</button>`, "text/html")
                    .querySelector('button');
                const button_event = new Function(buttons[label]);
                button.addEventListener('click', button_event);
                box.prepend(button);
            });
        });
    }
    /**
     * Attach the click event to each Run button
     */
    activate_run_buttons() {
        this.el.querySelectorAll('.nbtools-run').forEach((button) => button.addEventListener('click', () => {
            // Validate required parameters and return if not valid
            if (!this.validate())
                return;
            // Execute the interact instance
            this.el.querySelector('.widget-interact > .jupyter-button').click();
            // Collapse the widget, if collapse=True
            if (this.model.get('collapse'))
                this.el.querySelector('.nbtools-collapse').click();
        }));
    }
    /**
     * Check to make sure required parameters are checked out.
     * Highlight missing parameters. Return whether valid.
     */
    validate() {
        let valid = true;
        const form = this.el.querySelector('.nbtools-form');
        form.querySelectorAll('.nbtools-input').forEach((param) => {
            if (!param.classList.contains('required'))
                return; // Ignore optional parameters
            const input = param.querySelector('input, select');
            if (input.value.trim() === '') { // If empty
                param.classList.add('missing'); // Add missing style
                valid = false; // Not all params are valid
            }
            else
                param.classList.remove('missing'); // Remove missing style
        });
        return valid;
    }
    widget_dialog({ title = '', body = '', button_label = 'OK', callback = null }) {
        this.element.appendChild(new DOMParser().parseFromString(this.dialog, "text/html")
            .querySelector('body > :first-child'));
        const dialog = this.element.querySelector('.nbtools-dialog');
        const header = dialog.querySelector('.nbtools-header');
        const button = dialog.querySelector('button.nbtools-panel-button');
        header.style.backgroundColor = this.model.get('color');
        header.textContent = title;
        dialog.querySelector('.nbtools-body > p').textContent = body;
        dialog.querySelector('.nbtools-panel-cancel').addEventListener('click', () => dialog.remove());
        button.textContent = button_label;
        button.style.backgroundColor = this.model.get('color');
        button.addEventListener('click', () => {
            dialog.remove();
            callback();
        });
    }
    /**
     * Create group headers and reorder the form widget according to the group spec
     *
     * @private
     */
    _init_parameter_groups() {
        // Get the parameter groups
        const groups = this.model.get('parameter_groups');
        if (!groups || !groups.length)
            return; // No groups are defined, skip this step
        // Get the UI Builder form container
        const form = this.el.querySelector('.nbtools-form > .widget-interact');
        if (!form)
            return; // If no container is found, skip this step
        // Iterate over each group, create headers and add parameters
        groups.reverse().forEach((group) => {
            const hidden = !!group['hidden']; // Is the group collapsed by default?
            const advanced = !!group['advanced']; // Toggle on with advanced options call?
            // Create and add the header
            const header = this._create_group_header(group['name'], hidden, advanced);
            const body = this._create_group_body(header, group['description'], hidden, advanced);
            form.prepend(body);
            form.prepend(header);
            // Add the parameters
            group['parameters'] && group['parameters'].forEach((param_name) => {
                const param = this._param_dom_by_name(form, param_name);
                if (!param)
                    return; // If the parameter is not found, skip
                body.append(param);
            });
        });
    }
    _create_group_header(name, hidden, advanced) {
        // Create the expand / collapse button
        const controls = document.createElement('controls');
        const button = document.createElement('button');
        const icon = document.createElement('span');
        controls.classList.add('nbtools-controls');
        button.classList.add('nbtools-collapse');
        icon.classList.add('fa', 'fa-minus');
        button.append(icon);
        controls.append(button);
        // Create the header
        const header = document.createElement('div');
        header.classList.add('nbtools-header', 'nbtools-group-header');
        if (advanced)
            header.classList.add('nbtools-advanced');
        header.append(name || '');
        header.append(controls);
        // Apply the color
        header.style.backgroundColor = this.model.get('color');
        // Hide the header if no name is given and not collapsed
        if (!name && !hidden)
            header.style.display = 'none';
        // Return the container
        return header;
    }
    _create_group_body(header, description, hidden, advanced) {
        // Create the container
        const box = document.createElement('div');
        box.classList.add('nbtools-group');
        if (advanced)
            box.classList.add('nbtools-advanced');
        // Create the description
        if (description) {
            const desc = document.createElement('div');
            desc.classList.add('nbtools-description');
            desc.append(description || '');
            box.append(desc);
        }
        // Add controls to the expand / collapse button
        const button = header.querySelector('button');
        const icon = button.querySelector('span');
        button.addEventListener('click', () => {
            this._group_toggle_collapse(box, icon);
        });
        // Collapse if hidden
        if (hidden)
            this._group_toggle_collapse(box, icon);
        return box;
    }
    _group_toggle_collapse(group_box, button) {
        const collapsed = group_box.style.display === "none";
        // Hide or show widget body
        (0,_utils__WEBPACK_IMPORTED_MODULE_4__.toggle)(group_box);
        // Toggle the collapse button
        if (collapsed) {
            button.classList.add('fa-minus');
            button.classList.remove('fa-plus');
        }
        else {
            button.classList.remove('fa-minus');
            button.classList.add('fa-plus');
        }
    }
    _param_dom_by_name(form, name) {
        // First attempt: Try to get parameter by data-name attribute (created by attach_callbacks() method)
        let param = form.querySelector(`.nbtools-input[data-name='${name}']`);
        if (param)
            return param; // Found it! Return the parameter
        // Second attempt: Try to locate by parameter name label
        const label = form.querySelector(`.nbtools-input > .widget-label:first-child`);
        if (!label)
            return null; // No matching label found, return null
        const match = name.toLowerCase().replace(/[^a-zA-Z]/g, '') ===
            label.textContent.toLowerCase().replace(/[^a-zA-Z]/g, '');
        if (match)
            return label.closest('.nbtools-input');
        // Match not found, return null
        return null;
    }
    /**
     * Attach ID and event callbacks to the UI Builder
     *
     * @private
     */
    _attach_callbacks() {
        // Handle widget events
        const widget_events = this.model.get('events');
        this._attach_all_events(this.el, widget_events);
        // Handle parameter IDs and parameter events
        const json_parameters = this.model.get('_parameters');
        const dom_parameters = this.el.querySelectorAll('.nbtools-input');
        for (let i = 0; i < json_parameters.length; i++) {
            const param_spec = json_parameters[i];
            const param_el = dom_parameters[i];
            // Attach the data-name attribute
            param_el.setAttribute('data-name', param_spec.name);
            // Attach specified ID as a data-id attribute
            if (!!param_spec.id)
                param_el.setAttribute('data-id', param_spec.id);
            // Attach parameter events
            if (!!param_spec.events) {
                this._attach_all_events(param_el, param_spec.events);
            }
            // Resize footer, if necessary
            if (param_spec.name === 'output_var' && param_spec.description) {
                // noinspection JSConstantReassignment
                this.el.querySelector('.nbtools-footer').style.height = '50px';
            }
        }
        // Attach send to / come from menus
        this._attach_menus();
        // Attach enter key submit event
        this._submit_keypress();
    }
    _submit_keypress() {
        this.el.querySelectorAll('.nbtools-form input, .nbtools-form select').forEach((element) => {
            element.addEventListener("keydown", (event) => {
                if (event.keyCode === 13) {
                    this.el.querySelector('.nbtools-run').click();
                }
            });
        });
    }
    /**
     * Add default choices defined in with UI Builder choice parameter to the label -> value map
     *
     * @param display_value_map
     * @param model
     * @private
     */
    _add_default_choices(display_value_map, model) {
        const choices = model.get('choices');
        if (choices && Object.keys(choices).length)
            display_value_map['Default Choices'] = model.get('choices');
    }
    /**
     * Add all files matching a specific selector to the label -> value map under the specified name
     *
     * @param display_value_map
     * @param target
     * @param kinds
     * @param selector
     * @param group_name
     * @private
     */
    _add_notebook_files(display_value_map, target, kinds, selector, group_name) {
        // Get the notebook's parent node
        const notebook = target.closest('.jp-Notebook');
        // Get all possible outputs
        const markdown_outputs = [...notebook.querySelectorAll(selector)];
        // Build list of compatible outputs
        const compatible_outputs = {};
        markdown_outputs.forEach((output) => {
            let href, label, kind;
            // Handle getting the kind and label from a link
            if (output.tagName.toLowerCase() === 'a') {
                href = output.getAttribute('href');
                label = (output.textContent || href).trim();
                kind = UIBuilderView.get_kind(href);
            }
            // Handle getting the kind and label from text
            else {
                label = (output.textContent || 'Blank Text Option').trim();
                href = (output.textContent || '').trim();
                kind = 'text';
            }
            // Special case for text "send to"
            if (group_name === "Text Options") {
                if (kinds.includes('text'))
                    compatible_outputs[label] = href;
                kind = 'text';
            }
            // Include if matching kind
            if (UIBuilderView.matching_kind(kinds, href))
                compatible_outputs[label] = href;
            // Include if kinds blank and not text
            else if (kinds.length === 0 && kind !== 'text')
                compatible_outputs[label] = href;
        });
        // Add to the label -> value map
        if (Object.keys(compatible_outputs).length > 0)
            display_value_map[group_name] = compatible_outputs;
    }
    /**
     * Add markdown input files to the label -> value map
     *
     * @param display_value_map
     * @param target
     * @param kinds
     * @private
     */
    _add_markdown_files(display_value_map, target, kinds) {
        this._add_notebook_files(display_value_map, target, kinds, '.nbtools-markdown-file', 'Notebook Instructions');
    }
    /**
     * Add markdown text options to the label -> value map
     *
     * @param display_value_map
     * @param target
     * @param kinds
     * @private
     */
    _add_markdown_text(display_value_map, target, kinds) {
        this._add_notebook_files(display_value_map, target, kinds, '.nbtools-text-option', 'Text Options');
    }
    /**
     * Add UIOutput files to the label -> value map
     *
     * @param display_value_map
     * @param target
     * @param kinds
     * @private
     */
    _add_output_files(display_value_map, target, kinds) {
        const origins = this.supported_origins();
        const compatible_outputs = _context__WEBPACK_IMPORTED_MODULE_5__.ContextManager.data_registry.get_data({ kinds: kinds, origins: origins });
        if (Object.keys(compatible_outputs).length > 0) {
            for (let origin of Object.keys(compatible_outputs))
                display_value_map[origin] = compatible_outputs[origin];
        }
    }
    supported_origins() {
        // Get the list of supported origins for data
        let this_origin = this.model.get('origin');
        let accept_origins = this.model.get('accept_origins');
        // If supported origins is empty or undefined, accept same origins and "Notebook" by default
        if (accept_origins === null || accept_origins.length < 1) {
            accept_origins = [this_origin];
            if (this_origin !== 'Notebook')
                accept_origins.push('Notebook');
        }
        // Unless... if this origin is empty or undefined, accept all origins
        if (this_origin === null || this_origin.length < 1)
            accept_origins = [];
        // Otherwise, return the list
        return accept_origins;
    }
    _attach_kinds(attach_point) {
        const view = attach_point.widget;
        const model = view.model; // Get the model from the view
        const kinds = model.get('kinds') || ['text'];
        attach_point.setAttribute('data-type', kinds.join(', '));
    }
    _attach_name(attach_point) {
        let name = '';
        let param_element = null;
        let name_element = null;
        param_element = attach_point.closest('.nbtools-input');
        if (param_element)
            name_element = param_element.querySelector('div:first-child');
        if (name_element)
            name = name_element.textContent.replace(/\*/g, '');
        attach_point.setAttribute('data-name', name);
    }
    _attach_accept_origins(attach_point) {
        const origins = this.supported_origins();
        attach_point.setAttribute('data-origins', origins.join(', '));
    }
    /**
     * Attach sent to / come from menu support to the UI Builder widget
     *
     * @private
     */
    _attach_menus() {
        this.el.querySelectorAll('.nbtools-menu-attached').forEach((attach_point) => {
            this._attach_kinds(attach_point);
            this._attach_name(attach_point);
            this._attach_accept_origins(attach_point);
            attach_point.addEventListener("click", (event) => {
                // Get all compatible outputs and build display -> value map
                const display_value_map = this.build_display_map(attach_point);
                if (display_value_map === null)
                    return; // No view found, return
                // Update and attach the menu
                const target = attach_point.querySelector('input, select');
                this.attach_combobox_menu(target, display_value_map);
                // Attach the chevron to the input... or not
                this.update_chevron(attach_point, display_value_map);
            });
            // Initial menu attachment
            this.update_chevron(attach_point);
        });
    }
    build_display_map(attach_point) {
        const view = attach_point.widget; // Get widget view or abort
        if (!view)
            return null;
        const model = attach_point.widget.model; // Get the model from the view
        const sendto = !attach_point.classList.contains('nbtools-nosendto'); // Send if sendto enabled
        const kinds = model.get('kinds') || ['text']; // Get the list of compatible kinds
        // Build the map
        const display_value_map = {};
        this._add_default_choices(display_value_map, model);
        if (sendto)
            this._add_output_files(display_value_map, attach_point, kinds);
        if (sendto)
            this._add_markdown_files(display_value_map, attach_point, kinds);
        if (sendto)
            this._add_markdown_text(display_value_map, attach_point, kinds);
        return display_value_map;
    }
    update_chevron(attach_point, display_value_map = null) {
        if (!display_value_map)
            display_value_map = this.build_display_map(attach_point);
        if (Object.keys(display_value_map).length > 0)
            attach_point.classList.add('nbtools-dropdown');
        else
            attach_point.classList.remove('nbtools-dropdown');
    }
    toggle_file_menu(link, display_value_map) {
        const menu = link.nextElementSibling;
        const collapsed = menu.style.display === "none";
        // If the menu is empty, don't show it
        if (menu.childElementCount === 0)
            return;
        // Hide or show the menu
        if (collapsed)
            menu.style.display = "block";
        else
            menu.style.display = "none";
        // Hide the menu with the next click
        const hide_next_click = function (event) {
            if (link.contains(event.target))
                return;
            menu.style.display = "none";
            document.removeEventListener('click', hide_next_click);
        };
        document.addEventListener('click', hide_next_click);
    }
    /**
     * Create or update the menu based on the label -> value map
     *
     * @param target
     * @param display_value_map
     */
    attach_combobox_menu(target, display_value_map) {
        // Get the menu and empty it, if it exists.
        let menu = target.nextSibling;
        const menu_exists = menu && menu.classList.contains('nbtools-menu');
        if (menu_exists)
            menu.innerHTML = '';
        // Create and insert the menu, if necessary
        else {
            menu = document.createElement('ul');
            menu.classList.add('nbtools-menu', 'nbtools-file-menu');
            menu.style.display = 'none';
            target.parentNode ? target.parentNode.insertBefore(menu, target.nextSibling) : null;
        }
        // Iterate over display -> value map and insert menu items
        Object.keys(display_value_map).forEach((group) => {
            // Add the group label
            if (group !== 'Default Choices')
                this.add_menu_item(group, () => { }, 'nbtools-menu-header', menu, false);
            // Loop over all files in the group
            Object.keys(display_value_map[group]).forEach((display_name) => {
                this.add_menu_item(display_name, () => {
                    target.value = display_value_map[group][display_name];
                    target.dispatchEvent(new Event('change', { 'bubbles': true }));
                }, 'nbtools-menu-subitem', menu, false);
            });
        });
        this.toggle_file_menu(target, display_value_map);
    }
    /**
     * Get the kind based on a given URL
     *
     * @param url
     */
    static get_kind(url) {
        return url.split(/\#|\?/)[0].split('.').pop().trim();
    }
    static matching_kind(kinds, url) {
        let match = false;
        kinds.forEach((kind) => {
            if (url.trim().endsWith(kind))
                match = true;
        });
        return match;
    }
    /**
     * Attach a map of events to the given DOM element (widget or parameter)
     *
     * @param {HTMLElement} element
     * @param event_map
     * @private
     */
    _attach_all_events(element, event_map) {
        Object.keys(event_map).forEach((key) => {
            const str_func = event_map[key];
            const func = new Function(str_func);
            // Handle the load event as a special case (run now)
            if (key === 'load')
                func.call(this, new CustomEvent('load'));
            // Handle the run event as a special case (bind as click to the Run button)
            else if (key === 'run') {
                const run_button = element.querySelector('.jupyter-button');
                if (!!run_button)
                    run_button.addEventListener('click', func);
            }
            // Special case to handle focus events, which are swallowed by the Jupyter UI
            else if (key === 'focus')
                element.addEventListener('focusin', func);
            // Otherwise, attach the event
            else
                element.addEventListener(key, func);
        });
    }
    set_input_model(model, spec) {
        // Special case for DropdownModel
        if (model.name === 'DropdownModel') {
            const labels = Object.keys(spec['choices']);
            for (let i = 0; i < labels.length; i++) {
                const label = labels[i];
                const value = spec['choices'][label];
                if (value === spec['default']) {
                    model.set('index', i);
                    break;
                }
            }
        }
        else { // Otherwise just set the value traitlet
            model.set('value', spec['default']);
        }
        // Save the model
        model.save_changes();
    }
    has_advanced() {
        return !!this.element.querySelector('.nbtools-advanced');
    }
    toggle_advanced() {
        this.element.querySelectorAll('.nbtools-advanced').forEach((e) => {
            const hidden = !e.classList.contains('nbtools-advanced-show');
            if (hidden)
                e.classList.add('nbtools-advanced-show');
            else
                e.classList.remove('nbtools-advanced-show');
        });
    }
    reset_parameters() {
        const params = this.model.get('_parameters');
        for (let i = 0; i < params.length; i++) {
            const spec = params[i];
            const name = spec['name'];
            const param_element = this.element.querySelector(`[data-name='${name}']:not(.nbtools-input)`);
            if (!param_element) { // Protect against nulls
                if (name !== 'output_var')
                    console.log(`Error finding ${name} in reset_parameters()`);
                return;
            }
            const view = param_element.widget;
            this.set_input_model(view.model, spec);
            // Special case for file lists
            const all_inputs = param_element.parentNode ? param_element.parentNode.querySelectorAll('input') : [];
            if (all_inputs.length > 1) {
                let first = true;
                all_inputs.forEach((input) => {
                    if (first)
                        first = false;
                    else
                        input.value = '';
                });
            }
        }
    }
}


/***/ }),

/***/ "./lib/uioutput.js":
/*!*************************!*\
  !*** ./lib/uioutput.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "UIOutputModel": () => (/* binding */ UIOutputModel),
/* harmony export */   "UIOutputView": () => (/* binding */ UIOutputView)
/* harmony export */ });
/* harmony import */ var _style_uioutput_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../style/uioutput.css */ "./style/uioutput.css");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _basewidget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./basewidget */ "./lib/basewidget.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _dataregistry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./dataregistry */ "./lib/dataregistry.js");
/**
 * Widget for representing Python output as an interactive interface
 *
 * @author Thorin Tabor
 *
 * Copyright 2020 Regents of the University of California and the Broad Institute
 */







// noinspection JSAnnotator
class UIOutputModel extends _basewidget__WEBPACK_IMPORTED_MODULE_3__.BaseWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: UIOutputModel.model_name, _model_module: UIOutputModel.model_module, _model_module_version: UIOutputModel.model_module_version, _view_name: UIOutputModel.view_name, _view_module: UIOutputModel.view_module, _view_module_version: UIOutputModel.view_module_version, name: 'Python Results', description: '', status: '', files: [], text: '', visualization: '', appendix: undefined, extra_file_menu_items: {} });
    }
}
UIOutputModel.model_name = 'UIOutputModel';
UIOutputModel.model_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME;
UIOutputModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
UIOutputModel.view_name = 'UIOutputView';
UIOutputModel.view_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME;
UIOutputModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
UIOutputModel.serializers = Object.assign(Object.assign({}, _basewidget__WEBPACK_IMPORTED_MODULE_3__.BaseWidgetModel.serializers), { appendix: {
        deserialize: (value, manager) => (0,_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.unpack_models)(value, manager)
    } });
// noinspection JSAnnotator
class UIOutputView extends _basewidget__WEBPACK_IMPORTED_MODULE_3__.BaseWidgetView {
    constructor() {
        super(...arguments);
        this.dom_class = 'nbtools-uioutput';
        this.traitlets = [...super.basics(), 'status', 'files', 'text', 'visualization'];
        this.renderers = {
            "description": this.render_description,
            "error": this.render_error,
            "info": this.render_info,
            "files": this.render_files,
            "visualization": this.render_visualization
        };
        this.body = `
        <div class="nbtools-description" data-traitlet="description"></div>
        <div class="nbtools-error" data-traitlet="error"></div>
        <div class="nbtools-info" data-traitlet="info"></div>
        <div class="nbtools-status" data-traitlet="status"></div>
        <div class="nbtools-files" data-traitlet="files"></div>
        <pre class="nbtools-text" data-traitlet="text"></pre>
        <div class="nbtools-visualization" data-traitlet="visualization"></div>
        <div class="nbtools-appendix"></div>`;
        this.file_cache = [];
    }
    render() {
        super.render();
        // Add the child widgets
        this.attach_child_widget('.nbtools-appendix', 'appendix');
    }
    remove() {
        super.remove();
        // Clean up data files from the cache
        for (let f of this.file_cache)
            _context__WEBPACK_IMPORTED_MODULE_5__.ContextManager.data_registry.unregister({ data: f });
    }
    sync_file_cache() {
        // Unregister old files associated with this widget
        for (let f of this.file_cache)
            _context__WEBPACK_IMPORTED_MODULE_5__.ContextManager.data_registry.unregister({ data: f });
        // Create the data objects and add them to the file cache
        this.file_cache = [];
        const origin = this.model.get('origin');
        for (let f of this.model.get('files'))
            this.file_cache.push(new _dataregistry__WEBPACK_IMPORTED_MODULE_6__.Data(origin, f));
        // Register the files currently associated with this widget
        for (let f of this.file_cache)
            _context__WEBPACK_IMPORTED_MODULE_5__.ContextManager.data_registry.register({ data: f });
    }
    render_files(files, widget) {
        // Sync the file cache with what is displayed
        widget.sync_file_cache();
        let to_return = '';
        files.forEach(path => {
            const name = (0,_utils__WEBPACK_IMPORTED_MODULE_4__.extract_file_name)(path);
            const type = (0,_utils__WEBPACK_IMPORTED_MODULE_4__.extract_file_type)(path);
            const path_prefix = UIOutputView.pick_path_prefix(path);
            to_return += `<a class="nbtools-file" href="${path_prefix}${path}" data-type="${type}" onclick="return false;">${name} <i class="fa fa-info-circle"></i></a>`;
            to_return += `<ul class="nbtools-menu nbtools-file-menu" style="display: none;"></ul>`;
        });
        setTimeout(() => widget.initialize_file_menus(widget), 100);
        return to_return;
    }
    render_visualization(visualization, widget) {
        // Function for toggling pop out menu item on or off
        function toggle_open_visualizer(hide) {
            const controls = widget.element.querySelector('.nbtools-controls');
            if (!controls)
                return; // Get the gear menu buttons at the top and protect against null
            // Toggle or set the Pop Out Visualizer menu option's visibility
            controls.querySelectorAll('.nbtools-menu > li').forEach((item) => {
                if (item.textContent.includes('Pop Out Visualizer')) {
                    if (hide)
                        item.style.display = 'none';
                    else
                        item.style.display = 'block';
                }
            });
        }
        // Hide or show the open visualizer menu option, depending on whether there is a visualization
        if (!visualization.trim())
            toggle_open_visualizer(true);
        else
            toggle_open_visualizer(false);
        // If URL, display an iframe
        if ((0,_utils__WEBPACK_IMPORTED_MODULE_4__.is_url)(visualization))
            return `<iframe class="nbtools-visualization-iframe" src="${visualization}"></iframe>`;
        // Otherwise, embed visualization as HTML
        else
            return visualization;
    }
    traitlet_changed(event) {
        const widget = this;
        const name = typeof event === "string" ? event : Object.keys(event.changed)[0];
        const elements = this.element.querySelectorAll(`[data-traitlet=${name}]`);
        elements.forEach(element => {
            // Ignore traitlets in the appendix, unless this is a subwidget in the appendix
            if (!this.element.closest('.nbtools-appendix') && element.closest('.nbtools-appendix'))
                return;
            if (name in this.renderers)
                element.innerHTML = this.renderers[name](this.model.get(name), widget);
            else
                element.innerHTML = this.model.get(name);
        });
    }
    static pick_path_prefix(path) {
        if ((0,_utils__WEBPACK_IMPORTED_MODULE_4__.is_url)(path))
            return ''; // is a URL
        else if ((0,_utils__WEBPACK_IMPORTED_MODULE_4__.is_absolute_path)(path))
            return ''; // is an absolute
        else
            return 'files/' + _context__WEBPACK_IMPORTED_MODULE_5__.ContextManager.context().notebook_path(); // is relative path
    }
    attach_menu_options() {
        // Attach the Open Visualizer gear option
        const visualizer_option = this.add_menu_item('Pop Out Visualizer', () => this.open_visualizer());
        visualizer_option.style.display = this.model.get('visualization').trim() ? 'block' : 'none';
        // Call the base widget's attach_menu_options()
        super.attach_menu_options();
    }
    open_visualizer() {
        window.open(this.model.get('visualization'));
    }
    initialize_file_menus(widget) {
        const files = widget.el.querySelectorAll('.nbtools-file');
        files.forEach((link) => {
            link.addEventListener("click", function () {
                widget.toggle_file_menu(link);
            });
        });
    }
    initialize_menu_items(link) {
        const menu = link.nextElementSibling;
        if (!menu)
            return; // Protect against null
        const type = link.getAttribute('data-type');
        const href = link.getAttribute('href');
        const file_name = link.textContent ? link.textContent.trim() : href;
        const widget_name = this.model.get('name');
        const origin = this.model.get('origin') || '';
        // Add the send to options
        let send_to_empty = true;
        this.get_input_list(type, origin).forEach(input => {
            send_to_empty = false;
            this.add_menu_item(input['name'] + ' -> ' + input['param'], () => {
                const form_input = input['element'].querySelector('input');
                form_input.value = href;
                form_input.dispatchEvent(new Event('change', { bubbles: true }));
                const widget = form_input.closest('.nbtools');
                widget.scrollIntoView();
            }, 'nbtools-menu-subitem', menu);
        });
        // Add send to header
        if (!send_to_empty)
            this.add_menu_item('Send to...', () => { }, 'nbtools-menu-header', menu);
        // Add the extra menu items
        const menu_items = this.model.get('extra_file_menu_items');
        const template_vars = {
            'widget_name': widget_name,
            'file_name': file_name,
            'href': href,
            'type': type
        };
        Object.keys(menu_items).forEach((name) => {
            const item = menu_items[name];
            // Skip if this file doesn't match any type restrictions
            if (item['kinds'] && Array.isArray(item['kinds']) && !item['kinds'].includes(type))
                return;
            // Create the callback and attach the menu item
            const callback = this.create_menu_callback(item, template_vars);
            this.add_menu_item(name, callback, 'nbtools-menu-subitem', menu);
        });
        // Add download and new tab options
        this.add_menu_item('Copy Link', () => navigator.clipboard.writeText((0,_utils__WEBPACK_IMPORTED_MODULE_4__.get_absolute_url)(link.getAttribute('href'))), '', menu);
        this.add_menu_item('Download', () => window.open(link.getAttribute('href') + '?download=1'), '', menu);
        this.add_menu_item('Open in New Tab', () => window.open(link.getAttribute('href')), '', menu);
    }
    toggle_file_menu(link) {
        const menu = link.nextElementSibling;
        const collapsed = menu.style.display === "none";
        // Build the menu lazily
        menu.innerHTML = ''; // Clear all existing children
        this.initialize_menu_items(link);
        // Hide or show the menu
        if (collapsed)
            menu.style.display = "block";
        else
            menu.style.display = "none";
        // Hide the menu with the next click
        const hide_next_click = function (event) {
            if (link.contains(event.target))
                return;
            menu.style.display = "none";
            document.removeEventListener('click', hide_next_click);
        };
        document.addEventListener('click', hide_next_click);
    }
    get_input_list(type, origin) {
        // Get the notebook's parent node
        const notebook = this.el.closest('.jp-Notebook');
        // Get all possible outputs
        const parameters = [...notebook.querySelectorAll('.nbtools-menu-attached')];
        // Build list of compatible inputs
        const compatible_inputs = [];
        parameters.forEach((input) => {
            // Ignore hidden parameters
            if (input.offsetWidth === 0 && input.offsetHeight === 0)
                return;
            // Ignore parameters with sendto=False
            if (input.classList.contains('nbtools-nosendto'))
                return;
            // Ignore if this origin does not match the supported origins
            const origins_str = input.getAttribute('data-origins') || '';
            const origins_list = origins_str.split(', ');
            if (!origins_list.includes(origin) && origins_str !== '')
                return;
            // Ignore incompatible inputs
            const kinds = input.getAttribute('data-type') || '';
            const param_name = input.getAttribute('data-name') || '';
            const kinds_list = kinds.split(', ');
            if (!kinds_list.includes(type) && kinds !== '')
                return;
            // Add the input to the compatible list
            const widget_element = input.closest('.nbtools');
            let name = widget_element.querySelector('.nbtools-title').textContent;
            if (!name)
                name = "Untitled Widget";
            compatible_inputs.push({
                'name': name,
                'param': param_name,
                'element': input
            });
        });
        return compatible_inputs;
    }
}


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "send_notification": () => (/* binding */ send_notification),
/* harmony export */   "is_absolute_path": () => (/* binding */ is_absolute_path),
/* harmony export */   "is_url": () => (/* binding */ is_url),
/* harmony export */   "get_absolute_url": () => (/* binding */ get_absolute_url),
/* harmony export */   "extract_file_name": () => (/* binding */ extract_file_name),
/* harmony export */   "extract_file_type": () => (/* binding */ extract_file_type),
/* harmony export */   "element_rendered": () => (/* binding */ element_rendered),
/* harmony export */   "show": () => (/* binding */ show),
/* harmony export */   "hide": () => (/* binding */ hide),
/* harmony export */   "toggle": () => (/* binding */ toggle),
/* harmony export */   "process_template": () => (/* binding */ process_template),
/* harmony export */   "pulse_red": () => (/* binding */ pulse_red)
/* harmony export */ });
/**
 * Send a browser notification
 *
 * @param message
 * @param sender
 * @param icon
 */
function send_notification(message, sender = 'nbtools', icon = '') {
    // Internal function to display the notification
    function notification() {
        new Notification(sender, {
            body: message,
            badge: icon,
            icon: icon,
            silent: true
        });
    }
    // Browser supports notifications and permission is granted
    if ("Notification" in window && Notification.permission === "granted") {
        notification();
    }
    // Otherwise, we need to ask the user for permission
    else if ("Notification" in window && Notification.permission !== "denied") {
        Notification.requestPermission(function (permission) {
            // If the user accepts, let's create a notification
            if (permission === "granted") {
                notification();
            }
        });
    }
}
/**
 * Determines ia a given string is an absolute file path
 *
 * @param path_or_url
 * @returns {boolean}
 */
function is_absolute_path(path_or_url) {
    let path_exp = new RegExp('^/');
    return path_exp.test(path_or_url);
}
/**
 * Decides if a string represents a valid URL or not
 *
 * @param path_or_url
 * @returns {boolean}
 */
function is_url(path_or_url) {
    const url_exp = new RegExp('^(?:http|ftp)s?://');
    return url_exp.test(path_or_url);
}
function get_absolute_url(url) {
    try {
        return new URL(url).href;
    }
    catch (e) {
        return new URL(url, document.baseURI).href;
    }
}
/**
 * Extracts a file name from a URL
 *
 * @param path
 * @returns {*}
 */
function extract_file_name(path) {
    if (is_url(path))
        return path.split('/').pop();
    else
        return path;
}
/**
 * Extracts a file type from a path or URL
 *
 * @param {string} path
 * @returns {any}
 */
function extract_file_type(path) {
    return path.split('.').pop().trim();
}
/**
 * Wait until the specified element is found in the DOM and then execute a promise
 *
 * @param {HTMLElement} el
 */
function element_rendered(el) {
    return new Promise((resolve, reject) => {
        (function element_in_dom() {
            if (document.body.contains(el))
                return resolve(el);
            else
                setTimeout(element_in_dom, 200);
        })();
    });
}
/**
 * Show an element
 *
 * @param {HTMLElement} elem
 */
function show(elem) {
    // Get the natural height of the element
    const getHeight = function () {
        elem.style.display = 'block'; // Make it visible
        const height = elem.scrollHeight + 'px'; // Get it's height
        elem.style.display = ''; //  Hide it again
        return height;
    };
    const height = getHeight(); // Get the natural height
    elem.classList.remove('nbtools-hidden'); // Make the element visible
    elem.style.height = height; // Update the height
    // Once the transition is complete, remove the inline height so the content can scale responsively
    setTimeout(function () {
        elem.style.height = '';
        elem.classList.remove('nbtools-toggle');
    }, 350);
}
/**
 * Hide an element
 *
 * @param elem
 * @param min_height
 */
function hide(elem, min_height = '0') {
    elem.classList.add('nbtools-toggle');
    // Give the element a height to change from
    elem.style.height = elem.scrollHeight + 'px';
    // Set the height back to 0
    setTimeout(function () {
        elem.style.height = min_height;
    }, 10);
    // When the transition is complete, hide it
    setTimeout(function () {
        elem.classList.add('nbtools-hidden');
    }, 350);
}
/**
 * Toggle element visibility
 *
 * @param elem
 * @param min_height
 */
function toggle(elem, min_height = '0') {
    // If the element is visible, hide it
    if (!elem.classList.contains('nbtools-hidden')) {
        hide(elem, min_height);
        return;
    }
    // Otherwise, show it
    show(elem);
}
function process_template(template, template_vars) {
    Object.keys(template_vars).forEach((key_var) => {
        template = template.replace(new RegExp(`{{${key_var}}}`, 'g'), template_vars[key_var]);
    });
    return template;
}
function pulse_red(element, count = 0, count_up = true) {
    setTimeout(() => {
        element.style.border = `rgba(255, 0, 0, ${count / 10}) solid ${Math.ceil(count / 2)}px`;
        if (count_up && count < 10)
            pulse_red(element, count + 1, count_up);
        else if (count_up)
            pulse_red(element, count, false);
        else if (count > 0)
            pulse_red(element, count - 1, count_up);
        else
            element.style.border = `none`;
    }, 25);
}


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
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

/***/ "./style/g2nb_logo.png":
/*!*****************************!*\
  !*** ./style/g2nb_logo.png ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (__webpack_require__.p + "6b8c90c7eb68fb0a698ade6fa7df2e33.png");

/***/ }),

/***/ "./style/icon.svg":
/*!************************!*\
  !*** ./style/icon.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 166.53 166.53\"><defs><style>.cls-1{isolation:isolate;}.cls-2{stroke:#dbdcdd;stroke-miterlimit:10;stroke-width:2.43px;fill:url(#linear-gradient);}.cls-3{fill:#534f97;}.cls-4{mask:url(#mask);}.cls-5{opacity:0.25;mix-blend-mode:multiply;}.cls-6{fill:#020202;}.cls-7{fill:#ec1c24;}.cls-8{mask:url(#mask-2);}.cls-9{mask:url(#mask-3);}.cls-10{mask:url(#mask-4);}.cls-11{mask:url(#mask-5);}.cls-12{mask:url(#mask-6);}.cls-13{mask:url(#mask-7);}.cls-14{mask:url(#mask-8);}.cls-15{mask:url(#mask-9);}.cls-16{filter:url(#luminosity-invert);}</style><linearGradient id=\"linear-gradient\" x1=\"582.21\" y1=\"458.05\" x2=\"582.21\" y2=\"622.15\" gradientTransform=\"matrix(-1, 0, 0, 1, 665.48, -456.63)\" gradientUnits=\"userSpaceOnUse\"><stop offset=\"0\" stop-color=\"#ededee\"/><stop offset=\"0.18\" stop-color=\"#fff\"/><stop offset=\"0.63\" stop-color=\"#fff\"/><stop offset=\"0.63\" stop-color=\"#fff\"/><stop offset=\"1\" stop-color=\"#dbdcdd\"/></linearGradient><filter id=\"luminosity-invert\" filterUnits=\"userSpaceOnUse\" color-interpolation-filters=\"sRGB\"><feColorMatrix values=\"-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0\"/></filter><mask id=\"mask\" x=\"11.57\" y=\"11.37\" width=\"43\" height=\"43\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"43\" transform=\"translate(888 468)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAArCAYAAADhXXHAAAAACXBIWXMAAAsSAAALEgHS3X78AAADHElEQVRYR+3Z70vyXBzH8feOc83csJImPREkoSfW//+HRNCDSirRTHDq5tL9uh/cnHPNOa4Lo5xBHxio5zhenB+DfY8GpPyQiH91OKTo+R+63S6tVgvbtjEMg2q1ihACTdPQNK3oHp9Omv4/qUmSEMcxURSxWq2Yz+eMx2MeHx83+m9gb25u6PV6tNttms0mlmVhGAaVSgUhhELL7IqXuOz3PNTzPN7f33l9feX4+Jjb21vVX2G73S69Xo/r62s6nQ6O42DbNqZpbmBldoXKZMFpmpKmKXEcE4YhQRAwn895e3vj9PSUNE0JgoCHhwcgg221WrTbbTqdDpeXlziOszWy8HlkUbLYOI7VErAsCyEEruvy8vKyjbVtm2azieM4OI7D+fk5pml+Ke5fSZIE0zQB8H2fs7MzbNtW7WpeDcPAsixs28ayrL1DAYQQ1Ot1ZZAzq9rlh2q1imEYmKaJYRh7h8oIITg6OlIOXf/zDFBYIQSVSkVdZUYIga7r6Lq+YVFYTdPUjs/u+jKSfUxmZ7gQW3YkNP9c35DJhrLWazZFlvKHcYdsYQ9hVGXylsJlcAgpsvzsZXDI+cV+V36x35Vf7HflF/td+bnY/Ht9mSmybI3sIYHzOehlkB+4g8bCJlhhZXVEXmUmSZJCxwY2jmPVsczIgl0erLCymievMpMkifIUYqMoIgxD1us1URQV3mRfieNYObIWhV2v1wRBgO/7BEFQGliWPoMg4OPjoxi7XC5xXZfpdMpsNsPzvL2DwzBksVjgui6u6+J5HqvVSrWrqtdoNGIwGNBqtajX66RpSqPRwDRNdF1XlZqvrNjITZQkCVEUEQQBs9mM4XDIaDRiMpngeZ7qr7D39/dcXFxg2zaapuH7PicnJ9RqNVVQzteedn11/1uZfr1es1wumU6njEYjnp6eeH5+Zjweq/4bZwr9fh+AxWLBYDCg0WhQq9WoVqtb2F2hMvkyffZMYblcMp/PGQ6H9Pt9+v3+xiGIRsE52NXVlVoOEiqx8HloNhKdLdOHYYjv+0wmE+7u7rb+U4g91HzdbtlD/gNw/7gOVEqcSgAAAABJRU5ErkJggg==\"/></g></g></mask><mask id=\"mask-2\" x=\"61.57\" y=\"11.37\" width=\"43\" height=\"43\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"43\" transform=\"translate(938 468)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAArCAYAAADhXXHAAAAACXBIWXMAAAsSAAALEgHS3X78AAADIElEQVRYR+3Z7UvyUBjH8e+O0023NYtIfRX26Mv+/78jgqBCqIGpkK3pdO7hfhHntJlxc3eXLugHB9Rdjo9nZwe8pgEZPyTibwVlir76Qbfbpd1uY9s2pmmi6zqVSgUhXn+XpmnvTvLZZNnrRU3TlCRJiOOYxWKB7/sMh0Pu7u4K9QXsyckJFxcXHB4esr+/j+M4GIZBtVpFCIEQooD9V7jE5d+vQoMgYDQa8fDwQKPR4PLyUtUXsN1ul16vx+npKZ1Oh52dHer1usJqmqaA/wqVyYOzLCPLMpIkYblcEoYhvu/z+PjI7u4uWZYRhiG3t7dADtvr9Tg7O+Po6Ijj42Pa7Tau62IYBrquK+hnkeuSxyZJopaAbdsIIZhMJtzf37/HttttNVqtFgcHB1iWpdbqJpKmKaZpAjCdTtnb28NxHHVcSSzLwnVdms0mrutuHAoghMCyLBzHwbZtbNumVqu9HZcvqtUqpmnSaDQwDGPjUBkhBIZhYJomtVoNXX+7rZRI13Wq1aoa24wQAl3X1bapPs8XVCoVKpXKl95En0l+m8xbCtd6XcE2Ih2r+7rC5rembWPhbR//cGbLnnfYMsyqzKqlgC0zFH76MihzfrHflV/sd+UX+135xX5Xfi529X992fJuZssCXuco9TJYBZcaC0WwwsruiBzbTJqmax0FbJIkqnCb+WjiFFZ28+TYZvKWtdg4jlkul0RRRBzHa0+yqSRJQhRFqhUqo7BRFBGGIdPplDAMtwaO45j5fM58PicMw8JVVtjZbMZkMuHp6Ynn52eCINg4OI5jgiDA931832c2m7FYLNRx1fUaDAZ4nker1cKyLLIsw3Vd1aqXjbqvbNjJm1mu0fl8ju/7DAYDhsMh4/GYIAhUvcJeX1/T6XRwHAdN05hOpzSbTer1OrVaTfXA/qdNDx93vqMoUtjhcEi/38fzPEajkaovtOn7/T4ALy8veJ6H67qqTb+K/QxURoJXO99hGDKbzRiPx3iex9XVFTc3N+p7Gmueg52fn6vlIKH57uL/QGVWwXEcq1a9fAiSh8IH2LLm6+6WDeQP81+8EyzgnHEAAAAASUVORK5CYII=\"/></g></g></mask><mask id=\"mask-3\" x=\"111.57\" y=\"11.37\" width=\"43\" height=\"43\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"43\" transform=\"translate(988 468)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAArCAYAAADhXXHAAAAACXBIWXMAAAsSAAALEgHS3X78AAADJElEQVRYR+3ZS0/qQByH4Zeh0NKLFUMQVwYVw9Lv/yXcGDdeolEiAkbSlN5o6VmYjqViTo5HoCb+kibQGZqHYWYS/lMBUn5IxN86lClK8Ua326XT6WCaJpqmoSgK1WoVId6+V6VS+fCQryZN337UxWJBkiTEcUwYhjiOw2g04vb2dqn/Evbk5ISzszMODw9ptVpYloWqqtRqNYQQCCGWsP8Kz3D590Wo67qMx2MeHx/RdZ2LiwvZfwnb7Xbp9/v0ej0ODg7Y2dmh0WhIbKVSkcB/hWbJg9M0JU1TkiRhPp/j+z6O4/D8/Eyz2SRNU3zf5+bmBshh+/0+p6enHB0dcXx8TKfTwbZtVFVFURQJ/SpyVfLYJEnkFDBNEyEE0+mUh4eHj9hOpyOv/f192u02hmHIubqJLBYLNE0DYDabsbe3h2VZsl1KDMPAtm12d3exbXvjUAAhBIZhYFkWpmlimib1ev29PXtRq9XQNA1d11FVdePQLEIIVFVF0zTq9TqK8r6spEhRFGq1mry2GSEEiqLIbVPez3eoVqtUq9VvXURfSX6bzFuWfutVHbaRzFHc1yU2vzVtGwvv+/inI1v2fMCWYVSzFC1L2DJD4adPgzLnF7uu/GLXlV/suvKLXVd+Lrb4v75s+TCyZQGvcpR6GhTBpZ8GeZPEZnWnrEqyzXzmWMLmwdtMZimCJTZfzYvjeOVDNpXMkiTJamwcx0RRRBRFW8cmSUIURXLwskhsGIbMZjNc18X3/a2B4zgmCAKCIMD3fZIkkW0S63ke0+mUl5cXXl9fcRyH+Xy+8oHrShzHuK6L4zg4joPneYRhKNtl1evp6Yn7+3tarRaGYZCmKUEQyFJ9vkryXckWczZHgyDAcRyGwyGj0YjJZILrurK/xF5dXWGaJo1GA3ivj+q6Tr1el+cK/1Omh88r31EUSexoNOLu7o7BYMB4PJb9l8r05+fnsjQ+HA5pNpsSWzxT+Ao0SwYuVr5938fzPCaTCYPBgMvLS66vr+XnKqw4B+v1erTbbSzLkqOary7+DzRLERzHsSzVZ4cgeSh8gi1rvm+1bCB/AOUnxFb7yBLGAAAAAElFTkSuQmCC\"/></g></g></mask><mask id=\"mask-4\" x=\"11.57\" y=\"61.37\" width=\"43\" height=\"44\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"44\" transform=\"translate(888 518)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAsCAYAAAD8WEF4AAAACXBIWXMAAAsSAAALEgHS3X78AAAD/ElEQVRYR+2Z60/yPADFT9l9QwbjEkXMo1/w//9/jEExTHSMwZizu5T3w5M2Gwx8NC+giSdpGFm7/XLWS3pKAKzxQ1T7qMJ3krzv5s3NDdrtNkzThCzLkCQJhBAQQgBA/P6r1ut16ZoxBsYYkiQBpRSz2Qz39/c72xNsdIPBYIButwvHcTAYDOA4Dur1OjRNgyzLqNVqqNX+fpAi7C7wIiD/z0ue58iyDJRSRFEEz/Pgui5838fLywuenp5KbUvOXl9f4/b2FldXV7i4uECv10Or1RKwiqJAkiTUarVPu8uhOShjDHmeI01TUEoRhiGCIMDr6ytc18V4PIYsyxiNRuIZArbf72M4HGI4HOL6+hqXl5fodrtoNBqo1+tQVRWKoghn/8VVrs3PX3SWw0ZRhMVigW63C9u2oes6GGOglMJ1XQAFWMdxcH5+jsFggD9//qDf76PT6YiGXwUtquguADDGkGUZsixDHMewbRumaUKSJKRpiiAI4LruNqxlWXAcB51OB71eD71eD+12G5ZlQZblT0F9RpqmYb1ewzAMqKoKQgiSJEEQBGg2mzAMQ9QVsJqmwbIsNBoN2LYN27ZhWRYURal8yf8pQghUVUW9XkeapgjDEI1GA6ZpQlVVUU/Ms5IkQdM0GIYBwzDEgDqmFEWBruswDAO6rovux1WCVRRFQB4bFPjrsCzL4v18quQSV3zwSJK0VemYkiSpxFAJSwgRNzdH/DFFCBFz+SZHyT6+lBaX1GNrH8NO2FOriqXUDTYrn0q73r01ir6Ts5va6gan1j6G08xPX9Qv7KH0C3so/cIeSj8XdnPb/N1U6ewpoTc3lUVtwe6rfGoJ2O8Et4tlq8/ycmpVcZSc3Syn0D6OkrM81WOMnRQ2z/P9sDwo43EOY6zyYYdWnuciVto0rQSbZRmSJEGapkjTtPJhhxYP66pME7A8J43jGHEcg1KKLMsqH3gocbMopaCUIkkS5Hku7gtYHjuGYYjlcokwDPH29nY04DzPEccxVquVKHEcI0kSUUcEc1EUYT6fYzabodVqQdd1AECapiJS4qED3yd9dc9WXHj4WHl/f8dqtUIQBPB9H/P5HIvFAnEci3YC1vd9TKdTcYZACAGlFKvVSgR1xdT7q8BVoPzTL5dLeJ6H5+dnTKdTeJ4H3/dFWwE7mUxgmiYURcF6vUYcxwiCAGdnZyI75flTVQDxEXRxVPMpqRjV8y7g+z4mkwlGoxEeHx8xHo9Fu9KZwt3dHRhjSNMUi8UCzWazdPhRzKCAjwF3iYPywgdWFEUIggDT6RQPDw8i8ebaOq0BIE5pLMsqOfqVg48qFbsCXwTyPBezked5Wyc1wA7Y76oftVP4D/nsfMMRIRpaAAAAAElFTkSuQmCC\"/></g></g></mask><mask id=\"mask-5\" x=\"61.57\" y=\"61.37\" width=\"43\" height=\"44\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"44\" transform=\"translate(938 518)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAsCAYAAAD8WEF4AAAACXBIWXMAAAsSAAALEgHS3X78AAAD8UlEQVRYR+2Z626qQBSF1wgoN294SWttav/Y93+fJk1tarEpIMqdAc6PZiao1HNsjqVN+iVEExnmy5LZhD0EQIEfQuNvJ3wnxGM/3t7eYjAYQFVViKIIQRBACAEhBAD45ykURcE/i6JAnufIsgxJkiAIAti2jcViUTn2QHY6nWI0GsEwDEynUxiGAV3X0Wq1IIoiGo0GGo33P6Qse0ycCbLvVaJhGGKz2cC2bUwmEyyXywPpHdnZbIa7uztcX1/j8vIS4/EY/X6fy0qSBEEQ0Gg0Tk53P9GiKJBlGdI05am6rgvLsjAcDmEYBgRBwMPDA78Gl51MJpjP55jP55jNZri6usJoNEKn04Gu62g2m5AkiSf7r6kCx5NlsmEYwnVdvL29Qdd1iKIISimiKMLLywuAkqxhGLi4uMB0OsXNzQ0mkwmGwyG63S5kWf60aJl96TzPuXAURWi321AUBYQQRFEEx3GwXC4PZTVNg2EYGA6HGI/HGI/HGAwG0DQNoiieJHUqsixDURRIkgRCCOI4xnq9Rq/Xg6qq/Dwu22q1oGkaOp0Out0uut0uNE2DJEmVE/xPCCGQJAm6riNNU7TbbbTbbaiqimazyc/jdVYQBLRaLSiKAkVR+IL6SkRRhCzL/GAViLEjK0kSl/xqUeA9YeYhiiKv7QwuyxaPIAi8ntaBIAjcgT2EGNyIEMKF91f8V8LSZQ6VsuzE8lEHxxw+lK2bKped22D/5Lr4aO6DVfSdkt3n4Daom2MO9dSnT/Irey5+Zc/Fr+y5+Lmy5Xek70hlsnVKH5v7QLb8fl8nVfNz2brlynzkcnDPsqNuqjx2kt0/6uCYx06yrEOS53mtsmz+D2VZR49SCkop8jyvvNi5KYqCe+yHtiNLKUWSJEjTFGmaVl7s3LCwKKXIsqxallKKOI4RhiHCMEQcx6CUVl7wXLCw4jjmoWVZxn/nsnEcw/d9bLdbbDYbbLdbBEHwZcJZliEMQwRBAN/3EQQBoija+Yd5I8n3fTiOA8uy0O/3IcsyACBNU95S2m88fPadrfzgYWsliiL4vg/btuE4DlzXhed5SJKEj+Oytm1jtVrxPQRC3luPnufxRl1Vp+RU4X3RPM+RJAmiKMJ2u4VlWTBNE6+vr3AcB57n8bFcdrlcQlVVSJKEoigQhiHW6zVv8DabTd4Dq2pA/E26vFBYSWKpsmay53lwHAemaeLx8RHPz89Yr9d83M6ewv39Pe9Eu66LXq+3s/nBkq3aADmFci1lZSpJEvi+j81mg9VqhcViAdM0YZomH0dQsWnHdmk0TdtJ9DMbHx9RLvpZliHLMl6NLMvC09PTwZhK2e/Kj3pT+AOtZ3ePHu+txgAAAABJRU5ErkJggg==\"/></g></g></mask><mask id=\"mask-6\" x=\"111.57\" y=\"61.37\" width=\"43\" height=\"44\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"44\" transform=\"translate(988 518)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAsCAYAAAD8WEF4AAAACXBIWXMAAAsSAAALEgHS3X78AAADaUlEQVRYR+2Z207qWhRAR0tLuRUFKUjUuNWowcQH//8jTHwwJiImJhKwQcDQQu/nqWsXqR73ORutiSNZCem6dDA7VwNzSUDEN0H+twFZQnmv8/z8nGazSalUQlEUFEVBkiQkSXpv2oeIokg03/fxPI/ZbMZwOOTm5iZ1jsSrNDg+PmZnZwfDMDg4OKDRaKDrOvl8nlwuhyzLyLK8JPwR+ShazrYoigiCgDAM8TyPxWLBZDLBNE16vR739/dcX18vzVmK7MnJCRcXF0K43W5Tr9cpl8vk83kRWVn+nT0fEY1JCkdRRBiGBEGA7/vYts1sNsM0TdrtNoZhoCgKV1dXYs6S7OHhIZ1Oh06nw+7uLs1mE13XKRQKKIpCLpf762kQBAFBEOB5HpZlYRiGeJLxl+h2u0BC9uzsjKOjI379+sX+/j57e3tsbGxQLBaXIrlOdF0X93McB9M0abVaq7KtVot2u0273abValGr1SgWi28uvA7y+Tybm5s4jsPW1hb1ep1KpSL6RchKpRLVapVqtUqlUqFQKKQuuG5UVaVUKlEul8VeiRGyqqpSKBQoFotomvZX8vK/oigKmqahqiqK8ntbCVlFUVBVdWXAVyDLMrlcTjRxPf4gSZLo/MqoAuL1+Pp9viQbd3617FseS7LJlhVSI/sdyKzsu2nw1oAskdnIpvEjuy5+ZNfFj+y6+JFdF99X9vV/+6yxEtksC2c2DdKClllZWBVeydm4ZYWki5CNa09ZEI093oxsLBu3ryT5hFMjm6zoBUGQushnkSyHpsp6nofjOCwWC1zXTV3ks/B9XxSYk4ETsq7rYlkWlmUxn8/xPC91oXXj+z6O42DbNq7rLnkI2ZeXF0ajEaPRiOfnZ15eXj49wkEQYFkW0+mU6XS64iCKWk9PTzw+PrK9vU25XEaSJBzHoVQqoaqqKNHDn1W73yPeQGEY4vs+8/mc6XTKYDBgOByKoMUI2W63i67raJpGGIbYtk2j0aBSqaBp2tJ5Avx/4eRuT1a+x+Mx/X6fu7s7er0epmmKOUvlwsvLS8IwxHVdxuMxtVpN1EiTRbs/PfxIknauEG+m+XzOZDKh3+9ze3vLw8MDvV5PjF85rQE4PT3FMAyq1aoog66jaPc6DVzXxbZtBoNB6vFSqmxWyfQPmdf8A6NKyy8g/AoLAAAAAElFTkSuQmCC\"/></g></g></mask><mask id=\"mask-7\" x=\"11.57\" y=\"112.37\" width=\"43\" height=\"43\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"43\" transform=\"translate(888 569)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAArCAYAAADhXXHAAAAACXBIWXMAAAsSAAALEgHS3X78AAADkUlEQVRYR+2Za2vqShRAV4xmjAY1FRGlQvvB//+PCgVp00iNtXl08ryfZoivHm971B7oAjHoTGa5ndk6ewyg4h+h8acGP4nm7gvT6ZThcEin00EIQbPZpNFo0Gg0MAwDQD9/laqq9HNVVZRlSVEUZFlGmqa8v7+zXq/xPG+r35bs3d0d8/mcyWSC67o4joMQglarhWmaGIahH4pTxZWgut4VTdOUJEmIoojVaoXneQgheHx81P207HQ6ZT6fM5/Pmc1mjEYj+v0+tm0jhMA0TR3dXeFT2Y1oVVU6olJK4jhmvV6zXC5xHAcAKaWOsJYdDodMJhNmsxn39/eMx2Nc18W2bSzL0tOhLvp/hQ/JlmVJmqZIKQnDkPV6TafTASAMQ15eXvZlO50OrusyGo0Yj8dMJhMGg4GW/a6ooi4MUJYleZ6TpilRFNFutynLkjiO8TxPi0NNVgiB4zj0+31c12UwGDAYDLAs68tipyKEoN1u02q1AIjjmF6vR7fbxbIs3U7LNptNhBDYtq0flxBVmKaJbdukaYrjONi2vfUBoJZnG40GrVYLIQSWZV1UVGGaph7bsiydhRRbsqZpYpqmXkzXQI3fbDZ1BlLoK7V4dn8ALo0av54q9Xv1hvUcei3ZzwK2F9lriiqOpci9ifndPPo3ORrZzxpdmmPj783Za/PZN3ud/PRFfmXPxa/sufiVPRe/sudiS7a+Xb4Wu3u0OnuRVbvOn8jRaXBN4WNja9n6Xv6aoopDHntz9trCuw51j73IlmV5NVFAl5T+KFsUhS6UlWV58GbnRo2d5/le4LRsURS6mpemKXmeH7zZOVEBy7KMPM+1sGJLNk1TPj4+kFIipaQoioM3PRd5nuuxpZTHZaWURFFEGIZsNhvCMCSKootEuKoqsiwjjmPCMNRjJ0lClmW6na51JUnC29sbQRCwWq2wbRuALMv2Sp51Tt237S5atXjU9FMlzyAICIKAzWZDFEVIKXUfLfv6+orv+zw9PWHbti47qup3vZzzne26kq4vaFVMVrKe57FcLgmCgCRJdF8tu1gs9FmCYRjEccxqtaLb7WrZQ9E9Vbge2XpaUgtJTcPNZsNyuWSxWOD7PkEQ6H5bZwrPz88ARFGE7/v0er2jle9TJQ9Rl1VpKs9zfaYQBAG+7/Pw8KCdAAzYPwe7vb3l5ubmr54n7LIrXJ8OSZIQBMGWKByR/an8U3++/wN2T3nxpLkmlwAAAABJRU5ErkJggg==\"/></g></g></mask><mask id=\"mask-8\" x=\"61.57\" y=\"112.37\" width=\"43\" height=\"43\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"43\" transform=\"translate(938 569)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAArCAYAAADhXXHAAAAACXBIWXMAAAsSAAALEgHS3X78AAADnElEQVRYR+2Za2+qShSGH0BAkBgvaYymafVD//8/atLEtBRTsZZLh+v5NBPwsndzjKU76ZsQiM4wj69rFswaDaj5R6T/rcFPUu/wg9lsxnQ6xXVdbNvGsix0XUfXdTRNQ9M0AHX+P6rrWp3ruqaqKsqyJM9zsizj4+OD3W6H7/utfi3YxWLBw8MDi8WC6XSK53k4joNpmhiGcQQMX4eWgPL6EDTLMtI0JY5jttstvu9j2zZPT0+qXwt2Pp+zWq1YrVbMZjNGo5FyuNfrYRjGRe4eOlrXtXJUCEGSJOx2OzabDZ7nASCEUA4r2Lu7O5bLJff39yyXSxaLBZPJRMGapnlxKJyCraqKLMsQQhBFEbvdDtd1AYiiiNfX12PY6XTKzc0Ns9mM+XzOfD5XsJZlXeyqVBMYoKoqiqIgyzLiOKbf71NVFUmS4Pu+AocGrOM4DIdDxuMx4/GYyWTCaDTCtm10/bpJw7Zt+v0+pmkCkCQJw+GQwWCAZVmqnYK1LAvXdXFdF8/z1N9/bVApwzBwHIcsy9TEbv4AaORZwzAwTZN+v99KWd8pwzCwLEsdMgtJKRpd1+n1eupoNvpOGYbRYmgapq40TUPXdQzDUJOpC8kHUDOvq+/khZzpzaMLSdMOQeHg3aBrUKlzKbLl7GGHrvVHZ2WDrkHPjX8UBl3rT0/I702kF+oX9lr6hb2WfmGvpV/Ya6kF21wud6XDNVpTR87KVedP1Nkw6BL43NgKtrmW7xJU6hTHUcx2DXzI0OQ4craqqs5AAVVS+itsWZaqUFZV1cmbXVty7KIojoxTsGVZqmpelmUURXHyZteUNCzPc4qiUMBSLdgsy/j8/EQIgRCCsixP3vRaKopCjS2EOA8rhCCOY6IoYr/fE0URcRx/i8N1XZPnOUmSEEWRGjtNU/I8V+1UrStNU97f3wnDkO12i+M4AOR5jmVZ9Hq9k2v5r67bDietnDwy/GTJMwxDwjBkv98TxzFCCNVHwb69vREEAc/PzziOo8qOnue1islN4K+CNiWhmxNaFpMlrO/7bDYbwjAkTVPVV8Gu12u1l6BpGkmSsN1uGQwGCvaUu18FbjrbTEtyIskw3O/3bDYb1us1QRAQhqHq1yrTv7y8ABDHMUEQMBwOcRznKAwurS00YWWaKopC7SmEYUgQBDw+PiomAA2O98Fub2+ZTCY4joNt20ebH5eASh0CN8MhTVPCMGyBwhnYn6p/6uX7P4W9eoGB8TNYAAAAAElFTkSuQmCC\"/></g></g></mask><mask id=\"mask-9\" x=\"111.57\" y=\"112.37\" width=\"43\" height=\"43\" maskUnits=\"userSpaceOnUse\"><g class=\"cls-16\"><g transform=\"translate(-876.43 -456.63)\"><image width=\"43\" height=\"43\" transform=\"translate(988 569)\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAArCAYAAADhXXHAAAAACXBIWXMAAAsSAAALEgHS3X78AAADoUlEQVRYR+2ZW2+qTBiFH0COpY2HNEYvWr3o//9FbdKkB6pRiHKQ83exMxNE7W6+1tKddCUTiDLwuJx5YRYKUPOPSP3bAT9JvfYH4/GY0WiE4ziYpolhGKiqiqqqKIqCoigAcvt/VNe13NZ1TVVVlGVJnudkWcZ2uyUIAjzP2+u3BzudTrm7u2M6nTIajXBdF9u20XUdTdMOgOHj0AJQ7LdBsywjSRKiKGK9XuN5HqZp8vj4KPvtwU4mE+bzOfP5nPF4TL/flw73ej00TfuUu21H67qWjqZpShzHBEHAcrnEdV0A0jSVDkvYm5sbZrMZt7e3zGYzptMpw+FQwuq6/umhcAy2qiqyLCNNU8IwJAgCHMcBIAxD3t7eDmFHoxHX19eMx2MmkwmTyUTCGobxaVeFmsAAVVVRFAVZlhFFEZZlUVUVcRzjeZ4EhwasbdtcXV0xGAwYDAYMh0P6/T6maaKq5y0apmliWRa6rgMQxzFXV1dcXFxgGIY8TsIahoHjODiOg+u68u8/N6iQpmnYtk2WZXJiN38ANOqspmnouo5lWXsl6zulaRqGYcgmqpCQpFFVlV6vJ1vzoO+Upml7DE3D5J6iKKiqiqZpcjJ1IXEDatZ1+Z3YETO92bqQMK0NCq1ng65BhU6VyD1n2x261rvOigO6Bj11/YNh0LXeu0N+byH9pH5hz6Vf2HPpF/Zc+oU9l/Zgm8vlrtReozV14KxYdf5EnRwGXQKfuraEba7luwQVOsZxMGa7Bm4zNDkOnK2qiqqqOoUty/J9WBGQlWXZKay4flEUBxx7sCLGybKMPM+PnuycEq7meU5RFBJYSMKK2HG327Hb7UjTlLIsj570XCqKgjRNZTsJu9vtiKKI7XbLZrNhu90SRRFFURw98VeqrmvyPCeOY8IwJAxDoigiSZK9f1hmXUmSEAQBq9WKwWCAZVkAZFkm81mRjjTXRx9dt7XngJg8Yp6IyNP3fXzfZ7PZEEURaZrKPhJ2tVrx8vJCv9/Htm3quiaOYy4vL2U+205JPgralIAWoFVVyTBZwHqex3K5xPd9kiSRfSXs8/OzDOXgT+y4Xq9xXVfC9nq9gyDko8BNZ5tlSUykNE2JoojNZsNyueTp6YnFYoHv+7LfXkx/f38P/InGV6uVdLk5DL4itWnCiipUFIV8p+D7PovFgoeHB15fX2U/hSPvwcQLENu2ZfT4VaBCbeDmcEiSBN/390DhBOxP1T/18P0fQcp4ILYL4HQAAAAASUVORK5CYII=\"/></g></g></mask></defs><title>genepattern-logo</title><g class=\"cls-1\"><g id=\"Layer_1\" data-name=\"Layer 1\"><rect class=\"cls-2\" x=\"1.22\" y=\"1.22\" width=\"164.1\" height=\"164.1\"/><path class=\"cls-3\" d=\"M928.78,503.56a5,5,0,0,1-5,5H895.44a5,5,0,0,1-5-5V475.21a5,5,0,0,1,5-5h28.34a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/><g class=\"cls-4\"><g class=\"cls-5\"><path class=\"cls-6\" d=\"M928.78,503.56a5,5,0,0,1-5,5H895.44a5,5,0,0,1-5-5V475.21a5,5,0,0,1,5-5h28.34a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/></g></g><path class=\"cls-7\" d=\"M978.86,503.56a5,5,0,0,1-5,5H945.53a5,5,0,0,1-5-5V475.21a5,5,0,0,1,5-5h28.34a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/><g class=\"cls-8\"><g class=\"cls-5\"><path d=\"M978.86,503.56a5,5,0,0,1-5,5H945.53a5,5,0,0,1-5-5V475.21a5,5,0,0,1,5-5h28.34a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/></g></g><path class=\"cls-7\" d=\"M1029,503.56a5,5,0,0,1-5,5H995.61a5,5,0,0,1-5-5V475.21a5,5,0,0,1,5-5H1024a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/><g class=\"cls-9\"><g class=\"cls-5\"><path d=\"M1029,503.56a5,5,0,0,1-5,5H995.61a5,5,0,0,1-5-5V475.21a5,5,0,0,1,5-5H1024a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/></g></g><path class=\"cls-3\" d=\"M19,64.35H47.35a5,5,0,0,1,5,5V97.69a5,5,0,0,1-5,5H19a5,5,0,0,1-5-5V69.34A5,5,0,0,1,19,64.35Z\"/><g class=\"cls-10\"><g class=\"cls-5\"><path d=\"M19,64.35H47.35a5,5,0,0,1,5,5V97.69a5,5,0,0,1-5,5H19a5,5,0,0,1-5-5V69.34A5,5,0,0,1,19,64.35Z\"/></g></g><rect class=\"cls-3\" x=\"64.1\" y=\"64.35\" width=\"38.33\" height=\"38.33\" rx=\"5\"/><g class=\"cls-11\"><g class=\"cls-5\"><rect x=\"64.1\" y=\"64.35\" width=\"38.33\" height=\"38.33\" rx=\"5\"/></g></g><path class=\"cls-7\" d=\"M119.18,64.35h28.34a5,5,0,0,1,5,5V97.69a5,5,0,0,1-5,5H119.18a5,5,0,0,1-5-5V69.34A5,5,0,0,1,119.18,64.35Z\"/><g class=\"cls-12\"><g class=\"cls-5\"><path d=\"M119.18,64.35h28.34a5,5,0,0,1,5,5V97.69a5,5,0,0,1-5,5H119.18a5,5,0,0,1-5-5V69.34A5,5,0,0,1,119.18,64.35Z\"/></g></g><path class=\"cls-3\" d=\"M19,114.6H47.35a5,5,0,0,1,5,5v28.35a5,5,0,0,1-5,5H19a5,5,0,0,1-5-5V119.59a5,5,0,0,1,5-5Z\"/><g class=\"cls-13\"><g class=\"cls-5\"><path d=\"M19,114.6H47.35a5,5,0,0,1,5,5v28.35a5,5,0,0,1-5,5H19a5,5,0,0,1-5-5V119.59a5,5,0,0,1,5-5Z\"/></g></g><path class=\"cls-7\" d=\"M69.09,114.6H97.44a5,5,0,0,1,5,5v28.35a5,5,0,0,1-5,5H69.09a5,5,0,0,1-5-5V119.59A5,5,0,0,1,69.09,114.6Z\"/><g class=\"cls-14\"><g class=\"cls-5\"><path d=\"M69.09,114.6H97.44a5,5,0,0,1,5,5v28.35a5,5,0,0,1-5,5H69.09a5,5,0,0,1-5-5V119.59A5,5,0,0,1,69.09,114.6Z\"/></g></g><path class=\"cls-3\" d=\"M1029,604.57a5,5,0,0,1-5,5H995.61a5,5,0,0,1-5-5V576.22a5,5,0,0,1,5-5H1024a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/><g class=\"cls-15\"><g class=\"cls-5\"><path d=\"M1029,604.57a5,5,0,0,1-5,5H995.61a5,5,0,0,1-5-5V576.22a5,5,0,0,1,5-5H1024a5,5,0,0,1,5,5Z\" transform=\"translate(-876.43 -456.63)\"/></g></g></g></g></svg>");

/***/ }),

/***/ "./style/basewidget.css":
/*!******************************!*\
  !*** ./style/basewidget.css ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_basewidget_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./basewidget.css */ "./node_modules/css-loader/dist/cjs.js!./style/basewidget.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_basewidget_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_basewidget_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),

/***/ "./style/uibuilder.css":
/*!*****************************!*\
  !*** ./style/uibuilder.css ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_uibuilder_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./uibuilder.css */ "./node_modules/css-loader/dist/cjs.js!./style/uibuilder.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_uibuilder_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_uibuilder_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),

/***/ "./style/uioutput.css":
/*!****************************!*\
  !*** ./style/uioutput.css ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_uioutput_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./uioutput.css */ "./node_modules/css-loader/dist/cjs.js!./style/uioutput.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_uioutput_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_uioutput_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse("{\"name\":\"@g2nb/nbtools\",\"version\":\"22.12.0-beta.1\",\"description\":\"Framework for creating user-friendly Jupyter notebooks, accessible to both programming and non-programming users alike.\",\"keywords\":[\"jupyter\",\"jupyterlab\",\"jupyterlab-extension\",\"widgets\"],\"files\":[\"lib/**/*.{js,css}\",\"style/*.{js,css,png,svg}\",\"schema/**/*.json\",\"dist/*.{js,css}\",\"style/index.js\"],\"homepage\":\"https://github.com/g2nb/nbtools\",\"bugs\":{\"url\":\"https://github.com/g2nb/nbtools/issues\"},\"license\":\"BSD-3-Clause\",\"author\":{\"name\":\"Thorin Tabor\",\"email\":\"tmtabor@cloud.ucsd.edu\"},\"main\":\"lib/index.js\",\"types\":\"./lib/index.d.ts\",\"style\":\"style/index.css\",\"repository\":{\"type\":\"git\",\"url\":\"https://github.com/g2nb/nbtools\"},\"scripts\":{\"build\":\"jlpm run build:lib && jlpm run build:labextension:dev\",\"build:all\":\"jlpm run build:lib && jlpm run build:labextension && jlpm run build:nbextension\",\"build:labextension\":\"jupyter labextension build .\",\"build:labextension:dev\":\"jupyter labextension build --development True .\",\"build:lib\":\"tsc\",\"build:nbextension\":\"webpack --mode production\",\"clean\":\"jlpm run clean:lib\",\"clean:all\":\"jlpm run clean:lib && jlpm run clean:labextension && jlpm run clean:nbextension\",\"clean:labextension\":\"rimraf nbtools/labextension\",\"clean:lib\":\"rimraf lib tsconfig.tsbuildinfo\",\"clean:nbextension\":\"rimraf nbtools/nbextension/static/index.js\",\"eslint\":\"eslint . --ext .ts,.tsx --fix\",\"eslint:check\":\"eslint . --ext .ts,.tsx\",\"install:extension\":\"jlpm run build\",\"prepack\":\"jlpm run build:lib\",\"prepare\":\"jlpm run clean && jlpm run build:all\",\"test\":\"jlpm run test:firefox\",\"test:chrome\":\"karma start --browsers=Chrome tests/karma.conf.js\",\"test:debug\":\"karma start --browsers=Chrome --singleRun=false --debug=true tests/karma.conf.js\",\"test:firefox\":\"karma start --browsers=Firefox tests/karma.conf.js\",\"test:ie\":\"karma start --browsers=IE tests/karma.conf.js\",\"watch\":\"run-p watch:src watch:labextension\",\"watch:labextension\":\"jupyter labextension watch .\",\"watch:lib\":\"tsc -w\",\"watch:nbextension\":\"webpack --watch\",\"watch:src\":\"tsc -w\"},\"dependencies\":{\"@jupyter-widgets/base\":\"^4.0.0\",\"@jupyterlab/application\":\"^3.0.4\",\"@jupyterlab/mainmenu\":\"^3.0.3\",\"@jupyterlab/notebook\":\"^3.0.4\"},\"devDependencies\":{\"@jupyterlab/apputils\":\"^3.0.3\",\"@jupyterlab/builder\":\"^3.0.0\",\"@jupyterlab/ui-components\":\"^3.0.3\",\"@lumino/application\":\"^1.13.1\",\"@lumino/widgets\":\"^1.16.1\",\"@types/backbone\":\"^1.4.4\",\"@types/node\":\"^14.14.27\",\"@typescript-eslint/eslint-plugin\":\"^4.8.1\",\"@typescript-eslint/parser\":\"^4.8.1\",\"backbone\":\"^1.2.3\",\"css-loader\":\"^5.2.7\",\"eslint\":\"^7.14.0\",\"eslint-config-prettier\":\"^6.15.0\",\"eslint-plugin-prettier\":\"^3.1.4\",\"expect.js\":\"^0.3.1\",\"file-loader\":\"^6.2.0\",\"fs-extra\":\"^9.1.0\",\"karma\":\"^6.1.1\",\"karma-typescript\":\"^5.3.0\",\"mkdirp\":\"^1.0.4\",\"mocha\":\"^8.3.0\",\"npm-run-all\":\"^4.1.5\",\"prettier\":\"^2.1.1\",\"rimraf\":\"^3.0.2\",\"source-map-loader\":\"^2.0.1\",\"style-loader\":\"^2.0.0\",\"ts-loader\":\"^8.0.17\",\"typescript\":\"~4.1.3\",\"webpack\":\"^5.21.2\",\"webpack-cli\":\"^4.5.0\"},\"jupyterlab\":{\"extension\":\"lib/plugin\",\"schemaDir\":\"schema\",\"sharedPackages\":{\"@jupyter-widgets/base\":{\"bundled\":false,\"singleton\":true}},\"discovery\":{\"kernel\":[{\"kernel_spec\":{\"language\":\"^python\"},\"base\":{\"name\":\"nbtools\"},\"managers\":[\"pip\",\"conda\"]}]},\"outputDir\":\"nbtools/labextension\"},\"styleModule\":\"style/index.js\"}");

/***/ })

}]);
//# sourceMappingURL=lib_registry_js-lib_uibuilder_js-lib_uioutput_js.3459ae1bcd279270eeed.js.map