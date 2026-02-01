<script setup lang="ts">
import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '@/stores/auth'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import type { RegisterInput } from '@/types/user'
import { NInput, NCheckbox, NButton, NIcon } from 'naive-ui'
import { PersonAdd } from '@vicons/ionicons5'
import FormField from '@/components/common/form/FormField.vue'
import FormGroup from '@/components/common/form/FormGroup.vue'
import FormActions from '@/components/common/form/FormActions.vue'
import InfoBox from '@/components/common/feedback/InfoBox.vue'
import Label from '@/components/common/typography/Label.vue'

interface Props {
  userType: 'admin' | 'staff' | 'normal'
}

const props = defineProps<Props>()

const message = useMessage()
const authStore = useAuthStore()

// Form validation schema
const schema = yup.object({
  username: yup
    .string()
    .required('Username is required')
    .min(3, 'Username must be at least 3 characters'),
  email: yup.string().required('Email is required').email('Must be a valid email'),
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
const showPassword = ref(false)

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true

  const input: RegisterInput = {
    username: values.username,
    email: values.email,
    password: values.password,
    firstName: values.firstName || undefined,
    lastName: values.lastName || undefined,
    isSuperuser: props.userType === 'admin',
    isStaff: props.userType === 'admin' || props.userType === 'staff',
    isActive: values.isActive,
  }

  const result = await authStore.register(input)

  isLoading.value = false

  if (result.success) {
    message.success(result.message, { duration: 5000 })
    resetForm()
  } else {
    message.error(result.message, { duration: 5000 })
  }
})
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-6 max-w-2xl">
    <FormGroup layout="grid">
      <!-- Username Field -->
      <FormField label="Username" for="username" :error="errors.username" required>
        <n-input
          id="username"
          v-model:value="username"
          placeholder="Enter username"
          :status="errors.username ? 'error' : undefined"
          autocomplete="off"
        />
      </FormField>

      <!-- Email Field -->
      <FormField label="Email" for="email" :error="errors.email" required>
        <n-input
          id="email"
          v-model:value="email"
          placeholder="Enter email"
          :status="errors.email ? 'error' : undefined"
          autocomplete="email"
        />
      </FormField>

      <!-- First Name Field -->
      <FormField label="First Name" for="firstName">
        <n-input
          id="firstName"
          v-model:value="firstName"
          placeholder="Enter first name"
          autocomplete="off"
        />
      </FormField>

      <!-- Last Name Field -->
      <FormField label="Last Name" for="lastName">
        <n-input
          id="lastName"
          v-model:value="lastName"
          placeholder="Enter last name"
          autocomplete="off"
        />
      </FormField>
    </FormGroup>

    <!-- Password Field -->
    <FormField label="Password" for="password" :error="errors.password" required>
      <n-input
        id="password"
        v-model:value="password"
        :type="showPassword ? 'text' : 'password'"
        placeholder="Enter password"
        :status="errors.password ? 'error' : undefined"
        show-password-on="click"
        autocomplete="new-password"
      />
    </FormField>

    <!-- Active Checkbox -->
    <div class="flex items-center gap-2">
      <n-checkbox id="isActive" v-model:checked="isActive" />
      <Label for="isActive" class="cursor-pointer">Active Account</Label>
    </div>

    <!-- Role Info -->
    <InfoBox variant="info">
      <p class="font-medium mb-1">
        {{
          userType === 'admin'
            ? 'Administrator Account'
            : userType === 'staff'
              ? 'Staff Account'
              : 'Normal User Account'
        }}
      </p>
      <p class="text-sm opacity-90">
        {{
          userType === 'admin'
            ? 'This user will have full access to all features including user management.'
            : userType === 'staff'
              ? 'This user will have elevated privileges but no user management capabilities.'
              : 'This user will have standard access without administrative capabilities.'
        }}
      </p>
    </InfoBox>

    <!-- Submit Button -->
    <FormActions>
      <n-button type="primary" attr-type="submit" :loading="isLoading" size="large">
        <template #icon>
          <n-icon><PersonAdd /></n-icon>
        </template>
        Create {{ userType === 'admin' ? 'Admin' : userType === 'staff' ? 'Staff' : 'Normal' }} User
      </n-button>
    </FormActions>
  </form>
</template>
