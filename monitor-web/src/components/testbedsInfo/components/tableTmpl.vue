<template>
  <div style="margin-top: 10px">
    <el-select
      v-model="selectedOwner"
      width="50%"
      placeholder="Owner"
      @change="changeSelect"
      @remove-tag="removeTag"
      multiple
      collapse-tags
      filterable
    >
      <el-option
        label="All"
        value="allOwners"
        @click.native="selectAll"
      ></el-option>
      <el-option
        v-for="(item, index) in owners"
        :key="index"
        :label="item['owner']"
        :value="item['owner']"
      />
    </el-select>

    <span style="float: right">
      <el-badge
        :value="disconnectedNum"
        class="item"
        style="margin-right: 15px"
      >
        <el-button
          style="border-radius: 15px"
          size="small"
          @click="getDisconnected()"
          >Disconnected</el-button
        >
      </el-badge>
      <el-badge
        :value="errorNum"
        class="item"
        type="warning"
        style="margin-right: 15px"
      >
        <el-button style="border-radius: 15px" size="small" @click="getError()"
          >Error</el-button
        >
      </el-badge>
    </span>

    <div :style="getEquipStyle()">
      <el-table
        :data="
          equip_infos.slice(
            (currentPage - 1) * pageSize,
            currentPage * pageSize
          )
        "
        style="width: 100%"
      >
        <el-table-column prop="Owner" label="Owner"> </el-table-column>
        <el-table-column prop="System" label="System"> </el-table-column>
        <el-table-column prop="IP" label="IP"> </el-table-column>
        <el-table-column label="SSH">
          <template slot-scope="scope">
            <el-tag type="danger" v-if="scope.row['Connected'] == 0"
              >Disconnected</el-tag
            >
            <el-tag type="success" v-if="scope.row['Connected'] == 1"
              >Connected</el-tag
            >
            <el-tag v-if="scope.row['Connected'] == 2">Connecting</el-tag>
            <el-tag type="warning" v-if="scope.row['Connected'] == 3"
              >Error</el-tag
            >
            <el-button
              type="warning"
              icon="el-icon-refresh-right"
              circle
              @click="flashStatus(scope.row)"
              style="margin-left: 10px"
              size="small"
              plain
              :disabled="$store.state.role == 'Visitor'"
            ></el-button>
          </template>
        </el-table-column>
        <el-table-column prop="Type" label="Type"> </el-table-column>
        <el-table-column prop="Rack" label="Rack"> </el-table-column>
        <el-table-column label="Operation">
          <template slot-scope="scope">
            <el-button
              type="primary"
              icon="el-icon-edit"
              circle
              @click="editClick(scope.row)"
              style="margin-right: 10px"
              :disabled="$store.state.role == 'Visitor'"
            ></el-button>

            <el-popconfirm
              confirm-button-text="OK"
              cancel-button-text="NO"
              icon="el-icon-info"
              icon-color="red"
              title="Click OK to confirm the deletion"
              @confirm="deleteClick(scope.row)"
              style="margin-right: 10px"
            >
              <template #reference>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  :disabled="$store.state.role == 'Visitor'"
                ></el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <div class="block" style="margin-top: 15px">
        <el-pagination
          align="center"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[1, 5, 10, 20]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="equip_infos.length"
        >
        </el-pagination>
      </div>
    </div>

    <el-dialog
      title="Edit Equip"
      :visible.sync="editBox"
      width="50%"
      :before-close="handleClose"
    >
      <el-form
        ref="editEquipData"
        label-width="100px"
        :model="editEquipData"
        :rules="rules"
      >
        <el-form-item label="Owner:" required prop="owner">
          <el-select
            v-model="editOwner"
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
            v-model="editEquipData.ip"
          ></el-input>
        </el-form-item>
        <el-form-item label="System:" prop="system">
          <el-select
            v-model="editSystem"
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
            v-model="editEquipData.rack"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="
            this.editEquipData.type == 'ONT' || this.editEquipData.type == 'VM'
          "
          label="Username"
          prop="username"
        >
          <el-input
            placeholder="ssh login username"
            maxlength="50"
            v-model="editEquipData.username"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="
            this.editEquipData.type == 'ONT' || this.editEquipData.type == 'VM'
          "
          label="Password"
          prop="password"
        >
          <el-input
            placeholder="ssh login password"
            maxlength="50"
            v-model="editEquipData.password"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="this.editEquipData.type == 'ONT'"
          label="Port"
          prop="port"
        >
          <el-input
            placeholder="ssh port"
            maxlength="50"
            v-model="editEquipData.port"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" plain @click="editEquip">Confirm</el-button>
        <el-button type="danger" plain @click="closeBox">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "TestbedsInfo",
  props: ["equipType"],
  data() {
    return {
      rules: {
        owner: [
          { required: true, message: "please input owner", trigger: "blur" },
        ],
        ip: [{ required: true, message: "please input IP", trigger: "blur" }],
        type: [
          { required: true, message: "please select type", trigger: "blur" },
        ],
      },
      //定义数据
      type: this.equipType,
      disconnectedNum: 0,
      errorNum: 0,
      equip_infos: [],
      equip: {},
      equipShow: false,
      editBox: false,
      pageSize: 10,
      owners: [],
      systems: [],
      selectedOwner: "",
      currentPage: 1,
      editOwner: "",
      editSystem: "",
      editEquipData: {
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
    };
  },
  mounted() {
    this.getDisconnected();
    this.getError();
    this.getEquipData();
    this.getOwnerData();
    this.getSystemData();
  },

  watch: {
    selectedOwner(newName, oldName) {
      this.currentPage = 1;
      this.getEquipData();
    },
    editOwner(newName, oldName) {
      this.editEquipData.owner = newName;
      this.$refs.owners.createdLabel = null;
    },
    editSystem(newName, oldName) {
      this.editEquipData.system = newName;
      this.$refs.owners.createdLabel = null;
    },
  },

  methods: {
    // 获得设备数据
    getEquipData: function () {
      this.equipShow = true;
      var result;
      $.ajax({
        //url
        url:
          "/api/show_data?owners=" + this.selectedOwner + "&type=" + this.type,
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
          console.log("show_all_data出错");
        },
      });
      this.equip_infos = result;
    },

    getOwnerData: function () {
      var result;
      $.ajax({
        //url
        url: "/api/check_owners?type=" + this.type,
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
        url: "/api/check_systems?type=" + this.type,
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

    getDisconnected: function () {
      var result;
      $.ajax({
        //url
        url: "/api/check_disconnected?type=" + this.type,
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
          console.log("check_disconnected出错");
        },
      });
      this.equip_infos = result;
      this.disconnectedNum = result.length;
    },

    getError: function () {
      var result;
      $.ajax({
        //url
        url: "/api/check_error?type=" + this.type,
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
          console.log("check_error出错");
        },
      });
      this.equip_infos = result;
      this.errorNum = result.length;
    },

    // 删除设备
    deleteClick: function (data) {
      var id = data["id"];
      $.ajax({
        //url
        url: "/api/delete_equip?id=" + id,
        //请求类型：
        type: "GET",
        //响应体结果：
        dataType: "json",
        //将ajax改为同步执行
        async: false,
        //成功回调：
        success: function (data) {
          console.log("delete成功");
        },
        //超时时间：
        timeout: 2000,
        //失败回调：
        error: function () {
          console.log("delete出错");
        },
      });

      this.getEquipData();
    },

    // 编辑设备
    editClick: function (data) {
      this.editBox = true;
      this.equip = data;
      this.editEquipData = {
        id: data["id"],
        owner: data["Owner"],
        system: data["System"],
        ip: data["IP"],
        type: this.type,
        rack: data["Rack"],
        username: data["Username"],
        password: data["Password"],
        port: data["Port"],
      };
      this.$nextTick(function () {
        this.editOwner = data["Owner"];
        this.editSystem = data["System"];
      });
    },

    editEquip: function () {
      this.$refs.editEquipData.validate((valid) => {
        if (!valid) {
          this.$message({
            message: "Required items not completed！！！",
            type: "warning",
          });
        } else {
          $.ajax({
            //url
            url: "/api/edit_equip",
            //请求类型：
            type: "POST",
            //响应体结果：
            dataType: "json",
            data: this.editEquipData,
            //成功回调：
            success: (data) => {
              this.$message({
                showClose: true,
                message: "Success!",
                type: "success",
              });
              this.getEquipData();
            },
            //超时时间：
            async: false,
            timeout: 20000,
            //失败回调：
            error: () => {},
          });
          this.editBox = false;
          this.editEquipData = {
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

    flashStatus: function (data) {
      $.ajax({
        //url
        url: "/api/flash_status?",
        //请求类型：
        type: "POST",
        //响应体结果：
        dataType: "json",
        data: data,
        //成功回调：
        success: (data) => {
          this.$message({
            showClose: true,
            message: "flash successfully!",
            type: "success",
          });
          this.getEquipData();
        },
        //超时时间：
        timeout: 60000,
        //失败回调：
        error: () => {
          console.log("time");
        },
      });
    },

    // 取消弹窗
    closeBox: function () {
      this.editBox = false;
      this.editOwner = "";
      this.editSystem = "";
    },
    // 下一页
    current_change: function (currentPage) {
      this.currentPage = currentPage;
    },
    // 控制显示隐藏:
    getEquipStyle: function () {
      if (this.equipShow == false) {
        return { display: "none" };
      } else {
        return {};
      }
    },

    handleSizeChange(val) {
      this.currentPage = 1;
      this.pageSize = val;
    },
    //当前页改变时触发 跳转其他页
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    handleClose(done) {
      done();
    },

    //el-select全选功能
    selectAll() {
      if (this.selectedOwner.length < this.owners.length) {
        this.selectedOwner = [];
        this.owners.map((item) => {
          this.selectedOwner.push(item.owner);
        });
        this.selectedOwner.unshift("allOwners");
      } else {
        this.selectedOwner = [];
      }
    },
    changeSelect(val) {
      if (!val.includes("allOwners") && val.length === this.owners.length) {
        this.selectedOwner.unshift("allOwners");
      } else if (
        val.includes("allOwners") &&
        val.length - 1 < this.owners.length
      ) {
        this.selectedOwner = this.selectedOwner.filter((item) => {
          return item !== "allOwners";
        });
      }
    },
    removeTag(val) {
      if (val === "allOwners") {
        this.selectedOwner = [];
      }
    },
  },
};
</script>