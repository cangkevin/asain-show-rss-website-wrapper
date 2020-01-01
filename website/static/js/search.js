var searchApp = new Vue({
  el: '#search',
  data() {
    return {
      selected: false,
      query: '',
      results: []
    }
  },
  watch: {
    query: function(newQuery) {
      this.debouncedQueryIndex()
    }
  },
  created: function() {
    this.debouncedQueryIndex = _.debounce(this.queryIndex, 750)
  }, 
  methods: {
    queryIndex: function() {
      if (this.query) {
        axios.get('/search', {
            params: {
              'q': this.query
            }
          })
          .then(response => (this.results = response.data))
          .catch(error => (this.results = []))
      } else {
        this.results = []
      }
    },
    showSuggestions: function(event) {
      this.selected = true
    },
    hideSuggestions: function(event) {
      targeted = event.relatedTarget
      if (!targeted || !targeted.attributes['class'].value.includes('suggestion')) {
        this.selected = false
      }
    }
  },
  delimiters: ['[[',']]']
})
