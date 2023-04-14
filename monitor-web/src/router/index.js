// 该文件专门用于创建整个应用的路由器
import Router from "vue-router";


const VueRouter = new Router({
    routes: [
        {
            path: "/",
            redirect: "/index"
        },
        {
            name: 'Login',
            path: "/login",
            component: () => import('@/components/Login'),
        },

        {
            path: '/index',
            redirect: 'dashboard',
            component: () => import('@/layout/default'),
            meta: { requireAuth: true },
            children: [
                {
                    name: 'Dashboard',
                    path: "/dashboard",
                    component: () => import('@/components/dashboard/index'),
                },
                {
                    name: 'Testbeds Info',
                    path: "/testbedsInfo",
                    component: () => import('@/components/testbedsInfo/index'),
                },
                {
                    name: 'Check Log',
                    path: "/checkLog",
                    component: () => import('@/components/CheckLog'),
                },
                {
                    name: 'System File',
                    path: "/systemFile",
                    component: () => import('@/components/SystemFile'),
                },
                {
                    name: 'CLI Panel',
                    path: "/cliPanel",
                    component: () => import('@/components/CliPanel'),
                }

            ]
        }
    ],
    mode: "history"
})

// 全局前置路由守卫
VueRouter.beforeEach((to, from, next) => {
    //如果要跳转到登录页面
    if (to.fullPath === "/login" || to.fullPath === "/Login") {
        //如果localStorage 存在 token 则 不允许直接跳转到 登录页面
        if (localStorage.getItem('user')) {
            console.log("不准前往登陆界面")
            next({
                path: from.fullPath
            });
        } else {
            next();
        }
    }
    //如果要跳转到其他页面
    else {
        // 判断token有没有过期
        let data = JSON.parse(localStorage.getItem('token'));
        if (!data) {
            user = null
        }
        else if (Date.now() - data.timestamp < 3600000) { // 1 小时过期
            // 数据未过期，可以使用
            console.log("未过期")
            var user = data.user;
        } else {
            // 数据已过期，需要删除
            window.alert(
                'Session timeout! please login in!'
            )
            localStorage.removeItem('token');
        }
        if (to.matched.some((r) => r.meta.requireAuth)) {
            if (user) {   //判断是否已经登录
                console.log("已经登陆了")
                next();
            } else {
                console.log("没有登陆，重定向到login界面")
                next({
                    path: '/login',
                    query: { redirect: to.fullPath }   //登录成功后重定向到当前页面
                });
            }
        } else {
            next();
        }
    }
});

VueRouter.afterEach((to, from) => {
    console.log(to, from)
    document.title = to.name
})

export default VueRouter;
