<template>
  <div>
    <el-card class="box-card" style="height: 100%; min-height: 100%">
      <div slot="header" class="clearfix">
        <span>monitor.log</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          @click="get_log()"
          >refresh</el-button
        >
      </div>
      <div v-for="line in monitor_log" :key="line">
        <mark v-if="/\d+\.\d+\.\d+\.\d+/.test(line)">{{ line }}</mark>
        <a v-else>{{ line }}</a>
      </div>
      <!-- <a style="white-space: pre-wrap">{{ monitor_log }}</a> -->
    </el-card>
  </div>
</template>
<script>
import $ from "jquery";
export default {
  name: "CheckLog",
  data() {
    return {
      monitor_log: [],
    };
  },
  mounted() {
    this.get_log();
  },
  methods: {
    get_log: function () {
      $.ajax({
        //url
        url: "/api/get_log",
        //请求类型：
        type: "GET",
        //响应体结果：
        dataType: "json",
        //成功回调：
        success: (data) => {
          this.monitor_log = data;
          console.log(data);
        },
        //超时时间：
        timeout: 2000,
        //失败回调：
        error: function () {
          console.log("get_log出错");
        },
      });
    },
  },
};
</script>

<style>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

.box-card {
  width: 100%;
}
</style>
