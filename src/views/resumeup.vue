<template>
  <div class="resumeup">
    <b-container>
      <b-row align-h="center">
        <resume-upload></resume-upload>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import resumeupload from "@/components/resumeupload.vue";

export default {
  name: "resumeup",
  components: { "resume-upload": resumeupload }
};
</script>
<style lang="scss" scoped>
// b-card {
// padding: 10px;
// }
</style>
