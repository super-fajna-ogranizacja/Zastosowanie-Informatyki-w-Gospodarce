export default class SearchBox {
  constructor (searchBoxElement, callback, delay = 300) {
    this.searchBox = searchBoxElement
    this.delay = delay
    this.callback = callback

    // Bind the event listener
    this.searchBox.addEventListener('input', this.debounce(this.handleSearchInput.bind(this), this.delay))
  }

  debounce (func, timeout = 300) {
    let timer
    return (...args) => {
      clearTimeout(timer)
      timer = setTimeout(() => {
        func.apply(this, args)
      }, timeout)
    }
  }

  handleSearchInput () {
    if (typeof this.callback === 'function') {
      this.callback(this.searchBox.value)
    } else {
      throw new Error('No callback function provided')
    }
  }
}
