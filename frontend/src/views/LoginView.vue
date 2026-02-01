<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '@/stores/auth'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import { NInput, NButton, NCard, NIcon } from 'naive-ui'
import { LogIn } from '@vicons/ionicons5'
import PageHeading from '@/components/common/typography/PageHeading.vue'
import BodyText from '@/components/common/typography/BodyText.vue'
import FormField from '@/components/common/form/FormField.vue'

const router = useRouter()
const message = useMessage()
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
    message.success(result.message, { duration: 3000 })
    router.push({ name: 'dashboard' })
  } else {
    message.error(result.message, { duration: 5000 })
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4 py-8">
    <n-card class="w-full max-w-md shadow-2xl">
      <template #header>
        <div class="text-center pt-6 pb-2">
          <PageHeading as="h1" size="xl">Daily Helper</PageHeading>
          <BodyText size="sm" class="mt-2">Sign in to your account</BodyText>
        </div>
      </template>

      <template #default>
        <form @submit.prevent="onSubmit" class="space-y-6">
          <!-- Username Field -->
          <FormField label="Username" for="username" :error="errors.username">
            <n-input
              id="username"
              v-model:value="username"
              placeholder="Enter your username"
              :status="errors.username ? 'error' : undefined"
              autocomplete="username"
            />
          </FormField>

          <!-- Password Field -->
          <FormField label="Password" for="password" :error="errors.password">
            <n-input
              id="password"
              v-model:value="password"
              type="password"
              placeholder="Enter your password"
              :status="errors.password ? 'error' : undefined"
              show-password-on="click"
              autocomplete="current-password"
            />
          </FormField>

          <!-- Submit Button -->
          <n-button attr-type="submit" type="primary" :loading="isLoading" block size="large">
            <template #icon>
              <n-icon><LogIn /></n-icon>
            </template>
            Sign In
          </n-button>
        </form>
      </template>

      <template #footer>
        <div class="text-center text-sm text-gray-500 dark:text-gray-400">
          <p>Admin access required for user management</p>
        </div>
      </template>
    </n-card>
  </div>
</template>
