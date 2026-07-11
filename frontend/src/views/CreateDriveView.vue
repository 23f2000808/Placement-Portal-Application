<template>
  <div class="min-vh-100 bg-light">

    <nav class="navbar navbar-dark bg-primary">
      <div class="container">
        <span class="navbar-brand fw-semibold">
          Placement Portal
        </span>

        <button
          class="btn btn-outline-light"
          @click="goBack"
        >
          Company Dashboard
        </button>
      </div>
    </nav>

    <main class="container py-5">

      <div class="row justify-content-center">
        <div class="col-lg-8">

          <div class="mb-4">
            <h1 class="h2">Create a Placement Drive</h1>
            <p class="text-muted mb-0">
              Add a new placement opportunity for eligible students
            </p>
          </div>

          <div
            v-if="error"
            class="alert alert-danger"
          >
            {{ error }}
          </div>

          <div class="card shadow-sm">
            <div class="card-body p-4">

              <form @submit.prevent="createDrive">

                <div class="mb-3">
                  <label class="form-label">
                    Job Title
                  </label>

                  <input
                    v-model.trim="form.job_title"
                    type="text"
                    class="form-control"
                    required
                  >
                </div>

                <div class="mb-3">
                  <label class="form-label">
                    Job Description
                  </label>

                  <textarea
                    v-model.trim="form.job_description"
                    class="form-control"
                    rows="5"
                    required
                  ></textarea>
                </div>

                <h5 class="mt-4 mb-3">
                  Eligibility Criteria
                </h5>

                <div class="row">

                  <div class="col-md-4 mb-3">
                    <label class="form-label">
                      Eligible Branch
                    </label>

                    <input
                      v-model.trim="form.eligibility_branch"
                      type="text"
                      class="form-control"
                      placeholder="CSE"
                      required
                    >
                  </div>

                  <div class="col-md-4 mb-3">
                    <label class="form-label">
                      Minimum CGPA
                    </label>

                    <input
                      v-model.number="form.eligibility_cgpa"
                      type="number"
                      class="form-control"
                      min="0"
                      max="10"
                      step="0.1"
                      required
                    >
                  </div>

                  <div class="col-md-4 mb-3">
                    <label class="form-label">
                      Graduation Year
                    </label>

                    <input
                      v-model.number="form.eligibility_year"
                      type="number"
                      class="form-control"
                      required
                    >
                  </div>

                </div>

                <div class="mb-4">
                  <label class="form-label">
                    Application Deadline
                  </label>

                  <input
                    v-model="form.deadline"
                    type="date"
                    class="form-control"
                    required
                  >
                </div>

                <div class="d-flex gap-2">

                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="loading"
                  >
                    {{
                      loading
                        ? 'Creating...'
                        : 'Create Drive'
                    }}
                  </button>

                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    :disabled="loading"
                    @click="goBack"
                  >
                    Cancel
                  </button>

                </div>

              </form>

            </div>
          </div>

        </div>
      </div>

    </main>

  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const loading = ref(false)
const error = ref('')

const form = reactive({
  job_title: '',
  job_description: '',
  eligibility_branch: '',
  eligibility_cgpa: null,
  eligibility_year: null,
  deadline: ''
})

const createDrive = async () => {
  try {
    loading.value = true
    error.value = ''

    await api.post('/company/create-drive', {
      job_title: form.job_title,
      job_description: form.job_description,
      eligibility_branch: form.eligibility_branch,
      eligibility_cgpa: form.eligibility_cgpa,
      eligibility_year: form.eligibility_year,
      deadline: form.deadline
    })

    router.push('/company/dashboard')

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to create placement drive'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/company/dashboard')
}
</script>