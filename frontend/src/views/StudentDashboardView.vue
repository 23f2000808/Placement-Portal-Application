<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const student = ref(null)
const loading = ref(true)
const error = ref('')

const loadDashboard = async () => {
  try {
    const response = await api.get('/student/dashboard')
    student.value = response.data
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to load dashboard'
  } finally {
    loading.value = false
  }
}

const logout = async () => {
  try {
    await api.post('/logout')
    router.push('/login')
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Logout failed'
  }
}

const viewDrives = () => {
  router.push('/student/drives')
}

const viewApplications = () => {
  router.push('/student/applications')
}

const editProfile = () => {
  router.push('/student/profile')
}

const exportApplications = async () => {
  try {
    const res = await api.post('/student/export')
    alert(res.data.message)
  } catch (err) {
    alert(
      err.response?.data?.error ||
      'Export failed.'
    )
  }
}

onMounted(() => {
  loadDashboard()
})
</script>

<template>
  <div class="min-vh-100 bg-light">
    <nav class="navbar navbar-dark bg-primary">
      <div class="container">
        <span class="navbar-brand mb-0 h1">
          Placement Portal
        </span>
        <button
        class="btn btn-outline-light"
        @click="logout"
        >
         Logout
        </button>
      </div>
    </nav>

    <main class="container py-5">
      <div class="mb-4">
        <h2>Student Dashboard</h2>
        <p class="text-muted">
          Welcome to your placement portal
        </p>

        <div class="d-flex gap-2 mt-3">
          <button
            class="btn btn-primary"
            @click="viewDrives"
          >
            Available Drives
          </button>

          <button
            class="btn btn-outline-primary"
            @click="viewApplications"
          >
            My Applications
          </button>

          <button
            class="btn btn-outline-primary"
            @click="editProfile"
          >
            Edit Profile
          </button>

          <button
            class="btn btn-success"
            @click="exportApplications"
          >
            Export Application History
          </button>
        </div>
      </div>

      <div
        v-if="loading"
        class="alert alert-info"
      >
        Loading dashboard...
      </div>

      <div
        v-else-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>

      <template v-else-if="student">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h4 class="mb-4">
              Student Profile
            </h4>

            <div class="row g-4">
              <div class="col-md-6">
                <p class="text-muted mb-1">Name</p>
                <h5>{{ student.name }}</h5>
              </div>

              <div class="col-md-6">
                <p class="text-muted mb-1">Email</p>
                <h5>{{ student.email }}</h5>
              </div>

              <div class="col-md-6">
                <p class="text-muted mb-1">
                  Department
                </p>
                <h5>{{ student.department }}</h5>
              </div>

              <div class="col-md-6">
                <p class="text-muted mb-1">CGPA</p>
                <h5>{{ student.cgpa }}</h5>
              </div>

              <div class="col-md-6">
                <p class="text-muted mb-1">
                  Graduation Year
                </p>
                <h5>
                  {{ student.graduation_year }}
                </h5>
              </div>

              <div class="col-md-6">
                <p class="text-muted mb-1">
                  Resume
                </p>

                <span
                  v-if="student.resume_uploaded"
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
            </div>
          </div>
        </div>

        <div class="row mt-4">
          <div class="col-md-4">
            <div class="card shadow-sm text-center">
              <div class="card-body">
                <h2>
                  {{ student.total_applications }}
                </h2>

                <p class="text-muted mb-0">
                  Total Applications
                </p>
              </div>
            </div>
          </div>
        </div>

      </template>
    </main>
  </div>
</template>