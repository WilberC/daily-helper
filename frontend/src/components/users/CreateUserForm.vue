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
import FormField from '@/components/common/form/FormField.vue'
import FormGroup from '@/components/common/form/FormGroup.vue'
import FormActions from '@/components/common/form/FormActions.vue'
import InfoBox from '@/components/common/feedback/InfoBox.vue'
import Label from '@/components/common/typography/Label.vue'

interface Props {
  userType: 'admin' | 'staff' | 'normal'
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
    <FormGroup layout="grid">
      <!-- Username Field -->
      <FormField label="Username" for="username" :error="errors.username" required>
        <InputText
          id="username"
          v-model="username"
          placeholder="Enter username"
          :class="{ 'p-invalid': errors.username }"
          class="w-full"
          autocomplete="off"
        />
      </FormField>

      <!-- Email Field -->
      <FormField label="Email" for="email" :error="errors.email" required>
        <InputText
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter email"
          :class="{ 'p-invalid': errors.email }"
          class="w-full"
          autocomplete="off"
        />
      </FormField>

      <!-- First Name Field -->
      <FormField label="First Name" for="firstName">
        <InputText
          id="firstName"
          v-model="firstName"
          placeholder="Enter first name"
          class="w-full"
          autocomplete="off"
        />
      </FormField>

      <!-- Last Name Field -->
      <FormField label="Last Name" for="lastName">
        <InputText
          id="lastName"
          v-model="lastName"
          placeholder="Enter last name"
          class="w-full"
          autocomplete="off"
        />
      </FormField>
    </FormGroup>

    <!-- Password Field -->
    <FormField label="Password" for="password" :error="errors.password" required>
      <Password
        id="password"
        v-model="password"
        placeholder="Enter password"
        :class="{ 'p-invalid': errors.password }"
        toggle-mask
        input-class="w-full"
        autocomplete="new-password"
      />
    </FormField>

    <!-- Active Checkbox -->
    <div class="flex items-center gap-2">
      <Checkbox id="isActive" v-model="isActive" :binary="true" />
      <Label for="isActive" class="cursor-pointer"> Active Account </Label>
    </div>

    <!-- Role Info -->
    <InfoBox variant="info">
      <template #default="{ titleColor, textColor }">
        <p :class="[titleColor, 'font-medium mb-1']">
          {{
            userType === 'admin'
              ? 'Administrator Account'
              : userType === 'staff'
                ? 'Staff Account'
                : 'Normal User Account'
          }}
        </p>
        <p :class="[textColor, 'text-sm']">
          {{
            userType === 'admin'
              ? 'This user will have full access to all features including user management.'
              : userType === 'staff'
                ? 'This user will have elevated privileges but no user management capabilities.'
                : 'This user will have standard access without administrative capabilities.'
          }}
        </p>
      </template>
    </InfoBox>

    <!-- Submit Button -->
    <FormActions>
      <Button
        type="submit"
        :label="`Create ${
          userType === 'admin' ? 'Admin' : userType === 'staff' ? 'Staff' : 'Normal'
        } User`"
        :loading="isLoading"
        severity="primary"
        icon="pi pi-user-plus"
      />
    </FormActions>
  </form>
</template>
