class VirtualScroll {
    rows = [];
    container = null;
    innerContainer = null;
    options = {};
    defaultOptions = {
        rowHeight: 24,
        rowMaxNumber: 100,
        rowPadding: 4,
        visibleHeight: 300,
        height: 24 * 100,
    };
    cachedRows = new Map();

    constructor(container, rows, options = {}) {
        this.container = container;
        this.rows = rows;
        this.options = new Proxy(options, {
            get: (target, name) =>
                name in target ? target[name] : this.getDefaultOption(name)
        });
    }

    getDefaultOption(name) {
        if (name in this.defaultOptions) {
            return this.defaultOptions[name];
        }

        throw new Error(`Invalid option: ${name}`);
    }

    setOption(name, value) {
        this.options[name] = value;
    }

    getOption(name) {
        if (name in this.options || name in this.defaultOptions) {
            return this.options[name] ?? this.defaultOptions[name];
        }

        throw new Error(`Invalid option: ${name}`);
    }

    setRows(rows) {
        this.rows = rows;
        this.mount();
    }

    getStartNode = (scrollTop) => {
        const startNode = Math.floor(scrollTop / this.getOption('rowHeight')) - this.getOption('rowPadding');
        return Math.max(0, startNode);
    }

    getVisibleNodeCount = (startNode, rowsLength) => {
        const visibleNodesCount = Math.ceil(this.getOption("visibleHeight") / this.getOption('rowHeight')) + 2 * this.getOption('rowPadding');
        return Math.min(rowsLength - startNode, visibleNodesCount);
    }

    render(isFirst = false) {
        const {container: {scrollTop}, rows} = this;

        if (!this.innerContainer) {
            return;
        }

        const startNode = this.getStartNode(scrollTop);
        const visibleNodesCount = this.getVisibleNodeCount(startNode, rows.length);
        const offsetY = startNode * this.getOption('rowHeight');

        if (!isFirst) {
            this.unmountItems();
        } else {
            Array.from({length: visibleNodesCount}, (_, i) => this.renderItem(i));
        }

        for (let i = startNode; i < visibleNodesCount + startNode; i++) {
            const row = this.cachedRows.get(i) ?? this.renderItem(i);
            row.mountChild();
            row.element.style.transform = `translateY(${offsetY}px)`;
        }
    }

    renderItem = (index) => {
        this.unmountMessage();
        const data = {
            rowHeight: this.getOption('rowHeight'),
            text: this.rows[index].name,
            title: this.rows[index].name,
        }
        let row = this.cachedRows.get(index);
        if (!row) {
            row = new VirtualRow(this.innerContainer, data);
            this.cachedRows.set(index, row);
        }
        return row;
    }

    unmountItems = () => {
        if (this.innerContainer) {
            Array.from(this.innerContainer.childNodes).forEach(node => node.remove());
        }
    }

    renderMessage = (text) => {
        const {container} = this;
        let messageContainer = container.querySelector('.message-container');
        if (messageContainer) {
            container.querySelector('.message-container').innerText = text;
            return;
        }

        messageContainer = document.createElement('div');
        messageContainer.innerText = text;
        messageContainer.classList.add('message-container');

        if (this.innerContainer){
            container.replaceChild(messageContainer, this.innerContainer);
        } else {
            container.appendChild(messageContainer);
        }
    }

    unmountMessage = () => {
        const messageContainer = document.querySelector('.message-container');
        if (messageContainer) {
            if (this.innerContainer){
                this.container.replaceChild(this.innerContainer, messageContainer);
            } else {
                container.appendChild(document.createElement('div'));
                this.innerContainer = container.firstElementChild;
            }
            this.innerContainer.classList.remove("message-container")
            Object.assign(this.innerContainer.style, {
                height: `${this.getOption('height')}px`,
                overflow: 'hidden',
            })
        }
    }

    mount = () => {
        const {container, rows : {length}} = this;

        if (!container) {
            return;
        }

        this.cachedRows.clear();
        this.setOption('height', length * this.getOption('rowHeight'))
        this.setOption('visibleHeight', container.clientHeight)
        container.style.visibility = "visible";

        if (length > this.getOption('rowMaxNumber')) {
            this.renderMessage(`The maximum number of rows is ${this.getOption('rowMaxNumber')}`);
            return;
        }
        if (length <= 0) {
            this.renderMessage('No elements to display');
            return;
        }

        this.unmountMessage();
        if (!this.innerContainer) {
            container.appendChild(document.createElement('div'));
            this.innerContainer = container.firstElementChild;
        } else {
            this.unmountItems();
        }

        Object.assign(this.innerContainer.style, {
            height: `${this.getOption('height')}px`,
            overflow: 'hidden',
        })

        this.render(true);
    }

    unmount() {
        if (this.innerContainer){
            this.innerContainer.remove();
            this.innerContainer = null;
        }
        this.container.style.visibility = "hidden";
    }
}

class VirtualRow {
    container = null;
    element = null;

    constructor(container, data) {
        this.container = container;
        this.element = this.render(data);
    }

    get element() {
        return this.element;
    }

    set element(element) {
        this.element = element;
    }

    render = (data) => {
        const rowContainer = document.createElement('p');
        const rowInner = document.createElement('a');
        Object.assign(rowContainer.style, {
            height: `${data.rowHeight}px`,
            overflow: 'hidden',
            marginBottom: 0
        })
        rowContainer.title = data.title;
        rowInner.href = data.url;
        rowInner.target = '_blank';
        rowInner.innerText = data.text;
        rowContainer.appendChild(rowInner);
        this.element = rowContainer;
        return this.element;
    }

    mountChild = () => {
        this.container.appendChild(this.element);
    }
}

class SearchPrompt {
    title = null;
    urls = null;
    type = null;
    platform = null;
    desc = null;
    comment = null;

    constructor(text) {
        this.title = text.toLowerCase();
    }

    matches(project) {
        return project.name.toLowerCase().includes(this.title);
    }
}

class SearchBox {
    constructor(searchBoxElement, delay = 300, callback) {
        this.searchBox = searchBoxElement;
        this.delay = delay;
        this.callback = callback;

        // Bind the event listener
        this.searchBox.addEventListener('input', this.debounce(this.handleSearchInput.bind(this), this.delay));
    }

    debounce(func, timeout = 300){
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => { func.apply(this, args); }, timeout);
        };
    }

    handleSearchInput() {
        if (typeof this.callback === 'function') {
            this.callback(this.searchBox.value);
        } else {
            throw new Error('No callback function provided');
        }
    }
}

const container = document.getElementById('virtual-scroll');
const searchBox = document.getElementById('search-box');

window.addEventListener("load", () => {
    const rows = Array.from({length: 100}, (_, i) =>
        ({id: i, name: `Item ${i}`, url: "https://www.google.com"})
    );

    const filterProjects = (promptText, projects) => {
        const search = new SearchPrompt(promptText);

        return projects.filter(p => search.matches(p));
    };

    const callbackFunction = (searchInput) => {
        const projects = filterProjects(searchInput, rows);
        virtualScroll.setRows(projects);
    };

    const virtualScroll = new VirtualScroll(container, rows, {});
    new SearchBox(searchBox, 300, callbackFunction);

    searchBox.addEventListener('focus', () => {
        virtualScroll.mount();
    });

    document.addEventListener('click', (event) => {
        const target = event.target;
        if (!container.contains(target) && target !== searchBox) {
            virtualScroll.unmount();
        }
    });

    container.addEventListener('scroll', () => {
        virtualScroll.render();
    });


    console.info("Page is fully loaded");
});
