// 该文件用于创建Vuex中最为核心的store，用了Vuex技术
import Vuex from 'vuex'
import Vue from 'vue'
import * as getters from './getters'
import * as mutations from './mutations'
import * as actions from './actions'
Vue.use(Vuex)

// state和getter类似于data和computed
// State：用于存储数据
var state = {}
var user = JSON.parse(localStorage.getItem('token'))
if (user == null) {
    state = {
        userName: null,//当前用户
        role: null,//用户权限信息
    }
}
else {
    state = {
        userName: user['user']['User'],//当前用户
        role: user['user']['Role'],//用户权限信息
    }
}




export default new Vuex.Store({
    actions,
    mutations,
    state,
    getters
})
