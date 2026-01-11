<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import type { RegisterInput } from '@/types/user'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'

interface Props {
  isAdmin: boolean
}

const props = defineProps<Props>()

const toast = useToast()
const authStore = useAuthStore()

// Form validation schema
const schema = yup.object({
  username: yup
    .string()
    .required('Username is required')
    .min(3, 'Username must be at least 3 characters'),
  email: yup
    .string()
    .required('Email is required')
    .email('Must be a valid email'),
  password: yup
    .string()
    .required('Password is required')
    .min(8, 'Password must be at least 8 characters'),
  firstName: yup.string(),
  lastName: yup.string(),
  isActive: yup.boolean(),
})

const { defineField, handleSubmit, errors, resetForm } = useForm({
  validationSchema: schema,
  initialValues: {
    username: '',
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    isActive: true,
  },
})

const [username] = defineField('username')
const [email] = defineField('email')
const [password] = defineField('password')
const [firstName] = defineField('firstName')
const [lastName] = defineField('lastName')
const [isActive] = defineField('isActive')

const isLoading = ref(false)

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true

  const input: RegisterInput = {
    username: values.username,
    email: values.email,
    password: values.password,
    firstName: values.firstName || undefined,
    lastName: values.lastName || undefined,
    isStaff: props.isAdmin, // Set based on which tab/form is active
    isActive: values.isActive,
  }

  const result = await authStore.register(input)

  isLoading.value = false

  if (result.success) {
    toast.add({
      severity: 'success',
      summary: 'User Created',
      detail: result.message,
      life: 5000,
    })
    resetForm()
  } else {
    toast.add({
      severity: 'error',
      summary: 'Creation Failed',
      detail: result.message,
      life: 5000,
    })
  }
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-6 max-w-2xl">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Username Field -->
      <div class="flex flex-col gap-2">
        <label for="username" class="text-dark-text font-medium">
          Username <span class="text-red-400">*</span>
        </label>
        <InputText
          id="username"
          v-model="username"
          placeholder="Enter username"
          :class="{ 'p-invalid': errors.username }"
          class="w-full"
          autocomplete="off"
        />
        <small v-if="errors.username" class="text-red-400">{{ errors.username }}</small>
      </div>

      <!-- Email Field -->
      <div class="flex flex-col gap-2">
        <label for="email" class="text-dark-text font-medium">
          Email <span class="text-red-400">*</span>
        </label>
        <InputText
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter email"
          :class="{ 'p-invalid': errors.email }"
          class="w-full"
          autocomplete="off"
        />
        <small v-if="errors.email" class="text-red-400">{{ errors.email }}</small>
      </div>

      <!-- First Name Field -->
      <div class="flex flex-col gap-2">
        <label for="firstName" class="text-dark-text font-medium">First Name</label>
        <InputText
          id="firstName"
          v-model="firstName"
          placeholder="Enter first name"
          class="w-full"
          autocomplete="off"
        />
      </div>

      <!-- Last Name Field -->
      <div class="flex flex-col gap-2">
        <label for="lastName" class="text-dark-text font-medium">Last Name</label>
        <InputText
          id="lastName"
          v-model="lastName"
          placeholder="Enter last name"
          class="w-full"
          autocomplete="off"
        />
      </div>
    </div>

    <!-- Password Field -->
    <div class="flex flex-col gap-2">
      <label for="password" class="text-dark-text font-medium">
        Password <span class="text-red-400">*</span>
      </label>
      <Password
        id="password"
        v-model="password"
        placeholder="Enter password"
        :class="{ 'p-invalid': errors.password }"
        toggle-mask
        class="w-full"
        autocomplete="new-password"
      />
      <small v-if="errors.password" class="text-red-400">{{ errors.password }}</small>
    </div>

    <!-- Active Checkbox -->
    <div class="flex items-center gap-2">
      <Checkbox
        id="isActive"
        v-model="isActive"
        :binary="true"
      />
      <label for="isActive" class="text-dark-text font-medium cursor-pointer">
        Active Account
      </label>
    </div>

    <!-- Role Info -->
    <div class="bg-blue-950 border border-blue-800 rounded-lg p-4">
      <div class="flex items-start gap-3">
        <i class="pi pi-info-circle text-blue-400 mt-1"></i>
        <div>
          <p class="text-blue-200 font-medium mb-1">
            {{ isAdmin ? 'Administrator Account' : 'Staff Account' }}
          </p>
          <p class="text-blue-300 text-sm">
            {{ isAdmin 
              ? 'This user will have full access to all features including user management.' 
              : 'This user will have limited access without user management capabilities.' 
            }}
          </p>
        </div>
      </div>
    </div>

    <!-- Submit Button -->
    <div class="flex gap-4">
      <Button
        type="submit"
        :label="`Create ${isAdmin ? 'Admin' : 'Staff'} User`"
        :loading="isLoading"
        severity="primary"
        icon="pi pi-user-plus"
      />
    </div>
  </form>
</template>

<style scoped>
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

:deep(.p-checkbox) {
  border-color: #334155;
}

:deep(.p-checkbox:hover) {
  border-color: #475569;
}

:deep(.p-checkbox.p-highlight) {
  background: #3b82f6;
  border-color: #3b82f6;
}

:deep(.p-button) {
  background: #3b82f6;
  border-color: #3b82f6;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}

:deep(.p-button:hover) {
  background: #2563eb;
  border-color: #2563eb;
}
</style>
