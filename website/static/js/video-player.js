Vue.component('video-player', {
  props: {
    sources: Array
  },
  data: function() {
    return {
      selected: '',
    }
  },
  beforeMount: function() {
    this.selected = this.sources[0].url
  },
  methods: {
    render: function (event) {
      this.selected = event.target.attributes['data-source'].value
    }
  },
  template:`
    <div>
      <div class="embed-responsive embed-responsive-16by9 border">
        <iframe class="embed-responsive-item"
                v-bind:src="selected"
                allowfullscreen></iframe>
      </div>
      
      <div class="mt-2">
        <template v-for="source in sources">
          <button type="button" class="btn mr-1"
                  v-on:click="render"
                  v-bind:class="[selected == source.url ? 'btn-primary' : 'btn-secondary']"
                  v-bind:data-source="source.url">
            {{ source.title }}
          </button>
        </template>
      </div>
    </div>
  `
})

var videoPlayer = new Vue({ el: '#player' })
