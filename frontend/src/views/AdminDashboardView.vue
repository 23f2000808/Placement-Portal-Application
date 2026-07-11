<template>
  <div class="min-vh-100 bg-light">

    <!-- NAVBAR -->
    <nav class="navbar navbar-dark bg-primary">
      <div class="container">
        <span class="navbar-brand fw-semibold">
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

      <!-- HEADER -->
      <div class="mb-4">
        <h1 class="h2 mb-1">
          Admin Dashboard
        </h1>

        <p class="text-muted mb-0">
          Manage companies, students, placement drives and applications
        </p>
      </div>

      <!-- SUCCESS -->
      <div
        v-if="successMessage"
        class="alert alert-success"
      >
        {{ successMessage }}
      </div>

      <!-- ERROR -->
      <div
        v-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>

      <!-- LOADING -->
      <div
        v-if="loading"
        class="text-center py-5"
      >
        <div class="spinner-border text-primary"></div>

        <p class="text-muted mt-3">
          Loading admin dashboard...
        </p>
      </div>

      <template v-else>

        <!-- SUMMARY CARDS -->
        <div class="row g-3 mb-5">

          <div class="col-md-4">
            <div class="card shadow-sm h-100">
              <div class="card-body text-center py-4">
                <h2 class="fw-bold">
                  {{ stats.students }}
                </h2>

                <p class="text-muted mb-0">
                  Registered Students
                </p>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card shadow-sm h-100">
              <div class="card-body text-center py-4">
                <h2 class="fw-bold">
                  {{ stats.companies }}
                </h2>

                <p class="text-muted mb-0">
                  Registered Companies
                </p>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card shadow-sm h-100">
              <div class="card-body text-center py-4">
                <h2 class="fw-bold">
                  {{ stats.drives }}
                </h2>

                <p class="text-muted mb-0">
                  Total Drives
                </p>
              </div>
            </div>
          </div>

        </div>


        <!-- PENDING COMPANY APPLICATIONS -->
        <section class="mb-5">

          <h3 class="mb-3">
            Pending Company Applications
          </h3>

          <div
            v-if="pendingCompanies.length === 0"
            class="alert alert-secondary"
          >
            No pending company applications.
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
                      <th>HR Contact</th>
                      <th>Website</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="company in pendingCompanies"
                      :key="company.id"
                    >
                      <td class="fw-semibold">
                        {{ company.company_name }}
                      </td>

                      <td>
                        {{ company.hr_contact }}
                      </td>

                      <td>
                        {{ company.website }}
                      </td>

                      <td>
                        <div class="d-flex gap-2">

                          <button
                            class="btn btn-sm btn-success"
                            @click="approveCompany(company.id)"
                          >
                            Approve
                          </button>

                          <button
                            class="btn btn-sm btn-outline-danger"
                            @click="rejectCompany(company.id)"
                          >
                            Reject
                          </button>

                        </div>
                      </td>
                    </tr>
                  </tbody>

                </table>
              </div>

            </div>
          </div>

        </section>


        <!-- PENDING DRIVE APPLICATIONS -->
        <section class="mb-5">

          <h3 class="mb-3">
            Pending Drive Applications
          </h3>

          <div
            v-if="pendingDrives.length === 0"
            class="alert alert-secondary"
          >
            No drives waiting for approval.
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
                      <th>Company</th>
                      <th>Deadline</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="drive in pendingDrives"
                      :key="drive.id"
                    >
                      <td class="fw-semibold">
                        {{ drive.job_title }}
                      </td>

                      <td>
                        {{ drive.company }}
                      </td>

                      <td>
                        {{ drive.deadline }}
                      </td>

                      <td>
                        <span class="badge bg-warning text-dark">
                          Pending
                        </span>
                      </td>

                      <td>
                        <div class="d-flex gap-2">

                          <button
                            class="btn btn-sm btn-success"
                            @click="approveDrive(drive.id)"
                          >
                            Approve
                          </button>

                          <button
                            class="btn btn-sm btn-outline-danger"
                            @click="rejectDrive(drive.id)"
                          >
                            Reject
                          </button>

                        </div>
                      </td>
                    </tr>
                  </tbody>

                </table>
              </div>

            </div>
          </div>

        </section>


        <!-- REGISTERED COMPANIES -->
        <section class="mb-5">

          <h3 class="mb-3">
            Registered Companies
          </h3>

          <div
            v-if="companies.length === 0"
            class="alert alert-secondary"
          >
            No registered companies.
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
                      <th>HR Contact</th>
                      <th>Website</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="company in companies"
                      :key="company.id"
                    >
                      <td class="fw-semibold">
                        {{ company.company_name }}
                      </td>

                      <td>
                        {{ company.hr_contact }}
                      </td>

                      <td>
                        {{ company.website }}
                      </td>

                      <td>
                        <span
                          class="badge"
                          :class="companyStatusClass(
                            company.approval_status
                          )"
                        >
                          {{ formatStatus(company.approval_status) }}
                        </span>
                      </td>

                      <td>
                        <button
                          v-if="company.approval_status === 'approved'"
                          class="btn btn-sm btn-outline-danger"
                          @click="blacklistCompany(company.id)"
                        >
                          Blacklist
                        </button>

                        <span
                          v-else
                          class="text-muted"
                        >
                          No action
                        </span>
                      </td>
                    </tr>
                  </tbody>

                </table>
              </div>

            </div>
          </div>

        </section>


        <!-- REGISTERED STUDENTS -->
        <section class="mb-5">

          <h3 class="mb-3">
            Registered Students
          </h3>

          <div
            v-if="students.length === 0"
            class="alert alert-secondary"
          >
            No registered students.
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
                      <th>Student</th>
                      <th>Department</th>
                      <th>CGPA</th>
                      <th>Graduation Year</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="student in students"
                      :key="student.id"
                    >
                      <td>
                        <div class="fw-semibold">
                          {{ student.name }}
                        </div>

                        <small class="text-muted">
                          {{ student.email }}
                        </small>
                      </td>

                      <td>
                        {{ student.department }}
                      </td>

                      <td>
                        {{ student.cgpa }}
                      </td>

                      <td>
                        {{ student.graduation_year }}
                      </td>

                      <td>
                        <span
                          v-if="student.active"
                          class="badge bg-success"
                        >
                          Active
                        </span>

                        <span
                          v-else
                          class="badge bg-secondary"
                        >
                          Deactivated
                        </span>
                      </td>

                      <td>
                        <button
                          v-if="student.active"
                          class="btn btn-sm btn-outline-danger"
                          @click="blacklistStudent(student.id)"
                        >
                          Blacklist
                        </button>

                        <span
                          v-else
                          class="text-muted"
                        >
                          No action
                        </span>
                      </td>
                    </tr>
                  </tbody>

                </table>
              </div>

            </div>
          </div>

        </section>


        <!-- ONGOING DRIVES -->
        <section class="mb-5">

          <h3 class="mb-3">
            Ongoing Drives
          </h3>

          <div
            v-if="ongoingDrives.length === 0"
            class="alert alert-secondary"
          >
            No ongoing drives.
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
                      <th>Company</th>
                      <th>Deadline</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="drive in ongoingDrives"
                      :key="drive.id"
                    >
                      <td class="fw-semibold">
                        {{ drive.job_title }}
                      </td>

                      <td>
                        {{ drive.company }}
                      </td>

                      <td>
                        {{ drive.deadline }}
                      </td>

                      <td>
                        <span class="badge bg-success">
                          Approved
                        </span>
                      </td>

                      <td>
                        <button
                          class="btn btn-sm btn-outline-danger"
                          @click="closeDrive(drive.id)"
                        >
                          Close Drive
                        </button>
                      </td>
                    </tr>
                  </tbody>

                </table>
              </div>

            </div>
          </div>

        </section>


        <!-- STUDENT APPLICATIONS -->
        <section>

          <h3 class="mb-3">
            Student Applications
          </h3>

          <div
            v-if="applications.length === 0"
            class="alert alert-secondary"
          >
            No student applications.
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
                      <th>Student</th>
                      <th>Drive</th>
                      <th>Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="(application, index) in applications"
                      :key="index"
                    >
                      <td>
                        {{ application.student }}
                      </td>

                      <td>
                        {{ application.drive }}
                      </td>

                      <td>
                        <span
                          class="badge"
                          :class="applicationStatusClass(
                            application.status
                          )"
                        >
                          {{ formatStatus(application.status) }}
                        </span>
                      </td>
                    </tr>
                  </tbody>

                </table>
              </div>

            </div>
          </div>

        </section>

      </template>

    </main>

  </div>
