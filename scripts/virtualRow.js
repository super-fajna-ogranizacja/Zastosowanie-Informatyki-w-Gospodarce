export default class VirtualRow {
  container = null;

  element = null;

  constructor(container, data) {
    this.container = container;
    this.element = this.render(data);
  }

  // eslint-disable-next-line no-dupe-class-members
  get element() {
    return this.element;
  }

  // eslint-disable-next-line no-dupe-class-members
  set element(element) {
    this.element = element;
  }

  render = (data) => {
    const rowContainer = document.createElement('p');
    const rowInner = document.createElement('a');
    Object.assign(rowContainer.style, {
      height: `${data.rowHeight}px`,
      overflow: 'hidden',
      marginBottom: 0,
    });
    rowContainer.title = data.title;
    rowInner.href = data.url;
    rowInner.innerText = data.text;
    rowContainer.appendChild(rowInner);
    this.element = rowContainer;
    return this.element;
  };

  mountChild = () => {
    this.container.appendChild(this.element);
  };
}
