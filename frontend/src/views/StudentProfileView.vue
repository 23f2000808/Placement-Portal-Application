<template>
  <div class="min-vh-100 bg-light">

    <nav class="navbar navbar-dark bg-primary">
      <div class="container">
        <span class="navbar-brand fw-semibold">
          Placement Portal
        </span>

        <button
          class="btn btn-outline-light"
          @click="goToDashboard"
        >
          Dashboard
        </button>
      </div>
    </nav>

    <main class="container py-5">

      <div class="mb-4">
        <h1 class="h2 mb-1">Edit Profile</h1>

        <p class="text-muted mb-0">
          Update your academic and personal information
        </p>
      </div>

      <div
        v-if="successMessage"
        class="alert alert-success"
      >
        {{ successMessage }}
      </div>

      <div
        v-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>

      <div
        v-if="loading"
        class="text-center py-5"
      >
        <div class="spinner-border text-primary"></div>

        <p class="text-muted mt-3">
          Loading profile...
        </p>
      </div>

      <div
        v-else
        class="card shadow-sm"
      >
        <div class="card-body p-4">

          <form @submit.prevent="updateProfile">

            <div class="row g-4">

              <div class="col-md-6">
                <label class="form-label">
                  Name
                </label>

                <input
                  v-model.trim="form.name"
                  type="text"
                  class="form-control"
                  required
                >
              </div>

              <div class="col-md-6">
                <label class="form-label">
                  Email
                </label>

                <input
                  :value="form.email"
                  type="email"
                  class="form-control"
                  disabled
                >

                <div class="form-text">
                  Email cannot be changed.
                </div>
              </div>

              <div class="col-md-6">
                <label class="form-label">
                  Department
                </label>

                <input
                  v-model.trim="form.department"
                  type="text"
                  class="form-control"
                  required
                >
              </div>

              <div class="col-md-6">
                <label class="form-label">
                  CGPA
                </label>

                <input
                  v-model.number="form.cgpa"
                  type="number"
                  min="0"
                  max="10"
                  step="0.01"
                  class="form-control"
                  required
                >
              </div>

              <div class="col-md-6">
                <label class="form-label">
                  Graduation Year
                </label>

                <input
                  v-model.number="form.graduation_year"
                  type="number"
                  min="2000"
                  max="2100"
                  class="form-control"
                  required
                >
              </div>


             <div class="col-md-6">

  <label class="form-label">
    Resume Status
  </label>

  <div class="form-control bg-light mb-3">

    <span
      v-if="form.resume_uploaded"
      class="badge bg-success"
    >
      Uploaded
    </span>

    <span
      v-else
      class="badge bg-secondary"
    >
      Not Uploaded
    </span>

  </div>

  <input
    type="file"
    class="form-control"
    accept=".pdf"
    @change="handleResumeChange"
  >

  <button
    type="button"
    class="btn btn-primary mt-3"
    @click="uploadResume"
    :disabled="uploading"
  >

    <span
      v-if="uploading"
      class="spinner-border spinner-border-sm me-2"
    ></span>

    {{ uploading ? 'Uploading...' : 'Upload Resume' }}

  </button>

  <div
    v-if="uploadSuccess"
    class="alert alert-success mt-3"
  >
    {{ uploadSuccess }}
  </div>

  <div
    v-if="uploadError"
    class="alert alert-danger mt-3"
  >
    {{ uploadError }}
  </div>

</div>

            </div>

            <hr class="my-4">

            <div class="d-flex gap-2">

              <button
                type="submit"
                class="btn btn-primary"
                :disabled="saving"
              >
                <span
                  v-if="saving"
                  class="spinner-border spinner-border-sm me-2"
                ></span>

                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>

              <button
                type="button"
                class="btn btn-outline-secondary"
                @click="goToDashboard"
              >
                Cancel
              </button>

            </div>

          </form>

        </div>
      </div>

    </main>

  </div>
</template>


<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const successMessage = ref('')
const selectedResume = ref(null)
const uploading = ref(false)
const uploadSuccess = ref('')
const uploadError = ref('')

const form = reactive({
  name: '',
  email: '',
  department: '',
  cgpa: '',
  graduation_year: '',
  resume_uploaded: false
})


const loadProfile = async () => {
  try {
    error.value = ''

    const response = await api.get('/student/profile')

    form.name = response.data.name
    form.email = response.data.email
    form.department = response.data.department
    form.cgpa = response.data.cgpa
    form.graduation_year = response.data.graduation_year
    form.resume_uploaded = response.data.resume_uploaded

  } catch (err) {

    if (
      err.response?.status === 401 ||
      err.response?.status === 403
    ) {
      router.push('/login')
      return
    }

    error.value =
      err.response?.data?.error ||
      'Unable to load profile'

  } finally {
    loading.value = false
  }
}


const updateProfile = async () => {
  try {
    saving.value = true
    error.value = ''
    successMessage.value = ''

    const response = await api.put(
      '/student/profile',
      {
        name: form.name,
        department: form.department,
        cgpa: form.cgpa,
        graduation_year: form.graduation_year
      }
    )

    successMessage.value = response.data.message

    form.name = response.data.student.name
    form.department = response.data.student.department
    form.cgpa = response.data.student.cgpa
    form.graduation_year =
      response.data.student.graduation_year

  } catch (err) {

    error.value =
      err.response?.data?.error ||
      'Unable to update profile'

  } finally {
    saving.value = false
  }
}

const handleResumeChange = (event) => {
  selectedResume.value = event.target.files[0]
}

const uploadResume = async () => {

  uploadSuccess.value = ''
  uploadError.value = ''

  if (!selectedResume.value) {
    uploadError.value = 'Please select a PDF file.'
    return
  }

  const formData = new FormData()

  formData.append(
    'resume',
    selectedResume.value
  )

  try {

    uploading.value = true

    const response = await api.post(
      '/student/resume',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    uploadSuccess.value = response.data.message

    form.resume_uploaded = true

  }

  catch (err) {

    uploadError.value =
      err.response?.data?.error ||
      'Resume upload failed.'

  }

  finally {

    uploading.value = false

  }

}

const goToDashboard = () => {
  router.push('/student/dashboard')
}


onMounted(loadProfile)
</script>