</template>


<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const loading = ref(true)
const error = ref('')
const successMessage = ref('')

const stats = reactive({
  students: 0,
  companies: 0,
  drives: 0
})

const companies = ref([])
const students = ref([])
const drives = ref([])
const applications = ref([])


const pendingCompanies = computed(() => {
  return companies.value.filter(
    company => company.approval_status === 'pending'
  )
})


const pendingDrives = computed(() => {
  return drives.value.filter(
    drive => drive.status === 'pending'
  )
})


const ongoingDrives = computed(() => {
  return drives.value.filter(
    drive => drive.status === 'approved'
  )
})


const loadDashboard = async () => {
  try {
    error.value = ''

    const [
      dashboardResponse,
      companiesResponse,
      studentsResponse,
      drivesResponse,
      applicationsResponse
    ] = await Promise.all([
      api.get('/admin/dashboard'),
      api.get('/admin/companies'),
      api.get('/admin/students'),
      api.get('/admin/drives'),
      api.get('/admin/applications')
    ])

    stats.students = dashboardResponse.data.students
    stats.companies = dashboardResponse.data.companies
    stats.drives = dashboardResponse.data.drives

    companies.value = companiesResponse.data
    students.value = studentsResponse.data
    drives.value = drivesResponse.data
    applications.value = applicationsResponse.data

  } catch (err) {

    if (err.response?.status === 401) {
      router.push('/login')
      return
    }

    if (err.response?.status === 403) {
      router.push('/login')
      return
    }

    error.value =
      err.response?.data?.error ||
      'Unable to load admin dashboard'

  } finally {
    loading.value = false
  }
}


