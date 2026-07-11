import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import StudentDashboardView from '../views/StudentDashboardView.vue'
import AvailableDrivesView from '../views/AvailableDrivesView.vue'
import DriveDetailsView from '../views/DriveDetailsView.vue'
import StudentApplicationsView from '../views/StudentApplicationsView.vue'
import CompanyDriveApplicantsView from '../views/CompanyDriveApplicantsView.vue'
import CompanyDashboardView from '../views/CompanyDashboardView.vue'
import CreateDriveView from '../views/CreateDriveView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'
import StudentProfileView from '../views/StudentProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/student/dashboard',
      name: 'student-dashboard',
      component: StudentDashboardView
    },
    {
      path: '/student/drives',
      name: 'student-drives',
      component: AvailableDrivesView
    },
    {
      path: '/student/drives/:id',
      name: 'drive-details',
      component: DriveDetailsView
    },
    {
      path: '/student/applications',
      name: 'student-applications',
      component: StudentApplicationsView
    },
    {
      path: '/company/drives/:id/applications',
      name: 'company-drive-applications',
      component: CompanyDriveApplicantsView
    },
    {
      path: '/company/dashboard',
      name: 'company-dashboard',
      component: CompanyDashboardView
    },
    {
      path: '/company/drives/create',
      name: 'create-drive',
      component: CreateDriveView
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboardView
    },
    {
      path: '/student/profile',
      name: 'student-profile',
      component: StudentProfileView
    }
  ]
})

export default router
