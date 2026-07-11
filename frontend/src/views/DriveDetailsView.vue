<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const drive = ref(null)
const loading = ref(true)
const error = ref('')

const applying = ref(false)
const successMessage = ref('')
const applyError = ref('')

const formatStatus = (status) => {
  if (!status) {
    return ''
  }

  return status
    .replaceAll('_', ' ')
    .replace(/\b\w/g, letter => letter.toUpperCase())
}

// Load complete drive details
const loadDriveDetails = async () => {
  try {
    loading.value = true
    error.value = ''

    const response = await api.get(
      `/student/drives/${route.params.id}`
    )

    drive.value = response.data
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to load drive details'
  } finally {
    loading.value = false
  }
}

// Apply for the current drive
const applyForDrive = async () => {
  try {
    applying.value = true
    successMessage.value = ''
    applyError.value = ''

    const response = await api.post(
      `/student/drives/${route.params.id}/apply`
    )

    successMessage.value = response.data.message

    drive.value.has_applied = true
    drive.value.application_status = response.data.status
  } catch (err) {
    applyError.value =
      err.response?.data?.error ||
      'Unable to submit application'
  } finally {
    applying.value = false
  }
}

// Return to available drives
const goBack = () => {
  router.push('/student/drives')
}

onMounted(() => {
  loadDriveDetails()
})
</script>

<template>
  <div class="min-vh-100 bg-light">

    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-primary">
      <div class="container">
        <span class="navbar-brand mb-0 h1">
          Placement Portal
        </span>

        <button
          type="button"
          class="btn btn-outline-light"
          @click="goBack"
        >
          Back to Drives
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="container py-5">

      <!-- Loading -->
      <div
        v-if="loading"
        class="alert alert-info"
      >
        Loading drive details...
      </div>

      <!-- Drive Loading Error -->
      <div
        v-else-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>

      <!-- Drive Details -->
      <div
        v-else-if="drive"
        class="card shadow-sm"
      >
        <div class="card-body p-4 p-md-5">

          <!-- Job and Company -->
          <div class="mb-4">
            <h2 class="mb-2">
              {{ drive.job_title }}
            </h2>

            <h5 class="text-primary">
              {{ drive.company_name }}
            </h5>
          </div>

          <hr>

          <!-- Job Description -->
          <div class="mb-4">
            <h5>
              Job Description
            </h5>

            <p class="text-muted mb-0">
              {{ drive.job_description }}
            </p>
          </div>

          <!-- Eligibility -->
          <h5 class="mb-3">
            Eligibility Criteria
          </h5>

          <div class="row g-3 mb-4">

            <!-- Branch -->
            <div class="col-md-4">
              <div class="border rounded p-3 h-100">
                <small class="text-muted">
                  Eligible Branch
                </small>

                <div class="fw-bold mt-1">
                  {{ drive.eligibility_branch }}
                </div>
              </div>
            </div>

            <!-- CGPA -->
            <div class="col-md-4">
              <div class="border rounded p-3 h-100">
                <small class="text-muted">
                  Minimum CGPA
                </small>

                <div class="fw-bold mt-1">
                  {{ drive.eligibility_cgpa }}
                </div>
              </div>
            </div>

            <!-- Graduation Year -->
            <div class="col-md-4">
              <div class="border rounded p-3 h-100">
                <small class="text-muted">
                  Graduation Year
                </small>

                <div class="fw-bold mt-1">
                  {{ drive.eligibility_year }}
                </div>
              </div>
            </div>

          </div>

          <!-- Deadline -->
          <div class="alert alert-warning">
            <strong>Application Deadline:</strong>
            {{ drive.deadline }}
          </div>
                  <!-- Application Status -->
                  <div
                    v-if="drive.has_applied"
                    class="alert alert-info"
                  >
                    <strong>Application Status:</strong>
                    {{ formatStatus(drive.application_status) }}
                  </div>

                  <!-- Success Message -->
          <div
            v-if="successMessage"
            class="alert alert-success"
          >
            {{ successMessage }}
          </div>

          <!-- Apply Error -->
          <div
            v-if="applyError"
            class="alert alert-danger"
          >
            {{ applyError }}
          </div>

          <!-- Action Buttons -->
          <div class="d-flex gap-2 mt-4">

            <button
              v-if="!drive.has_applied"
              type="button"
              class="btn btn-primary px-4"
              :disabled="applying"
              @click="applyForDrive"
            >
              {{ applying ? 'Applying...' : 'Apply Now' }}
            </button>

            <button
              v-else
              type="button"
              class="btn btn-success px-4"
              disabled
            >
              Already Applied
            </button>

            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="goBack"
            >
              Go Back
            </button>

          </div>

        </div>
      </div>

    </main>
  </div>
</template>