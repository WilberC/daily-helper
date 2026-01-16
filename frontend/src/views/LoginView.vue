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
import PageHeading from '@/components/common/typography/PageHeading.vue'
import BodyText from '@/components/common/typography/BodyText.vue'
import FormField from '@/components/common/form/FormField.vue'

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
  <div class="min-h-screen flex items-center justify-center bg-surface-50 dark:bg-dark-bg px-4 py-8">
    <Toast />

    <Card class="w-full max-w-md shadow-2xl">
      <template #header>
        <div class="text-center pt-6 pb-2">
          <PageHeading as="h1" size="xl">Daily Helper</PageHeading>
          <BodyText size="sm" class="mt-2">Sign in to your account</BodyText>
        </div>
      </template>

      <template #content>
        <form @submit="onSubmit" class="space-y-6">
          <!-- Username Field -->
          <FormField label="Username" for="username" :error="errors.username">
            <InputText
              id="username"
              v-model="username"
              placeholder="Enter your username"
              :class="{ 'p-invalid': errors.username }"
              class="w-full"
              autocomplete="username"
            />
          </FormField>

          <!-- Password Field -->
          <FormField label="Password" for="password" :error="errors.password">
            <Password
              id="password"
              v-model="password"
              placeholder="Enter your password"
              :class="{ 'p-invalid': errors.password }"
              :feedback="false"
              toggle-mask
              input-class="w-full"
              autocomplete="current-password"
            />
          </FormField>

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

