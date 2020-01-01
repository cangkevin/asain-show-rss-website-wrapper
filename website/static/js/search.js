Vue.component('search', {
  data: function() {
    return {
      selected: false,
      query: '',
      results: []
    }
  },
  created: function() {
    this.debouncedQueryIndex = _.debounce(this.queryIndex, 750)
  }, 
  watch: {
    query: function(newQuery) {
      this.debouncedQueryIndex()
    }
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
  template:`
    <form v-on:submit.prevent>
      <div class="row">
        <div class="input-group col">
          <input v-model.trim="query"
                 v-on:focus="showSuggestions"
                 v-on:blur="hideSuggestions"
                 class="form-control form-control-sm border-right-0 border"
                 type="search" placeholder="Search...">
          <span class="input-group-append">
            <div class="input-group-text bg-white">
              <i class="fa fa-search"></i>
            </div>
          </span>
        </div>
      </div>

      <div id="suggestions" 
           class="position-absolute list-group"
           v-bind:class="{'d-none': !selected }">
        <template v-for="result in results">
          <a :href="'/episodes/' + result.id + '/1'"
              class="list-group-item list-group-item-action suggestion"
              v-bind:key="result.id">
            <div class="media">
              <img :src="result.image" class="mr-3" />
              <div class="media-body align-self-center">
                <h6>{{ result.title }}</h6>
              </div>
            </div>
          </a>
        </template>
      </div>
    </form>
    `
})

var searchApp = new Vue({ el: '#search' })
