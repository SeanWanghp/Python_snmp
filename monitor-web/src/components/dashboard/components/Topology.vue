<template>
  <div>
    <el-button
      plain
      type="primary"
      style="float: right"
      @click="dialogVisible = true"
      :disabled="$store.state.role == 'Visitor'"
      >Retrieve Topo</el-button
    >
    <div style="height: calc(100vh - 50px)">
      <RelationGraph
        ref="seeksRelationGraph"
        :options="graphOptions"
        :on-node-click="onNodeClick"
        :on-line-click="onLineClick"
        v-loading="loading"
        element-loading-text="Loading..."
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)"
      />
    </div>

    <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
      <span style="word-break: keep-all; white-space: pre-wrap"
        >Are you sure to do this operation? This operation will SSH to all the
        systems to get the latest Topo. Please make sure all of them can be
        connected, which can be known in 'Testbeds Information' page. we suggest
        you download current Topo before you do this operation!</span
      >
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="getTopo(1)">Confirm</el-button>
      </span>
    </el-dialog>
    <button @click="sss">123</button>
  </div>
</template>

 <script>
// relation-graph也支持在main.js文件中使用Vue.use(RelationGraph);这样，你就不需要下面这一行代码来引入了。
import RelationGraph from "relation-graph";
import $ from "jquery";
export default {
  name: "Topology",
  components: { RelationGraph },
  computed: {
    loading() {
      return this.data == "" ? true : false;
    },
  },
  data() {
    return {
      dialogVisible: false,
      graphOptions: {
        defaultNodeBorderWidth: 0,
        allowSwitchLineShape: true,
        allowSwitchJunctionPoint: true,
        defaultLineShape: 1,
        layouts: [
          {
            label: "自动布局",
            layoutName: "force",
            layoutClassName: "seeks-layout-force",
          },
        ],
        // 这里可以参考"Graph 图谱"中的参数进行设置
      },
      data: "",
    };
  },
  mounted() {
    console.log(this.data);
    this.getTopo();
  },
  methods: {
    showSeeksGraph() {
      // 以上数据中的node和link可以参考"Node节点"和"Link关系"中的参数进行配置
      this.$refs.seeksRelationGraph.setJsonData(this.data, (seeksRGGraph) => {
        // Called when the relation-graph is completed
      });
    },
    onNodeClick(nodeObject, $event) {
      console.log("onNodeClick:", nodeObject);
      console.log(this.data);
    },
    onLineClick(lineObject, $event) {
      console.log("onLineClick:", lineObject);
    },
    //flag为1则会重新ssh连接取得数据，为0则直接从数据库中取上一次的拓扑
    getTopo(flag = 0) {
      this.data = "";
      this.dialogVisible = false;
      $.ajax({
        //url
        url: "/api/get_topo?refresh=" + flag,
        //请求类型：
        type: "GET",
        //响应体结果：
        dataType: "json",
        //成功回调：
        success: (d) => {
          this.data = d[0];
          this.showSeeksGraph();
        },
        //超时时间：
        timeout: 180000,
        //失败回调：
        error: function () {
          console.log("get_topo出错");
        },
      });
    },
    sss() {
      console.log($store.getters);
    },
  },
};
</script>