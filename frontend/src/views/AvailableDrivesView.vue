<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const drives = ref([])
const loading = ref(true)
const error = ref('')

const loadDrives = async () => {
  try {
    const response = await api.get('/student/drives')
    drives.value = response.data
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to load placement drives'
  } finally {
    loading.value = false
  }
}

const goToDashboard = () => {
  router.push('/student/dashboard')
}

const viewDetails = (driveId) => {
  router.push(`/student/drives/${driveId}`)
}

onMounted(() => {
  loadDrives()
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
          @click="goToDashboard"
        >
          Dashboard
        </button>
      </div>
    </nav>

    <main class="container py-5">
      <div class="mb-4">
        <h2>Available Placement Drives</h2>
        <p class="text-muted">
          Browse approved placement opportunities
        </p>
      </div>

      <div
        v-if="loading"
        class="alert alert-info"
      >
        Loading placement drives...
      </div>

      <div
        v-else-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>

      <div
        v-else-if="drives.length === 0"
        class="alert alert-secondary"
      >
        No placement drives are currently available.
      </div>

      <div
        v-else
        class="row g-4"
      >
        <div
          v-for="drive in drives"
          :key="drive.id"
          class="col-md-6 col-lg-4"
        >
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h4 class="card-title">
                {{ drive.job_title }}
              </h4>

              <h6 class="text-primary mb-4">
                {{ drive.company_name }}
              </h6>

              <p class="mb-2">
                <strong>Branch:</strong>
                {{ drive.eligibility_branch }}
              </p>

              <p class="mb-2">
                <strong>Minimum CGPA:</strong>
                {{ drive.eligibility_cgpa }}
              </p>

              <p class="mb-2">
                <strong>Graduation Year:</strong>
                {{ drive.eligibility_year }}
              </p>

              <p class="mb-4">
                <strong>Deadline:</strong>
                {{ drive.deadline }}
              </p>

              <button
                class="btn btn-primary w-100"
                @click="viewDetails(drive.id)"
              >
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>