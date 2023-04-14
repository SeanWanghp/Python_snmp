const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  devServer: {
    host: '0.0.0.0',
    port: '8060',
    proxy: {
      '/api': {
        target: "http://localhost:5000", //请求后台接口
        changeOrigin: true, // 允许跨域
        pathRewrite: {
          '^/api': '' // 重写请求
        }
      }
    },
    // 防止路由history模式第一次打开页面时出现404错误
    historyApiFallback: {
      index: '/index.html'
    }
  }
})
