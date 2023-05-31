import SearchBox from './searchBox.js';
import SearchPrompt from './searchPrompt.js';
// eslint-disable-next-line import/no-unresolved
import { projects } from './projects.js';
import VirtualScroll from './virtualScroll.js';

const container = document.getElementById('virtual-scroll');
const searchBox = document.getElementById('search-box');

window.addEventListener('load', () => {
  const rows = Object.keys(projects).map((name) => ({ id: name, name, url: `/${name}.html` }));
  const virtualScroll = new VirtualScroll(container, rows, {});

  const filterProjects = (promptText, passedProjects) => {
    const search = new SearchPrompt(promptText);

    return passedProjects.filter((p) => search.matches(p));
  };

  const callbackFunction = (searchInput) => {
    const passedProjects = filterProjects(searchInput, rows);
    virtualScroll.setRows(passedProjects);
  };
  // eslint-disable-next-line no-unused-vars
  const _ = new SearchBox(searchBox, callbackFunction, 300);
  searchBox.addEventListener('focus', () => {
    virtualScroll.mount();
  });

  document.addEventListener('click', (event) => {
    const { target } = event;
    if (!container.contains(target) && target !== searchBox) {
      virtualScroll.unmount();
    }
  });

  container.addEventListener('scroll', () => {
    virtualScroll.render();
  });

  // eslint-disable-next-line no-console
  console.info('Page is fully loaded');
});
