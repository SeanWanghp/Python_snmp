import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import VueRouter from 'vue-router'
import router from './router';
import locale from '../node_modules/element-ui/lib/locale/lang/en'
import store from './store'

Vue.use(ElementUI, { locale })
Vue.config.productionTip = false
Vue.use(VueRouter)


const a = new Vue({
  render: h => h(App),
  store,
  router: router
}).$mount('#app')