const refreshDashboard = async (message) => {
  successMessage.value = message
  await loadDashboard()
}


const approveCompany = async (companyId) => {
  try {
    error.value = ''

    const response = await api.post(
      `/admin/approve-company/${companyId}`
    )

    await refreshDashboard(response.data.message)

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to approve company'
  }
}


const rejectCompany = async (companyId) => {

  const confirmed = window.confirm(
    'Reject this company application?'
  )

  if (!confirmed) return

  try {
    error.value = ''

    const response = await api.post(
      `/admin/reject-company/${companyId}`
    )

    await refreshDashboard(response.data.message)

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to reject company'
  }
}


const blacklistCompany = async (companyId) => {

  const confirmed = window.confirm(
    'Blacklist this company? The company will no longer be able to log in.'
  )

  if (!confirmed) return

  try {
    error.value = ''

    const response = await api.post(
      `/admin/blacklist-company/${companyId}`
    )

    await refreshDashboard(response.data.message)

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to blacklist company'
  }
}


const approveDrive = async (driveId) => {
  try {
    error.value = ''

    const response = await api.post(
      `/admin/approve-drive/${driveId}`
    )

    await refreshDashboard(response.data.message)

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to approve drive'
  }
}


const rejectDrive = async (driveId) => {

  const confirmed = window.confirm(
    'Reject this placement drive?'
  )

  if (!confirmed) return

  try {
    error.value = ''

    const response = await api.post(
      `/admin/reject-drive/${driveId}`
    )

    await refreshDashboard(response.data.message)

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to reject drive'
  }
}


const closeDrive = async (driveId) => {

  const confirmed = window.confirm(
    'Close this placement drive?'
  )

  if (!confirmed) return

  try {
    error.value = ''

    const response = await api.post(
      `/admin/close-drive/${driveId}`
    )

    await refreshDashboard(response.data.message)

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to close drive'
  }
}


const blacklistStudent = async (studentId) => {

  const confirmed = window.confirm(
    'Blacklist this student? The student will no longer be able to log in.'
  )

  if (!confirmed) return

  try {
    error.value = ''

    const response = await api.post(
      `/admin/blacklist-student/${studentId}`
    )

    await refreshDashboard(response.data.message)

  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Unable to blacklist student'
  }
}


const formatStatus = (status) => {
  if (!status) return 'Unknown'

  return status.charAt(0).toUpperCase() + status.slice(1)
}


const companyStatusClass = (status) => {
  if (status === 'approved') return 'bg-success'
  if (status === 'pending') return 'bg-warning text-dark'
  if (status === 'rejected') return 'bg-danger'

  return 'bg-secondary'
}


const applicationStatusClass = (status) => {
  if (status === 'selected') return 'bg-success'

  if (
    status === 'shortlisted' ||
    status === 'interview_scheduled'
  ) {
    return 'bg-warning text-dark'
  }

  if (status === 'rejected') return 'bg-danger'

  return 'bg-primary'
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


onMounted(loadDashboard)
</script>