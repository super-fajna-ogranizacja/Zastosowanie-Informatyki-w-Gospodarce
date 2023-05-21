class VirtualScroll {
    rows = [];
    container = null;
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

    getStartNode = (scrollTop) => {
        const startNode = Math.floor(scrollTop / this.getOption('rowHeight')) - this.getOption('rowPadding');
        return Math.max(0, startNode);
    }

    getVisibleNodeCount = (startNode, rowsLength) => {
        const visibleNodesCount = Math.ceil(this.getOption("visibleHeight") / this.getOption('rowHeight')) + 2 * this.getOption('rowPadding');
        return Math.min(rowsLength - startNode, visibleNodesCount);
    }

    render(isFirst = false) {
        const {container: {firstElementChild, scrollTop}, rows} = this;

        if (!firstElementChild) {
            return;
        }

        const startNode = this.getStartNode(scrollTop);
        const visibleNodesCount = this.getVisibleNodeCount(startNode, rows.length);
        const offsetY = startNode * this.getOption('rowHeight');

        if (!isFirst) {
            firstElementChild.childNodes.forEach((node, index) => {
                if (index < startNode || index >= startNode + visibleNodesCount ) {
                    node.remove();
                }
            });
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
        const data = {
            rowHeight: this.getOption('rowHeight'),
            text: this.rows[index].name,
            title: this.rows[index].name,
        }
        let row = this.cachedRows.get(index);
        if (!row) {
            row = new VirtualRow(this.container.firstElementChild, data);
            this.cachedRows.set(index, row);
        }
        return row;
    }

    mount = () => {
        const {container, rows} = this;
        this.setOption('height', rows.length * this.getOption('rowHeight'))
        this.setOption('visibleHeight', container.clientHeight)
        container.style.visibility = "visible";

        if (!container.firstElementChild) {
            container.appendChild(document.createElement('div'));
        }
        Object.assign(container.firstElementChild.style, {
            height: `${this.getOption('height')}px`,
            overflow: 'hidden',
        })

        this.render(true);
    }

    unmount() {
        const {container} = this;
        container.firstElementChild.remove();
        container.style.visibility = "hidden";
        this.cachedRows.clear();
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
        Object.assign(rowContainer.style, {
            height: `${data.rowHeight}px`,
            overflow: 'hidden',
            marginBottom: 0
        })
        rowContainer.innerText = data.text;
        rowContainer.title = data.title;
        this.element = rowContainer;
        return this.element;
    }

    mountChild = () => {
        this.container.appendChild(this.element);
    }
}

const container = document.getElementById('virtualScroll');
const searchBox = document.getElementById('searchBox');

window.addEventListener("load", () => {
    const rows = Array.from({length: 100}, (_, i) =>
        ({id: i, name: `Item ${i}`})
    );
    const virtualScroll = new VirtualScroll(container, rows, {});

    searchBox.addEventListener('focus', () => {
        virtualScroll.mount();
    });

    searchBox.addEventListener('blur', () => {
        // virtualScroll.unmount();
    });

    container.addEventListener('scroll', () => {
        virtualScroll.render();
    });

    console.log("page is fully loaded");
});