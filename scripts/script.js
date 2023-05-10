class VirtualScroll {
    rows = [];
    container = null;
    options = {};
    defaultOptions = {
        height: 300,
        rowHeight: 24,
        rowMaxNumber: 10000,
        rowPadding: 3
    };

    constructor(container, rows, options = {}) {
        this.container = container;
        this.rows = rows;
        this.options = new Proxy(options, {
            get: (target, name) =>
                name in target ? target[name] : this.getDefaultOption(name)
        });
    }

    getDefaultOption(name)  {
        if (name in this.defaultOptions) {
            return this.defaultOptions[name];
        }

        throw new Error(`Invalid option: ${name}`);
    }

    setOption(name, value) {
        if (name in this.options) {
            this.options[name] = value;
        } else {
            throw new Error(`Invalid option: ${name}`);
        }
    }

    getOption(name) {
        if (name in this.options) {
            return this.options[name];
        } else {
            throw new Error(`Invalid option: ${name}`);
        }
    }

    render() {
        const { container, rows, options } = this;
        const visible = document.createElement('div');
        container.style.visibility = "visible";

        // rows.map((row) => {
        //     const rowContainer = document.createElement('div');
        //     rowContainer.style.height = `${options.rowHeight}px`;
        //     rowContainer.style.border = "1px solid black";
        //     rowContainer.innerText = row;
        //     visible.appendChild(rowContainer);
        // });


        const nodePadding = options.rowPadding;
        const totalContentHeight = rows.length * options.rowHeight;
        let startNode = Math.floor(container.scrollTop / options.rowHeight) - nodePadding;
        startNode = Math.max(0, startNode);

        let visibleNodesCount = Math.ceil(options.height / options.rowHeight) + nodePadding;
        visibleNodesCount = Math.min(rows.length - startNode, visibleNodesCount);

        const offsetY = startNode * options.rowHeight;
        for (let i = 0; i < visibleNodesCount; i++) {
            const row = rows[startNode + i];
            const rowContainer = this.renderItem(row);
            rowContainer.style.transform = `translateY(${offsetY}px)`;
            visible.appendChild(rowContainer);
        }
        container.appendChild(visible);
        console.log("123");
    }

    renderItem(index) {
        const { rows, options } = this;
        const row = rows[index];
        const rowContainer = document.createElement('p');
        rowContainer.style.height = `${options.rowHeight}px`;
        // rowContainer.style.border = "1px solid black";
        rowContainer.innerText = index;
        rowContainer.style.marginBottom = "0";
        return rowContainer;
    }

    mount() {
        const { container } = this;
        container.style.visibility = "visible";
    }

    unmount() {
        const { container } = this;
        container.style.visibility = "hidden";
        container.children[0].remove();
    }


}


const container  = document.getElementById('virtualScroll');
const searchBox = document.getElementById('searchBox');

window.addEventListener("load", (event) => {
    const rows = Array.from({ length: 100 }, (_, i) => i);
    const virtualScroll = new VirtualScroll(container, rows, {});

    searchBox.addEventListener('focus', (event) => {
        virtualScroll.render();
    });

    searchBox.addEventListener('blur', (event) => {
        virtualScroll.unmount();
    });

    container.addEventListener('scroll', (event) => {
        console.log(event.target.scrollTop);
    });

    console.log("page is fully loaded");
});