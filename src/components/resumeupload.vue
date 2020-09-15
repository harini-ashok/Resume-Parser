<template>
  <div>
    <b-form-file v-model="file" ref="file-input" class="mb-2"></b-form-file>
    <p class="mt-2">
      Selected file: <b>{{ file ? file.name : "" }}</b>
    </p>
    <b-button @click="file = null">Upload Resume</b-button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: null,
    };
  },
};
</script>
