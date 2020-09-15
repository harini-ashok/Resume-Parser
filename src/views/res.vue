<template>
  <div class="res">
    <b-container>
      <b-row align-h="center">
        <div
          v-for="job in getDisplayJobs"
          :name="job.name"
          :id="job.id"
          :email="job.email"
          :mobile="job.mobile"
          :skills="job.skills"
          :education="job.education"
          :graduation="job.graduation_years"
          :city="job.city"
          :state="job.state"
          :experience="job.experience"
          :college="job.college"
          :key="job.id"
        >
          <resume-display
          v-if="job.id === $route.params.id"
            :name="job.name"
            :id="job.id"
            :email="job.email"
            :mobile="job.mobile"
            :skills="job.skills"
            :education="job.education"
            :graduation="job.graduation_years"
            :city="job.city"
            :state="job.state"
            :experience="job.experience"
            :college="job.college"
          ></resume-display>
        </div>
        <p></p>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import resume from "@/components/resume.vue";
import { mapGetters } from "vuex";

export default {
  name: "res",
  async mounted() {
    console.log("hello world");
    this.getRecords();
    console.log("Helloworld123");
  },
  components: { "resume-display": resume },
  computed: {
    ...mapGetters(["getRows", "getDisplayJobs"]),
  },
  methods: {
    async getRecords() {
      console.log("hello world222");
      await this.$store.dispatch("fetchJobs");
      console.log("hello world3333");
    },
  },

  // computed: {
  //   matchID() {
  //     return this.getDisplayJobs.filter(p => p !==  $route.params.id );
  //   }
  // }
};
</script>
<style lang="scss" scoped>
// b-card {
// padding: 10px;
// }
</style>
