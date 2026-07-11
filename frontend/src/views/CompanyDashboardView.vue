<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const company = ref(null)
const upcomingDrives = ref([])
const closedDrives = ref([])
const totalDrives = ref(0)

const loading = ref(true)
const error = ref('')
const completingId = ref(null)
const successMessage = ref('')

const loadDashboard = async () => {
  try {
    loading.value = true
    error.value = ''

    const response = await api.get('/company/dashboard')

    company.value = response.data.company
    upcomingDrives.value = response.data.upcoming_drives
    closedDrives.value = response.data.closed_drives
    totalDrives.value = response.data.total_drives
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to load company dashboard'
  } finally {
    loading.value = false
  }
}

const viewApplicants = (driveId) => {
  router.push(`/company/drives/${driveId}/applications`)
}

const exportCSV = async (driveId) => {

  try {

    const response = await api.get(
      `/company/drives/${driveId}/export`,
      {
        responseType: 'blob'
      }
    )

    const blob = new Blob(
      [response.data],
      {
        type: 'text/csv'
      }
    )

    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')

    link.href = url

    link.download =
      `drive_${driveId}_applications.csv`

    document.body.appendChild(link)

    link.click()

    document.body.removeChild(link)

    window.URL.revokeObjectURL(url)

  }

  catch (err) {

    alert(
      err.response?.data?.error ||
      'Unable to export CSV.'
    )

  }

}

const markAsComplete = async (driveId) => {
  const confirmed = window.confirm(
    'Mark this drive as complete? It will move to Closed Drives.'
  )

  if (!confirmed) {
    return
  }

  try {
    completingId.value = driveId
    error.value = ''
    successMessage.value = ''

    const response = await api.put(
      `/company/drives/${driveId}/complete`
    )

    successMessage.value = response.data.message

    await loadDashboard()
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to mark drive as complete'
  } finally {
    completingId.value = null
  }
}

const createDrive = () => {
  router.push('/company/drives/create')
}

const logout = async () => {
  try {
    await api.post('/logout')
  } catch (err) {
    console.error(err)
  } finally {
    router.push('/login')
  }
}

const formatStatus = (status) => {
  if (!status) return 'Unknown'

  return status
    .replaceAll('_', ' ')
    .replace(/\b\w/g, letter => letter.toUpperCase())
}

const statusClass = (status) => {
  const classes = {
    pending: 'bg-warning text-dark',
    approved: 'bg-success',
    rejected: 'bg-danger',
    closed: 'bg-secondary'
  }

  return classes[status] || 'bg-secondary'
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
          type="button"
          class="btn btn-outline-light"
          @click="logout"
        >
          Logout
        </button>
      </div>
    </nav>

    <main class="container py-5">

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

      <template v-else-if="company">

        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h2>{{ company.company_name }} Dashboard</h2>
            <p class="text-muted mb-0">
              Manage placement drives and student applications
            </p>
          </div>

          <button
            type="button"
            class="btn btn-primary"
            @click="createDrive"
          >
            Create Drive
          </button>
        </div>

        <div class="card shadow-sm mb-4">
          <div class="card-body">
            <h4 class="mb-4">Company Profile</h4>

            <div class="row g-4">

              <div class="col-md-6">
                <div class="text-muted">Email</div>
                <div class="fw-semibold">
                  {{ company.email }}
                </div>
              </div>

              <div class="col-md-6">
                <div class="text-muted">HR Contact</div>
                <div class="fw-semibold">
                  {{ company.hr_contact }}
                </div>
              </div>

              <div class="col-md-6">
                <div class="text-muted">Website</div>
                <div class="fw-semibold">
                  {{ company.website }}
                </div>
              </div>

              <div class="col-md-6">
                <div class="text-muted">Approval Status</div>

                <span
                  class="badge"
                  :class="statusClass(company.approval_status)"
                >
                  {{ formatStatus(company.approval_status) }}
                </span>
              </div>

            </div>
          </div>
        </div>

        <div
          v-if="successMessage"
          class="alert alert-success"
        >
          {{ successMessage }}
        </div>

        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h3 class="mb-1">Upcoming Drives</h3>
            <p class="text-muted mb-0">
              Total Drives: {{ totalDrives }}
            </p>
          </div>
        </div>

        <div
          v-if="upcomingDrives.length === 0"
          class="alert alert-secondary"
        >
          You do not have any upcoming placement drives.
        </div>

        <div
          v-else
          class="card shadow-sm mb-4"
        >
          <div class="card-body">

            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">

                <thead>
                  <tr>
                    <th>Job Title</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Applications</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="drive in upcomingDrives"
                    :key="drive.id"
                  >
                    <td class="fw-semibold">
                      {{ drive.job_title }}
                    </td>

                    <td>
                      {{ drive.deadline || 'N/A' }}
                    </td>

                    <td>
                      <span
                        class="badge"
                        :class="statusClass(drive.status)"
                      >
                        {{ formatStatus(drive.status) }}
                      </span>
                    </td>

                    <td>
                      {{ drive.total_applications }}
                    </td>

                    <td>
                      <div
                        v-if="drive.status === 'approved'"
                        class="d-flex flex-wrap gap-2"
                      >
                        <button
                          type="button"
                          class="btn btn-outline-primary btn-sm me-2"
                          @click="viewApplicants(drive.id)"
                        >
                          View Applicants
                        </button>

                        <button
                          type="button"
                          class="btn btn-success btn-sm"
                          @click="exportCSV(drive.id)"
                        >
                          Export CSV
                        </button>

                        <button
                          type="button"
                          class="btn btn-sm btn-success"
                          :disabled="completingId === drive.id"
                          @click="markAsComplete(drive.id)"
                        >
                          {{
                            completingId === drive.id
                              ? 'Completing...'
                              : 'Mark as Complete'
                          }}
                        </button>
                      </div>

                      <span
                        v-else-if="drive.status === 'pending'"
                        class="text-muted"
                      >
                        Waiting for Admin Approval
                      </span>
                    </td>
                  </tr>
                </tbody>

              </table>
            </div>

          </div>
        </div>

        <div class="mt-5">

          <h3 class="mb-3">
            Closed Drives
          </h3>

          <div
            v-if="closedDrives.length === 0"
            class="alert alert-secondary"
          >
            No closed drives yet.
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
                      <th>Job Title</th>
                      <th>Deadline</th>
                      <th>Applications</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="drive in closedDrives"
                      :key="drive.id"
                    >
                      <td class="fw-semibold">
                        {{ drive.job_title }}
                      </td>

                      <td>
                        {{ drive.deadline || 'N/A' }}
                      </td>

                      <td>
                        {{ drive.total_applications }}
                      </td>

                      <td>
                        <span class="badge bg-secondary">
                          Closed
                        </span>
                      </td>

                      <td>
                        <div class="d-flex flex-wrap gap-2">
                          <button
                            type="button"
                            class="btn btn-outline-primary btn-sm me-2"
                            @click="viewApplicants(drive.id)"
                          >
                            View Applicants
                          </button>

                          <button
                            type="button"
                            class="btn btn-success btn-sm"
                            @click="exportCSV(drive.id)"
                          >
                            Export CSV
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>

                </table>
              </div>

            </div>
          </div>

        </div>

      </template>

    </main>
  </div>
</template>
