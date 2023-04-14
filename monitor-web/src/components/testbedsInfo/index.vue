<template>
  <div>
    <el-tabs
      v-model="activeName"
      @tab-click="handleClick"
      :before-leave="beforeLeave"
    >
      <el-tab-pane label="OLT" name="first">
        <table-tmpl equipType="OLT" :key="OLT_reload"></table-tmpl>
      </el-tab-pane>
      <el-tab-pane label="VM" name="second">
        <table-tmpl equipType="VM" :key="VM_reload"></table-tmpl>
      </el-tab-pane>
      <el-tab-pane label="ONT" name="third">
        <table-tmpl equipType="ONT" :key="ONT_reload"></table-tmpl>
      </el-tab-pane>
      <el-tab-pane name="btn">
        <span slot="label">
          <el-button
            type="primary"
            size="small"
            plain
            :disabled="$store.state.role == 'Visitor'"
            @click="addEquipClick()"
          >
            Add Equip
          </el-button>
        </span>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      title="Add Equip"
      :visible.sync="addBox"
      width="50%"
      :before-close="handleClose"
    >
      <el-form
        ref="addEquipData"
        label-width="100px"
        :model="addEquipData"
        :rules="rules"
      >
        <el-form-item label="Owner:" required prop="owner">
          <el-select
            v-model="addEquipData.owner"
            placeholder="please input/select the owner's name"
            ref="owners"
            filterable
            allow-create
            required
            style="width: 100%"
          >
            <el-option
              v-for="(item, index) in owners"
              :key="index"
              :label="item['owner']"
              :value="item['owner']"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="IP：" required prop="ip">
          <el-input
            placeholder="please input IP"
            maxlength="50"
            v-model="addEquipData.ip"
          ></el-input>
        </el-form-item>
        <el-form-item label="System:" prop="system">
          <el-select
            v-model="addEquipData.system"
            placeholder="[None] if Individual Testbeds"
            ref="systems"
            filterable
            allow-create
            required
            style="width: 100%"
          >
            <el-option label="[None]" value=""></el-option>
            <el-option
              v-for="(item, index) in systems"
              :key="index"
              :label="item['system']"
              :value="item['System']"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Rack:" prop="rack">
          <el-input
            placeholder="optional"
            maxlength="50"
            v-model="addEquipData.rack"
          ></el-input>
        </el-form-item>
        <el-form-item label="Type：" required prop="type">
          <el-select
            v-model="addEquipData.type"
            filterable
            style="width: 100%"
            placeholder="please select"
          >
            <el-option
              v-for="(value, key) of { OLT: 'OLT', ONT: 'ONT', VM: 'VM' }"
              :value="key"
              :label="value"
              :key="key"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="
            this.addEquipData.type == 'ONT' || this.addEquipData.type == 'VM'
          "
          label="Username"
          prop="username"
        >
          <el-input
            placeholder="ssh login username"
            maxlength="50"
            v-model="addEquipData.username"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="
            this.addEquipData.type == 'ONT' || this.addEquipData.type == 'VM'
          "
          label="Password"
          prop="password"
        >
          <el-input
            placeholder="ssh login password"
            maxlength="50"
            v-model="addEquipData.password"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="this.addEquipData.type == 'ONT'"
          label="Port"
          prop="port"
        >
          <el-input
            placeholder="ssh port"
            maxlength="50"
            v-model="addEquipData.port"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" plain @click="addEquip">Confirm</el-button>
        <el-button type="danger" plain @click="closeBox">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import $ from "jquery";
import tableTmpl from "@/components/testbedsInfo/components/tableTmpl";
export default {
  name: "testbeds_information",
  components: { tableTmpl },
  data() {
    return {
      activeName: "first",
      //定义数据
      addBox: false,
      owners: "",
      systems: "",
      OLT_reload: "",
      ONT_reload: "",
      VM_reload: "",
      addEquipData: {
        id: "",
        owner: "",
        system: "",
        ip: "",
        type: "",
        rack: "",
        username: "",
        password: "",
        port: "",
      },
      rules: {
        owner: [
          { required: true, message: "please input owner", trigger: "blur" },
        ],
        ip: [{ required: true, message: "please input IP", trigger: "blur" }],
        type: [
          { required: true, message: "please select type", trigger: "blur" },
        ],
      },
    };
  },
  mounted() {
    this.getOwnerData();
    this.getSystemData();
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    beforeLeave(visitName, currentName) {
      if (visitName == "btn") {
        return false;
      }
    },

    // 添加设备数据             2-完成
    addEquipClick: function () {
      this.addEquipData = {
        id: "",
        owner: "",
        system: "",
        ip: "",
        type: "",
        rack: "",
        username: "",
        password: "",
        port: "",
      };
      this.addSystem = "";
      this.addOwner = "";
      this.addBox = true;
    },

    addEquip: function () {
      console.log("@@@", this.$refs);
      this.$refs.addEquipData.validate((valid) => {
        console.log(valid);
        if (!valid) {
          this.$message({
            message: "Required items not completed！！！",
            type: "warning",
          });
        } else {
          if (this.$refs.owners.createdLabel) {
            this.addEquipData["owner"] = this.$refs.owners.createdLabel;
          }
          if (this.$refs.systems.createdLabel) {
            this.addEquipData["system"] = this.$refs.systems.createdLabel;
          }
          $.ajax({
            //url
            url: "/api/add_equip",
            //请求类型：
            type: "POST",
            //响应体结果：
            dataType: "json",
            data: this.addEquipData,
            async: false,
            //成功回调：
            success: (data) => {
              this.$message({
                showClose: true,
                message: "Success!",
                type: "success",
              });
              // console.log(this.addEquipData.type);
              if (this.addEquipData.type == "OLT") {
                this.OLT_reload = new Date().getTime();
              } else if (this.addEquipData.type == "VM") {
                this.VM_reload = new Date().getTime();
              } else if (this.addEquipData.type == "ONT") {
                this.ONT_reload = new Date().getTime();
              }
            },
            //超时时间：
            timeout: 2000,
            //失败回调：
            error: function () {},
          });
          this.addBox = false;
          this.addEquipData = {
            id: "",
            owner: "",
            system: "",
            ip: "",
            type: "",
            rack: "",
            username: "",
            password: "",
            port: "",
          };
        }
      });
    },

    getOwnerData: function () {
      var result;
      $.ajax({
        //url
        url: "/api/check_owners",
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
          console.log("check_onwers出错");
        },
      });
      this.owners = result;
    },

    getSystemData: function () {
      var result;
      $.ajax({
        //url
        url: "/api/check_systems",
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
          console.log("check_systems出错");
        },
      });
      this.systems = result;
    },
    // 取消弹窗                             0-完成
    closeBox: function () {
      this.addBox = false;
      this.addOwner = "";
      this.addSystem = "";
    },
    handleClose(done) {
      done();
    },
  },
};
</script>