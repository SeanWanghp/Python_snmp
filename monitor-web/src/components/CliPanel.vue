<template>
  <div>
    <el-input
      v-model="input"
      placeholder="Input Command Line"
      clearable
      style="width: 20%"
    ></el-input>

    <el-select
      v-model="type"
      placeholder="Please select type"
      style="margin-left: 13px"
    >
      <el-option label="OLT" value="OLT">OLT</el-option>
      <el-option label="ONT" value="ONT">ONT</el-option>
      <el-option label="VM" value="VM">VM</el-option>
    </el-select>

    <el-cascader
      style="margin-left: 13px"
      :options="options"
      :props="props"
      collapse-tags
      clearable
      v-model="casValue"
      @change="change"
      placeholder="Please select IP"
      v-if="type"
    ></el-cascader>

    <el-button
      type="primary"
      style="margin-left: 13px"
      @click="execution('SSH')"
      :disabled="disable"
      plain
      >SSH</el-button
    >
    <el-button
      type="success"
      style="margin-left: 13px"
      @click="execution('Telnet')"
      :disabled="disable"
      plain
      >Telnet</el-button
    >

    <el-card
      style="margin-top: 10px; height: 100%; min-height: 600px"
      v-loading="loading"
      element-loading-text="Loading..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
      <el-button
        type="primary"
        plain
        v-if="feedback"
        size="small"
        style="margin-bottom: 10px"
        @click="saveFeedback"
        >Save</el-button
      >
      <div v-for="(line, index) in feedback" :key="index">
        <mark
          v-if="/\d+\.\d+\.\d+\.\d+:/.test(line)"
          style="white-space: pre-wrap"
          >{{ line }}</mark
        >
        <a v-else style="white-space: pre-wrap">{{ line }}</a>
      </div>
    </el-card>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "CliPanel",
  // according user adjust whether can running command, https://blog.csdn.net/HeBLL/article/details/126410965
  created(){
      if (this.$store.state.role == 'Visitor') {
        this.disable= true
      }
      else {
        this.disable = false
      }    
  },
  watch: {
    type() {
      this.getCasData();
    },
  },
  computed: {
    User() {
      return JSON.parse(localStorage.getItem("token")).user.User;
    },
  },
  data() {
    return {
      activeName: "first",
      input: "",
      props: { multiple: true },
      options: [],
      casValue: [],
      level1: 0, //第一层选项
      level2: 0, //第二层选项
      feedback: "",
      loading: false,
      disable: false,
      type: "",
    };
  },
  methods: {
    getCasData() {
      var result = [];
      $.ajax({
        //url
        url: "/api/cascade_data?type=" + this.type,
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
          console.log("cascade_data出错");
        },
      });
      this.options = result;
      console.log(this.options);
    },

    change(item) {
      // try catch是为了跳出forEach循环，因为forEach不能直接用break跳出
      try {
        item.forEach((i) => {
          if (i[0] != this.level1) {
            this.level1 = i[0];
            throw Error();
          }
        });
      } catch (e) {
        let filterd = item.filter((v) => v[0] == this.level1); // 过滤出与标识符相符的选项
        this.casValue = [];
        this.casValue.push(...filterd);
      }
    },

    execution(flag) {
      if (this.input == "") {
        this.$message.error("Command can't be empty!");
      } else if (this.casValue.length == 0) {
        this.$message.error("IP list can't be empty!");
      } else {
        if (flag == "Telnet") {
          this.$prompt("Please input your Telnet port:")
            .then(({ value }) => {
              this.loading = true;
              this.disable = true;
              var ips = this.casValue;
              ips = JSON.stringify(ips);
              var cli = this.input;
              var res = "";
              $.ajax({
                //url
                url: "/api/execute",
                //请求类型：
                type: "POST",
                //响应体结果：
                dataType: "json",
                data: { ips: ips, cli: cli, type: this.type, port: value },
                //成功回调：
                success: (data) => {
                  res = data[0];
                  var error_ip = data[1];
                  this.feedback = res;
                  if (data[1].length == 0) {
                    this.$message({
                      message: "CLI Execute Successfully!",
                      type: "success",
                    });
                  } else {
                    this.$message({
                      message: error_ip.join("&") + " didn't return properly",
                      type: "warning",
                    });
                  }

                  this.loading = false;
                  this.disable = false;
                },
                //超时时间：
                timeout: 180000,
                //失败回调：
                error: (XMLHttpRequest, textStatus, errorThrown) => {
                  this.$message({
                    message: errorThrown,
                    type: "error",
                  });
                  this.loading = false;
                  this.disable = false;
                },
              });
            })
            .catch((err) => {
              console.log(err);
            });
        } else {
          this.loading = true;
          this.disable = true;
          var ips = this.casValue;
          ips = JSON.stringify(ips);
          var cli = this.input;
          var res = "";
          $.ajax({
            //url
            url: "/api/execute",
            //请求类型：
            type: "POST",
            //响应体结果：
            dataType: "json",
            data: { ips: ips, cli: cli, type: this.type },
            //成功回调：
            success: (data) => {
              res = data[0];
              var error_ip = data[1];
              this.feedback = res;
              if (data[1].length == 0) {
                this.$message({
                  message: "CLI Execute Successfully!",
                  type: "success",
                });
              } else {
                this.$message({
                  message: error_ip.join("&") + " didn't return properly",
                  type: "warning",
                });
              }

              this.loading = false;
              this.disable = false;
            },
            //超时时间：
            timeout: 180000,
            //失败回调：
            error: (XMLHttpRequest, textStatus, errorThrown) => {
              this.$message({
                message: errorThrown,
                type: "error",
              });
              this.loading = false;
              this.disable = false;
            },
          });
        }
      }
    },

    saveFeedback() {
      this.$prompt("Please input your Email Address:")
        .then(({ value }) => {
          $.ajax({
            //url
            url: "/api/sendEmailWithLogs",
            //请求类型：
            type: "GET",
            //响应体结果：
            dataType: "json",
            data: { receiver: value, CLI: this.input },
            //成功回调：
            success: (data) => {
              this.$message({
                message: "Send Email successfully",
                type: "success",
              });
            },
            //超时时间：
            timeout: 180000,
            //失败回调：
            error: () => {
              this.$message({
                message: "fail in send",
                type: "error",
              });
            },
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

