<template>
  <div>
    <el-menu
      router
      :default-active="this.$router.path"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="/dashboard">Dashboard</el-menu-item>
      <el-menu-item index="/testbedsInfo">Testbeds Information</el-menu-item>
      <el-menu-item index="/cliPanel">CLI Panel</el-menu-item>
      <el-submenu index="/console" style="float: right">
        <template slot="title">Console</template>
        <el-menu-item index="/systemFile">System File</el-menu-item>
        <el-menu-item index="/checkLog">Check Log</el-menu-item>
        <el-menu-item @click.native="logout"
          >Log out [ {{ $store.state.userName }} ]</el-menu-item
        >
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "NavMenu",
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    logout: function () {
      var _this = this;
      this.$confirm("Are you sure to exit?", "Tips", {
        type: "warning",
      })
        .then(() => {
          localStorage.clear();
          this.$store.dispatch("Logout");
          _this.$router.push("/login");
        })
        .catch(() => {});
    },
  },
};
</script>