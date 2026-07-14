<template>
  <div class="container mt-5">

    <div class="row justify-content-center">

      <div class="col-md-6">

        <div class="text-center mb-4">
          <h1>Placement Portal</h1>
          <p class="text-muted">Create your account</p>
        </div>

        <div class="card shadow">

          <div class="card-body">

            <ul class="nav nav-tabs mb-4">

              <li class="nav-item">

                <button
                  class="nav-link"
                  :class="{ active: role === 'student' }"
                  @click="role='student'"
                >
                  Student
                </button>

              </li>

              <li class="nav-item">

                <button
                  class="nav-link"
                  :class="{ active: role === 'company' }"
                  @click="role='company'"
                >
                  Company
                </button>

              </li>

            </ul>

            <div
              v-if="success"
              class="alert alert-success"
            >
              {{ success }}
            </div>

            <div
              v-if="error"
              class="alert alert-danger"
            >
              {{ error }}
            </div>

            <!-- STUDENT FORM -->

            <form
              v-if="role==='student'"
              @submit.prevent="registerStudent"
            >

              <div class="mb-3">

                <label>Name</label>

                <input
                  v-model="student.name"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-3">

                <label>Email</label>

                <input
                  type="email"
                  v-model="student.email"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-3">

                <label>Password</label>

                <input
                  type="password"
                  v-model="student.password"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-3">

                <label>Department</label>

                <input
                  v-model="student.department"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-3">

                <label>CGPA</label>

                <input
                  type="number"
                  step="0.01"
                  v-model="student.cgpa"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-4">

                <label>Graduation Year</label>

                <input
                  type="number"
                  v-model="student.graduation_year"
                  class="form-control"
                  required
                >

              </div>

              <button
                class="btn btn-primary w-100"
              >
                Register Student
              </button>

            </form>

            <!-- COMPANY FORM -->

            <form
              v-else
              @submit.prevent="registerCompany"
            >

              <div class="mb-3">

                <label>Company Name</label>

                <input
                  v-model="company.company_name"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-3">

                <label>Email</label>

                <input
                  type="email"
                  v-model="company.email"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-3">

                <label>Password</label>

                <input
                  type="password"
                  v-model="company.password"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-3">

                <label>Website</label>

                <input
                  v-model="company.website"
                  class="form-control"
                  required
                >

              </div>

              <div class="mb-4">

                <label>HR Contact</label>

                <input
                  v-model="company.hr_contact"
                  class="form-control"
                  required
                >

              </div>

              <button
                class="btn btn-success w-100"
              >
                Register Company
              </button>

            </form>

            <hr>

            <p class="text-center">

              Already have an account?

              <router-link to="/login">

                Login

              </router-link>

            </p>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import api from "../services/api";

export default {

  name: "RegisterView",

  data() {

    return {

      role: "student",

      success: "",

      error: "",

      student: {

        name: "",
        email: "",
        password: "",
        department: "",
        cgpa: "",
        graduation_year: ""

      },

      company: {

        company_name: "",
        email: "",
        password: "",
        website: "",
        hr_contact: ""

      }

    };

  },

  methods: {

    async registerStudent() {

      this.error="";
      this.success="";

      try{

        const res=await api.post(
          "/register/student",
          this.student
        );

        this.success=res.data.message;

        setTimeout(() => {
          this.$router.push("/login");
        }, 2000);

      }

      catch(err){

        this.error=
          err.response?.data?.error ||
          "Registration failed";

      }

    },

    async registerCompany(){

      this.error="";
      this.success="";

      try{

        const res=await api.post(
          "/register/company",
          this.company
        );

        this.success=res.data.message;

        setTimeout(() => {
          this.$router.push("/login");
        }, 2000);

      }

      catch(err){

        this.error=
          err.response?.data?.error ||
          "Registration failed";

      }

    }

  }

};
</script>
