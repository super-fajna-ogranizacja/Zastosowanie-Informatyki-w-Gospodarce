export default class SearchPrompt {
  name = null;

  urls = null;

  type = null;

  platform = null;

  desc = null;

  comment = null;

  constructor(text) {
    this.name = text.toLowerCase();
  }

  matches(project) {
    const fullName = project.name.toLowerCase();
    const searchedName = this.name;

    if (fullName.includes(searchedName)) {
      return true;
    }

    if (fullName.length < searchedName.length) {
      return false;
    }

    let searchedIdx = 0;
    for (let fullIdx = 0; fullIdx < fullName.length; fullIdx += 1) {
      if (searchedName[searchedIdx].localeCompare(fullName[fullIdx]) === 0) {
        searchedIdx += 1;
        if (searchedIdx === searchedName.length) {
          return true;
        }
      }
    }

    return false;
  }
}
