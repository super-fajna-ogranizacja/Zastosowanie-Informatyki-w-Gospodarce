import VirtualRow from './virtualRow.js';

export default class VirtualScroll {
  rows = [];

  container = null;

  innerContainer = null;

  options = {};

  defaultOptions = {
    rowHeight: 24,
    rowMargin: 6,
    rowPadding: 4,
    visibleHeight: 300,
    height: 24 * 100,
  };

  cachedRows = new Map();

  constructor(container, rows, options = {}) {
    this.container = container;
    this.rows = rows;
    this.options = new Proxy(options, {
      get: (target, name) => (name in target ? target[name] : this.getDefaultOption(name)),
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
    const startNode = Math.floor(scrollTop / (this.getOption('rowHeight') + 2 * this.getOption('rowMargin'))) - this.getOption('rowPadding');
    return Math.max(0, startNode);
  };

  getVisibleNodeCount = (startNode, rowsLength) => {
    const visibleNodesCount = Math.ceil(this.getOption('visibleHeight') / (this.getOption('rowHeight') + 2 * this.getOption('rowMargin'))) + 2 * this.getOption('rowPadding');
    return Math.min(rowsLength - startNode, visibleNodesCount);
  };

  render(isFirst = false) {
    const { container: { scrollTop }, rows } = this;

    if (!this.innerContainer) {
      return;
    }

    const startNode = this.getStartNode(scrollTop);
    const visibleNodesCount = this.getVisibleNodeCount(startNode, rows.length);
    const offsetY = startNode * (this.getOption('rowHeight') + 2 * this.getOption('rowMargin'));

    if (!isFirst) {
      this.unmountItems();
    } else {
      Array.from({ length: visibleNodesCount }, (_, i) => this.renderItem(i));
    }

    for (let i = startNode; i < visibleNodesCount + startNode; i += 1) {
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
      url: this.rows[index].url,
    };
    let row = this.cachedRows.get(index);
    if (!row) {
      row = new VirtualRow(this.innerContainer, data);
      this.cachedRows.set(index, row);
    }
    return row;
  };

  unmountItems = () => {
    if (this.innerContainer) {
      Array.from(this.innerContainer.childNodes).forEach((node) => node.remove());
    }
  };

  renderMessage = (text) => {
    const { container } = this;
    let messageContainer = container.querySelector('.message-container');
    if (messageContainer) {
      container.querySelector('.message-container').innerText = text;
      return;
    }

    messageContainer = document.createElement('div');
    messageContainer.innerText = text;
    messageContainer.classList.add('message-container');

    if (this.innerContainer) {
      container.replaceChild(messageContainer, this.innerContainer);
    } else {
      container.appendChild(messageContainer);
    }
  };

  unmountMessage = () => {
    const messageContainer = document.querySelector('.message-container');
    if (messageContainer) {
      if (this.innerContainer) {
        this.container.replaceChild(this.innerContainer, messageContainer);
      } else {
        this.container.appendChild(document.createElement('div'));
        this.innerContainer = this.container.firstElementChild;
      }
      this.innerContainer.classList.remove('message-container');
      Object.assign(this.innerContainer.style, {
        height: `${this.getOption('height')}px`,
        overflow: 'hidden',
      });
    }
  };

  mount = () => {
    const { container, rows: { length } } = this;

    if (!container) {
      return;
    }

    this.cachedRows.clear();
    this.setOption('height', length * (this.getOption('rowHeight') + 2 * this.getOption('rowMargin')));
    this.setOption('visibleHeight', container.clientHeight);
    container.style.visibility = 'visible';

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
      position: 'relative',
    });

    this.render(true);
  };

  unmount() {
    if (this.innerContainer) {
      this.innerContainer.remove();
      this.innerContainer = null;
    }
    this.container.style.visibility = 'hidden';
  }
}
