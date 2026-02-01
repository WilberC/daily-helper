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
import { useTranslation } from '@/composables/useTranslation'

interface Props {
  userType: 'admin' | 'staff' | 'normal'
}

const props = defineProps<Props>()

const message = useMessage()
const authStore = useAuthStore()
const { t } = useTranslation()

// Form validation schema
const schema = yup.object({
  username: yup
    .string()
    .required(t('validation.username.required'))
    .min(3, t('validation.minLength', { field: t('users.form.username'), min: 3 })),
  email: yup.string().required(t('validation.email.required')).email(t('validation.email.invalid')),
  password: yup
    .string()
    .required(t('validation.password.required'))
    .min(8, t('validation.password.minLength', { min: 8 })),
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
      <FormField :label="t('users.form.username')" for="username" :error="errors.username" required>
        <n-input
          id="username"
          v-model:value="username"
          :placeholder="t('users.form.enterUsername')"
          :status="errors.username ? 'error' : undefined"
          autocomplete="off"
        />
      </FormField>

      <!-- Email Field -->
      <FormField :label="t('users.form.email')" for="email" :error="errors.email" required>
        <n-input
          id="email"
          v-model:value="email"
          :placeholder="t('users.form.enterEmail')"
          :status="errors.email ? 'error' : undefined"
          autocomplete="email"
        />
      </FormField>

      <!-- First Name Field -->
      <FormField :label="t('users.form.firstName')" for="firstName">
        <n-input
          id="firstName"
          v-model:value="firstName"
          :placeholder="t('users.form.enterFirstName')"
          autocomplete="off"
        />
      </FormField>

      <!-- Last Name Field -->
      <FormField :label="t('users.form.lastName')" for="lastName">
        <n-input
          id="lastName"
          v-model:value="lastName"
          :placeholder="t('users.form.enterLastName')"
          autocomplete="off"
        />
      </FormField>
    </FormGroup>

    <!-- Password Field -->
    <FormField :label="t('users.form.password')" for="password" :error="errors.password" required>
      <n-input
        id="password"
        v-model:value="password"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="t('users.form.enterPassword')"
        :status="errors.password ? 'error' : undefined"
        show-password-on="click"
        autocomplete="new-password"
      />
    </FormField>

    <!-- Active Checkbox -->
    <div class="flex items-center gap-2">
      <n-checkbox id="isActive" v-model:checked="isActive" />
      <Label for="isActive" class="cursor-pointer">{{ t('users.form.isActive') }}</Label>
    </div>

    <!-- Role Info -->
    <InfoBox variant="info">
      <p class="font-medium mb-1">
        {{
          userType === 'admin'
            ? t('users.info.adminAccount')
            : userType === 'staff'
              ? t('users.info.staffAccount')
              : t('users.info.normalAccount')
        }}
      </p>
      <p class="text-sm opacity-90">
        {{
          userType === 'admin'
            ? t('users.info.adminDescription')
            : userType === 'staff'
              ? t('users.info.staffDescription')
              : t('users.info.normalDescription')
        }}
      </p>
    </InfoBox>

    <!-- Submit Button -->
    <FormActions>
      <n-button type="primary" attr-type="submit" :loading="isLoading" size="large">
        <template #icon>
          <n-icon><PersonAdd /></n-icon>
        </template>
        {{
          t('users.form.create', {
            type:
              userType === 'admin'
                ? t('users.types.admin')
                : userType === 'staff'
                  ? t('users.types.staff')
                  : t('users.types.normal'),
          })
        }}
      </n-button>
    </FormActions>
  </form>
</template>
