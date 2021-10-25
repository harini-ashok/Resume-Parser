<template class="name">
  <body>
    <div class="header">
      <h2>Name</h2>
      <p>{{ name }}</p>
    </div>

    <div class="row">
      <div class="leftcolumn">
        <div class="card">
          <h2>Work experience</h2>
          <p>{{ id }}</p>
        </div>
        <div class="card">
          <h3>Skills</h3>
          <h4>{{ skills }}</h4>
          <p></p>
        </div>

        <div class="card">
          <h3>Education</h3>
          <h4>{{ education }}</h4>
          <h3>College Name</h3>

          <p>{{ college }}</p>
        </div>
      </div>
      <div class="rightcolumn">
        <div class="card">
          <h3>Email ID</h3>
          <h5>{{ email }}</h5>
          <h3>Phone Number</h3>
          <h5>{{ mobile }}</h5>
        </div>

        <div class="card">
          <h3>City and State</h3>
          <p>{{ city }}</p>
          <br />
          <p>{{ state }}</p>
        </div>
      </div>
    </div>
  </body>
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
* {
  box-sizing: border-box;
}

/* Add a gray background color with some padding */
body {
  font-family: Arial;
  padding: 20px;
  background: #f1f1f1;
}

/* Header/Blog Title */
.header {
  padding: 30px;
  font-size: 40px;
  text-align: center;
  background: white;
}

/* Create two unequal columns that floats next to each other */
/* Left column */
.leftcolumn {
  float: left;
  width: 65%;
}

/* Right column */
.rightcolumn {
  float: left;
  width: 35%;
  padding-left: 20px;
}

/* Add a card effect for articles */
.card {
  background-color: #ddd;
  padding: 20px;
  margin-top: 20px;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Responsive layout - when the screen is less than 800px wide, make the two columns stack on top of each other instead of next to each other */
@media screen and (max-width: 800px) {
  .leftcolumn,
  .rightcolumn {
    width: 100%;
    padding: 0;
  }
}
</style>
