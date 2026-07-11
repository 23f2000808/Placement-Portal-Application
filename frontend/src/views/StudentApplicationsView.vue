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
        <h1 class="h2 mb-1">
          My Applications
        </h1>

        <p class="text-muted mb-0">
          Track your placement application history and current status
        </p>
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
          Loading applications...
        </p>
      </div>

      <template v-else>

        <div
          v-if="applications.length === 0"
          class="alert alert-secondary"
        >
          You have not applied for any placement drives yet.
        </div>

        <div
          v-else
          class="card shadow-sm"
        >
          <div class="card-body">

            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">

                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Applied On</th>
                    <th>Current Status</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="application in applications"
                    :key="application.id"
                  >
                    <td class="fw-semibold">
                      {{ application.company_name }}
                    </td>

                    <td>
                      {{ application.job_title }}
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
                      <button
                        class="btn btn-sm btn-outline-primary"
                        @click="viewDrive(application.drive_id)"
                      >
                        View Details
                      </button>
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


<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const applications = ref([])
const loading = ref(true)
const error = ref('')


const loadApplications = async () => {
  try {
    error.value = ''

    const response = await api.get(
      '/student/applications'
    )

    applications.value = response.data

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
      'Unable to load your applications'

  } finally {
    loading.value = false
  }
}


const formatDate = (dateValue) => {
  if (!dateValue) return 'Not available'

  return new Date(dateValue).toLocaleDateString(
    'en-IN',
    {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    }
  )
}


const formatStatus = (status) => {
  if (!status) return 'Unknown'

  return status
    .replaceAll('_', ' ')
    .replace(/\b\w/g, letter => letter.toUpperCase())
}


const statusClass = (status) => {

  if (status === 'selected') {
    return 'bg-success'
  }

  if (
    status === 'shortlisted' ||
    status === 'interview_scheduled'
  ) {
    return 'bg-warning text-dark'
  }

  if (status === 'rejected') {
    return 'bg-danger'
  }

  return 'bg-primary'
}


const viewDrive = (driveId) => {
  router.push(`/student/drives/${driveId}`)
}


const goToDashboard = () => {
  router.push('/student/dashboard')
}


onMounted(loadApplications)
</script>