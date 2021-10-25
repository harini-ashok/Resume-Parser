<template>
  <div>
    <b-col>
      <b-card
        :title="name"
        img-src="https://picsum.photos/600/300/?image=25"
        img-alt="Image"
        img-top
        tag="article"
        style="max-width: 20rem;"
        class="mb-2"
      >
        <!-- <b-card-text>
          Some quick example text to build on the card title and make up the
          bulk of the card's content.
        </b-card-text> -->
        <!--router-link :to="`/resume/${id}`"-->
        <router-link :to="{ name: 'resumeid', params: { id: id } }">
          <b-button v-b-modal="modalId" variant="dark">
            Click to view resume
          </b-button>
        </router-link>
      </b-card>
    </b-col>
  </div>
</template>

<script>
export default {
  props: [
    "name",
    "id",
    "email",
    "mobile",
    "skills",
    "education",
    "graduation_years",
    "city",
    "state",
    "experience",
    "college",
  ],
  computed: {
    modalId() {
      return `modal-${this.id}`;
    },
  },
};
</script>

<style scoped></style>
