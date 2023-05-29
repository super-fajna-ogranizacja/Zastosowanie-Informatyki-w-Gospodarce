export default class SearchPrompt {
  title = null

  urls = null

  type = null

  platform = null

  desc = null

  comment = null

  constructor (text) {
    this.title = text.toLowerCase()
  }

  matches (project) {
    return project.name.toLowerCase().includes(this.title)
  }
}
