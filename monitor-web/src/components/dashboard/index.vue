<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="Topology" name="first">
        <topology></topology>
      </el-tab-pane>
      <el-tab-pane label="Himalaya" name="second">
        <himalaya></himalaya>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import Topology from "@/components/dashboard/components/Topology";
import Himalaya from "@/components/dashboard/components/Himalaya";
export default {
  name: "Dashboard",
  components: { Topology, Himalaya },
  data() {
    return {
      activeName: "first",
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
};
</script>