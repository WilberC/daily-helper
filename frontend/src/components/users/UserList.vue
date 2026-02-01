/** * Displays a list of users in a data table with edit capabilities. * Allows administrators to
view and update user information. * @component */
<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '@/stores/auth'
import type { User, UpdateUserInput } from '@/types/user'
import { formatDate } from '@/composables/useFormatters'
import {
  NDataTable,
  NButton,
  NModal,
  NInput,
  NCheckbox,
  NIcon,
  type DataTableColumns,
} from 'naive-ui'
import { Person, Pencil, Refresh } from '@vicons/ionicons5'
import SectionHeading from '@/components/common/typography/SectionHeading.vue'
import SubHeading from '@/components/common/typography/SubHeading.vue'
import FormField from '@/components/common/form/FormField.vue'
import InfoBox from '@/components/common/feedback/InfoBox.vue'
import Badge from '@/components/common/utils/Badge.vue'
import { useTranslation } from '@/composables/useTranslation'

const message = useMessage()
const authStore = useAuthStore()
const { t } = useTranslation()

const users = ref<User[]>([])
const loading = ref(false)
const editDialogVisible = ref(false)
const editingUser = ref<User | null>(null)
const editForm = ref({
  email: '',
  firstName: '',
  lastName: '',
  isStaff: false,
  isActive: true,
})

const loadUsers = async () => {
  loading.value = true
  users.value = await authStore.fetchAllUsers()
  loading.value = false
}

const openEditDialog = (user: User) => {
  editingUser.value = user
  editForm.value = {
    email: user.email,
    firstName: user.firstName,
    lastName: user.lastName,
    isStaff: user.isStaff,
    isActive: user.isActive,
  }
  editDialogVisible.value = true
}

const closeEditDialog = () => {
  editDialogVisible.value = false
  editingUser.value = null
}

const saveUser = async () => {
  if (!editingUser.value) return

  const input: UpdateUserInput = {
    userId: editingUser.value.id,
    email: editForm.value.email,
    firstName: editForm.value.firstName,
    lastName: editForm.value.lastName,
    isStaff: editForm.value.isStaff,
    isActive: editForm.value.isActive,
  }

  const result = await authStore.updateUser(input)

  if (result.success) {
    message.success(t('users.form.updateSuccess'), { duration: 5000 })
    closeEditDialog()
    await loadUsers()
  } else {
    message.error(t('users.form.updateError'), { duration: 5000 })
  }
}

// Define table columns
const columns: DataTableColumns<User> = [
  {
    title: () => t('users.table.username'),
    key: 'username',
    sorter: true,
    render: (row) => {
      return h('div', { class: 'flex items-center gap-2' }, [
        h(NIcon, { component: Person, color: '#18a058', size: 18 }),
        h('span', { class: 'font-medium' }, row.username),
      ])
    },
  },
  {
    title: () => t('users.table.email'),
    key: 'email',
    sorter: true,
  },
  {
    title: () => t('users.table.firstName'),
    key: 'firstName',
    sorter: true,
  },
  {
    title: () => t('users.table.lastName'),
    key: 'lastName',
    sorter: true,
  },
  {
    title: () => t('users.table.role'),
    key: 'isStaff',
    sorter: (row1, row2) => Number(row1.isStaff) - Number(row2.isStaff),
    render: (row) => {
      return h(Badge, { variant: row.isStaff ? 'admin' : 'staff' })
    },
  },
  {
    title: () => t('users.table.status'),
    key: 'isActive',
    sorter: (row1, row2) => Number(row1.isActive) - Number(row2.isActive),
    render: (row) => {
      return h(Badge, { variant: row.isActive ? 'active' : 'inactive' })
    },
  },
  {
    title: () => t('users.table.joined'),
    key: 'dateJoined',
    sorter: (row1, row2) =>
      new Date(row1.dateJoined).getTime() - new Date(row2.dateJoined).getTime(),
    render: (row) => formatDate(row.dateJoined),
  },
  {
    title: () => t('users.table.actions'),
    key: 'actions',
    render: (row) => {
      return h(
        NButton,
        {
          text: true,
          circle: true,
          disabled: row.isStaff,
          onClick: () => openEditDialog(row),
          title: row.isStaff
            ? t('users.actions.cannotEditAdmin')
            : t('users.actions.editUser', { username: row.username }),
        },
        {
          icon: () => h(NIcon, { component: Pencil }),
        },
      )
    },
  },
]

const paginationProps = {
  pageSize: 10,
  pageSizes: [5, 10, 20, 50],
  showSizePicker: true,
}

onMounted(() => {
  loadUsers()
})
</script>

<template>
  <div class="user-list-container">
    <div class="flex justify-between items-center mb-6">
      <SectionHeading variant="primary">{{ t('users.allUsers') }}</SectionHeading>
      <n-button secondary @click="loadUsers" :loading="loading">
        <template #icon>
          <n-icon><Refresh /></n-icon>
        </template>
        {{ t('users.actions.refresh') }}
      </n-button>
    </div>

    <n-data-table
      :columns="columns"
      :data="users"
      :loading="loading"
      :pagination="paginationProps"
      striped
      :bordered="false"
      class="user-table"
    />

    <!-- Edit User Modal -->
    <n-modal
      v-model:show="editDialogVisible"
      preset="card"
      :title="t('users.modal.editTitle', { username: editingUser?.username || '' })"
      :style="{ width: '500px' }"
      :closable="true"
    >
      <div class="space-y-4 py-4">
        <!-- Email -->
        <FormField :label="t('users.form.email')" for="edit-email" required>
          <n-input
            id="edit-email"
            v-model:value="editForm.email"
            :placeholder="t('users.form.enterEmail')"
          />
        </FormField>

        <!-- First Name -->
        <FormField :label="t('users.form.firstName')" for="edit-firstName">
          <n-input
            id="edit-firstName"
            v-model:value="editForm.firstName"
            :placeholder="t('users.form.enterFirstName')"
          />
        </FormField>

        <!-- Last Name -->
        <FormField :label="t('users.form.lastName')" for="edit-lastName">
          <n-input
            id="edit-lastName"
            v-model:value="editForm.lastName"
            :placeholder="t('users.form.enterLastName')"
          />
        </FormField>

        <!-- Permissions Section -->
        <div
          class="bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 space-y-3"
        >
          <SubHeading>{{ t('users.modal.permissions') }}</SubHeading>

          <!-- Staff Permission -->
          <div class="flex items-center gap-2">
            <n-checkbox
              id="edit-isStaff"
              v-model:checked="editForm.isStaff"
              :disabled="editingUser?.isStaff"
            />
            <label for="edit-isStaff" class="text-gray-700 dark:text-gray-300 cursor-pointer">
              {{ t('users.modal.adminAccess') }}
            </label>
          </div>

          <!-- Active Status -->
          <div class="flex items-center gap-2">
            <n-checkbox id="edit-isActive" v-model:checked="editForm.isActive" />
            <label for="edit-isActive" class="text-gray-700 dark:text-gray-300 cursor-pointer">
              {{ t('users.modal.activeAccount') }}
            </label>
          </div>

          <InfoBox v-if="editingUser?.isStaff" variant="warning">
            <p>{{ t('users.modal.adminWarning') }}</p>
          </InfoBox>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <n-button @click="closeEditDialog" secondary>{{ t('users.modal.cancel') }}</n-button>
          <n-button type="primary" @click="saveUser">{{ t('users.modal.saveChanges') }}</n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>
