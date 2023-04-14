// Actions:用于响应组件中的动作
//调用mutations
export const setUser = ({ commit }, user) => {
    commit("userStatus", user);
}

export const Logout = ({ commit }) => {
    console.log(1231)
    commit("Logout");
}