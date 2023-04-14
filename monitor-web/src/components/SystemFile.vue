<template>
  <div>
    <div class="tab-container">
      <div class="custom-tree-container">
        <el-input
          placeholder="Filter with keywords"
          v-model="filterText"
          prefix-icon="el-icon-search"
          clearable
        >
        </el-input>
        <!-- show-checkbox -->
        <div class="block" style="margin-top: 10px">
          <el-tree
            :data="data"
            node-key="id"
            :filter-node-method="filterNode"
            ref="tree"
            style="margin-top = 10px"
          >
            <span class="custom-tree-node" slot-scope="{ data }">
              <i
                :class="[
                  data.type == 'folder'
                    ? 'el-icon-folder'
                    : 'el-icon-notebook-2',
                ]"
                style="color: #ffe791; margin-right: 5px"
              ></i>
              <a style="font-size: 15px" v-if="data.type == 'folder'">{{
                data.fileName
              }}</a>
              <a style="font-size: 15px" v-else :href="data.path">{{
                data.fileName
              }}</a>
            </span>
          </el-tree>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
export default {
  name: "SystemFile",
  data() {
    return {
      filterText: "", //搜索过滤
      isFolder: false, //是否是文件夹
      data: [],
    };
  },

  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },

  mounted() {
    this.getData();
  },
  methods: {
    getData: function () {
      var result = "";
      $.ajax({
        //url
        url: "/api/getFileTree",
        //请求类型：
        type: "GET",
        //响应体结果：
        dataType: "json",
        //成功回调：
        success: function (data) {
          result = data;
        },
        //超时时间：
        timeout: 2000,
        async: false,
        //失败回调：
        error: function () {
          console.log("getFileTree出错");
        },
      });
      this.data = result;
    },

    filterNode(value, data) {
      if (!value) return true;
      return data.fileName.indexOf(value) !== -1;
    },
  },
};
</script>