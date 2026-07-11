<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const drive = ref(null)
const applications = ref([])
const totalApplications = ref(0)

const loading = ref(true)
const error = ref('')
const successMessage = ref('')
const updatingId = ref(null)

const loadApplications = async () => {
  try {
    loading.value = true
    error.value = ''

    const response = await api.get(
      `/company/drives/${route.params.id}/applications`
    )

    drive.value = response.data.drive
    applications.value = response.data.applications
    totalApplications.value = response.data.total_applications
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to load applications'
  } finally {
    loading.value = false
  }
}

const updateStatus = async (application, newStatus) => {
  try {
    updatingId.value = application.application_id
    error.value = ''
    successMessage.value = ''

    const response = await api.put(
      `/company/applications/${application.application_id}/status`,
      {
        status: newStatus
      }
    )

    application.status = response.data.status
    successMessage.value = response.data.message
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to update application status'
  } finally {
    updatingId.value = null
  }
}

const formatDate = (dateValue) => {
  if (!dateValue) {
    return 'N/A'
  }

  return new Date(dateValue).toLocaleDateString()
}

const formatStatus = (status) => {
  if (!status) {
    return 'Unknown'
  }

  return status
    .replaceAll('_', ' ')
    .replace(/\b\w/g, letter => letter.toUpperCase())
}

const statusClass = (status) => {
  const classes = {
    applied: 'bg-primary',
    shortlisted: 'bg-warning text-dark',
    interview_scheduled: 'bg-info text-dark',
    selected: 'bg-success',
    rejected: 'bg-danger'
  }

  return classes[status] || 'bg-secondary'
}

const goBack = () => {
  router.push('/company/dashboard')
}

onMounted(() => {
  loadApplications()
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
          type="button"
          class="btn btn-outline-light"
          @click="goBack"
        >
          Company Dashboard
        </button>
      </div>
    </nav>

    <main class="container py-5">
      <div v-if="loading" class="alert alert-info">
        Loading applications...
      </div>

      <div v-else-if="error && !drive" class="alert alert-danger">
        {{ error }}
      </div>

      <template v-else-if="drive">
        <div class="mb-4">
          <h2>{{ drive.job_title }} — Applicants</h2>

          <p class="text-muted mb-0">
            Total Applications: {{ totalApplications }}
          </p>
        </div>

        <div v-if="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>

        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <div
          v-if="applications.length === 0"
          class="alert alert-secondary"
        >
          No students have applied for this drive yet.
        </div>

        <div v-else class="card shadow-sm">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Academic Details</th>
                    <th>Applied On</th>
                    <th>Current Status</th>
                    <th>Update Status</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="application in applications"
                    :key="application.application_id"
                  >
                    <td>
                      <div class="fw-semibold">
                        {{ application.student_name }}
                      </div>

                      <small class="text-muted">
                        {{ application.email }}
                      </small>
                    </td>

                    <td>
                      <div>
                        {{ application.department }}
                      </div>

                      <small class="text-muted">
                        CGPA: {{ application.cgpa }}
                        |
                        Year: {{ application.graduation_year }}
                      </small>
                    </td>

                    <td>
                      {{ formatDate(application.application_date) }}
                    </td>

                    <td>
                      <span
                        class="badge"
                        :class="statusClass(application.status)"
                      >
                        {{ formatStatus(application.status) }}
                      </span>
                    </td>

                    <td>
                      <select
                        class="form-select"
                        :value="application.status"
                        :disabled="
                          updatingId === application.application_id
                        "
                        @change="
                          updateStatus(
                            application,
                            $event.target.value
                          )
                        "
                      >
                        <option value="applied">
                          Applied
                        </option>

                        <option value="shortlisted">
                          Shortlisted
                        </option>

                        <option value="interview_scheduled">
                          Interview Scheduled
                        </option>

                        <option value="selected">
                          Selected
                        </option>

                        <option value="rejected">
                          Rejected
                        </option>
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>