<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const login = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await api.post('/login', {
      email: email.value,
      password: password.value
    })

    const role = response.data.role

    if (role === 'student') {
      router.push('/student/dashboard')
    } else if (role === 'company') {
      router.push('/company/dashboard')
    } else if (role === 'admin') {
      router.push('/admin/dashboard')
    } else {
      error.value = 'Unknown user role'
    }
  } catch (err) {
    error.value =
      err.response?.data?.error ||
      'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-vh-100 bg-light d-flex align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="text-center mb-4">
            <h2>Placement Portal</h2>
            <p class="text-muted">
              Login to continue
            </p>
          </div>

          <div class="card shadow-sm">
            <div class="card-body p-4">
              <h4 class="mb-4">Login</h4>

              <div
                v-if="error"
                class="alert alert-danger"
              >
                {{ error }}
              </div>

              <form @submit.prevent="login">
                <div class="mb-3">
                  <label
                    for="email"
                    class="form-label"
                  >
                    Email
                  </label>

                  <input
                    id="email"
                    v-model="email"
                    type="email"
                    class="form-control"
                    required
                  >
                </div>

                <div class="mb-4">
                  <label
                    for="password"
                    class="form-label"
                  >
                    Password
                  </label>

                  <input
                    id="password"
                    v-model="password"
                    type="password"
                    class="form-control"
                    required
                  >
                </div>

                <button
                  type="submit"
                  class="btn btn-primary w-100"
                  :disabled="loading"
                >
                  {{ loading ? 'Logging in...' : 'Login' }}
                </button>
              </form>
            </div>
          </div>

          <div class="text-center mt-3">
            <p>
              Don't have an account?

              <router-link to="/register">
                Register Here
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
