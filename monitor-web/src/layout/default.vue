<template>
  <div>
    <el-header>
      <nav-menu></nav-menu>
    </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
  </div>
</template>

<script>
import NavMenu from "@/components/NavMenu";
export default {
  name: "Layout",
  components: {
    NavMenu,
  },
};
</script>
<style scoped>
body {
  margin: 0px;
}
.el-header {
  padding: 0;
}
</style>
