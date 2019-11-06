var app = new Vue({
  el: '#player',
  data: {
    selected: '',
    height: '',
  },
  beforeMount: function() {
    var sources = this.$el.getElementsByTagName('button')
    this.selected = sources[0].attributes['data-source'].value
    this.height = window.innerHeight * 0.75
  },
  methods: {
    render: function (event) {
      this.selected = event.target.attributes['data-source'].value
      var frame = this.$el.firstElementChild.firstElementChild
      frame.contentWindow.location.replace(this.selected)
    }
  },
  delimiters: ['[[',']]']
})
