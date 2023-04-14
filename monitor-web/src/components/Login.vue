<template>
  <div class="loginbBody">
    <div class="loginDiv">
      <div class="login-content">
        <h1 class="login-title">Login</h1>
        <el-form
          :model="loginForm"
          label-width="100px"
          :rules="rules"
          ref="loginForm"
          @keyup.enter.native="confirm()"
        >
          <el-form-item label="User :" prop="username">
            <el-input
              style="width: 200px"
              type="text"
              v-model="loginForm.username"
              autocomplete="off"
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item label="Pwd :" prop="password">
            <el-input
              style="width: 200px"
              type="password"
              v-model="loginForm.password"
              show-password
              autocomplete="off"
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="confirm"
              plain
              size="small"
              style="font-size: 15px; width: 90px"
              >Confirm</el-button
            >
            <el-button
              type="danger"
              @click="clear"
              plain
              size="small"
              style="font-size: 15px; width: 90px; margin-left: 20px"
              >Clear</el-button
            >
            <el-link
              :underline="false"
              type="info"
              style="font-size: 13px; margin-left: 20px"
              @click="visit"
              >Visitor</el-link
            >
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
const admin = { User: "admin", Pwd: "Calix123", Role: "Admin" };
const visitor = { User: "visitor", Pwd: "visitor", Role: "Visitor" };

export default {
  name: "login",
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
      rules: {
        username: [
          { required: true, message: "please input username", trigger: "blur" },
        ],
        password: [
          { required: true, message: "please input password", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    confirm() {
      console.log(this.$refs.loginForm);
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          //valid成功为true，失败为false
          if (
            this.loginForm.username == admin["User"] &&
            this.loginForm.password == admin["Pwd"]
          ) {
            var token = JSON.stringify({
              user: admin,
              timestamp: Date.now(), // 当前时间戳
            });
          } else if (
            this.loginForm.username == visitor["User"] &&
            this.loginForm.password == visitor["Pwd"]
          ) {
            var token = JSON.stringify({
              user: visitor,
              timestamp: Date.now(), // 当前时间戳
            });
          } else {
            this.$message({
              message: "Incorrect username or password ",
              type: "warning",
            });
            return false;
          }
          localStorage.setItem("token", token);
          //将用户名放入vuex中
          this.$store.dispatch("setUser", token);

          //路由跳转
          this.$router.replace("/index");
          this.$message({
            message: "Login success!",
            type: "success",
          });
        } else {
          console.log("校验失败");
          return false;
        }
      });
    },
    visit() {
      this.loginForm.username = "visitor";
      this.loginForm.password = "visitor";
      this.confirm();
    },
    clear() {
      this.loginForm.username = "";
      this.loginForm.password = "";
    },
  },
};
</script>

<style scoped >
.loginbBody {
  width: 100%;
  height: 100%;
}
.loginDiv {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -200px;
  margin-left: -250px;
  width: 450px;
  height: 330px;
  background: #fff;
  border-radius: 5%;
}
.login-title {
  margin: 20px 0;
  text-align: center;
}
.login-content {
  width: 400px;
  height: 250px;
  position: absolute;
  top: 25px;
  left: 25px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 10px rgba(0, 0, 0, 0.04);
  border-radius: 4px;
}
</style>
