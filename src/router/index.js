import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import resumeup from "../views/resumeup.vue";
import res from "../views/res.vue";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/resumeup",
    name: "resumeup",
    component: resumeup
  },
  {
    path: "/resume/:id",
    name: "resumeid",
    component: res
  }
];

//add route here

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router; 



