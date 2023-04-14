// Mutations：用于操作数据（state）
//更改用户状态信息
export const userStatus = (state, user) => {
    //判断用户是否存在
    if (user != null) {
        state.userName = JSON.parse(user).user.User;
        state.role = JSON.parse(user).user.Role;
    }
}

export const Logout = (state) => {
    state.userName = null;
    state.role = null;
}
