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

  matches (project) {
    const full_name = project.name.toLowerCase();
    const searched_name = this.name;

    if (full_name.includes(searched_name))
      return true;

    if (full_name.length < searched_name.length)
      return false;

    let full_idx = 0;
    let searched_idx = 0;
    for (const full_letter of full_name) {
      if (searched_name[searched_idx] == full_letter) {
        searched_idx += 1;
        if (searched_idx == searched_name.length) {
          return true;
        }
      }
    }

    return false;
  }
}
