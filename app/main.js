var Vue = require('vue')
var VueResource = require('vue-resource')
var VueCodeMirror = require('vue-codemirror')
var VueRouter = require('vue-router')

Vue.use(VueResource)
Vue.use(VueCodeMirror)
Vue.use(VueRouter)


var app = new Vue({
  el: "#wrapper",
  components: {
      'crawler': require('crawler.vue'),
      'spliter': require('spliter.vue'),
      'score': require('score.vue'),
      'train': require('train.vue'),
      'ntusd': require('ntusd.vue'),
      'check': require('check.vue')
  },
  data () {
    return {
      repo : "test",
    }
  }
})


Vue.http.options.emulateJSON = true
