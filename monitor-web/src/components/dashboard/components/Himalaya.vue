<template>
  <div>
    <el-upload
      action="/uploadTopoPic"
      style="float: right"
      :show-file-list="false"
      :on-success="handlePictureSuccess"
      :before-upload="beforePictureUpload"
      :disabled="$store.state.role == 'Visitor'"
    >
      <el-button plain type="primary" :disabled="$store.state.role == 'Visitor'"
        >Update</el-button
      >
    </el-upload>
    <div style="text-align: center">
      <img src="@/assets/Himalaya.png" alt="Himalaya" style="width: 80%" />
    </div>
  </div>
</template>

<script>
export default {
  name: "Himalaya",
  computed: {},
  methods: {
    handlePictureSuccess() {
      this.$message.success("Upload Successfully");
    },
    beforePictureUpload(file) {
      const isPNG = file.type === "image/png";
      const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isJPG && !isPNG) {
        this.$message.error("The image must be format of JPG or PNG!");
      }
      if (!isLt2M) {
        this.$message.error(
          "The size of uploaded image must be less than 2MB!"
        );
      }
      return (isPNG || isJPG) && isLt2M;
    },
  },
};
</script>