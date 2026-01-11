<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import Card from 'primevue/card'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

// Form validation schema
const schema = yup.object({
  username: yup.string().required('Username is required'),
  password: yup.string().required('Password is required'),
})

const { defineField, handleSubmit, errors } = useForm({
  validationSchema: schema,
})

const [username] = defineField('username')
const [password] = defineField('password')

const isLoading = ref(false)

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true

  const result = await authStore.login(values.username, values.password)

  isLoading.value = false

  if (result.success) {
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: result.message,
      life: 3000,
    })
    router.push({ name: 'dashboard' })
  } else {
    toast.add({
      severity: 'error',
      summary: 'Login Failed',
      detail: result.message,
      life: 5000,
    })
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-dark-bg px-4 py-8">
    <Toast />
    
    <Card class="w-full max-w-md bg-dark-surface border border-dark-border shadow-2xl">
      <template #header>
        <div class="text-center pt-6 pb-2">
          <h1 class="text-3xl font-bold text-dark-text mb-2">Daily Helper</h1>
          <p class="text-dark-text-secondary">Sign in to your account</p>
        </div>
      </template>
      
      <template #content>
        <form @submit="onSubmit" class="space-y-6">
          <!-- Username Field -->
          <div class="flex flex-col gap-2">
            <label for="username" class="text-dark-text font-medium">Username</label>
            <InputText
              id="username"
              v-model="username"
              placeholder="Enter your username"
              :class="{ 'p-invalid': errors.username }"
              class="w-full"
              autocomplete="username"
            />
            <small v-if="errors.username" class="text-red-400">{{ errors.username }}</small>
          </div>

          <!-- Password Field -->
          <div class="flex flex-col gap-2">
            <label for="password" class="text-dark-text font-medium">Password</label>
            <Password
              id="password"
              v-model="password"
              placeholder="Enter your password"
              :class="{ 'p-invalid': errors.password }"
              :feedback="false"
              toggle-mask
              class="w-full"
              autocomplete="current-password"
            />
            <small v-if="errors.password" class="text-red-400">{{ errors.password }}</small>
          </div>

          <!-- Submit Button -->
          <Button
            type="submit"
            label="Sign In"
            :loading="isLoading"
            class="w-full"
            severity="primary"
          />
        </form>
      </template>
      
      <template #footer>
        <div class="text-center text-sm text-dark-text-secondary">
          <p>Admin access required for user management</p>
        </div>
      </template>
    </Card>
  </div>
</template>

<style scoped>
/* Additional dark mode overrides for PrimeVue components */
:deep(.p-card) {
  background: var(--p-surface-0);
  border-radius: 0.75rem;
}

:deep(.p-inputtext),
:deep(.p-password input) {
  background: #0f172a;
  border-color: #334155;
  color: #f1f5f9;
}

:deep(.p-inputtext:enabled:hover),
:deep(.p-password input:enabled:hover) {
  border-color: #475569;
}

:deep(.p-inputtext:enabled:focus),
:deep(.p-password input:enabled:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.2rem rgba(59, 130, 246, 0.2);
}

:deep(.p-button) {
  background: #3b82f6;
  border-color: #3b82f6;
  padding: 0.75rem 1rem;
  font-weight: 600;
}

:deep(.p-button:hover) {
  background: #2563eb;
  border-color: #2563eb;
}
</style>
