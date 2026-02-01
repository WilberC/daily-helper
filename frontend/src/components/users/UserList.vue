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

const message = useMessage()
const authStore = useAuthStore()

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
    message.success(result.message, { duration: 5000 })
    closeEditDialog()
    await loadUsers()
  } else {
    message.error(result.message, { duration: 5000 })
  }
}

// Define table columns
const columns: DataTableColumns<User> = [
  {
    title: 'Username',
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
    title: 'Email',
    key: 'email',
    sorter: true,
  },
  {
    title: 'First Name',
    key: 'firstName',
    sorter: true,
  },
  {
    title: 'Last Name',
    key: 'lastName',
    sorter: true,
  },
  {
    title: 'Role',
    key: 'isStaff',
    sorter: (row1, row2) => Number(row1.isStaff) - Number(row2.isStaff),
    render: (row) => {
      return h(Badge, { variant: row.isStaff ? 'admin' : 'staff' })
    },
  },
  {
    title: 'Status',
    key: 'isActive',
    sorter: (row1, row2) => Number(row1.isActive) - Number(row2.isActive),
    render: (row) => {
      return h(Badge, { variant: row.isActive ? 'active' : 'inactive' })
    },
  },
  {
    title: 'Joined',
    key: 'dateJoined',
    sorter: (row1, row2) =>
      new Date(row1.dateJoined).getTime() - new Date(row2.dateJoined).getTime(),
    render: (row) => formatDate(row.dateJoined),
  },
  {
    title: 'Actions',
    key: 'actions',
    render: (row) => {
      return h(
        NButton,
        {
          text: true,
          circle: true,
          disabled: row.isStaff,
          onClick: () => openEditDialog(row),
          title: row.isStaff ? 'Cannot edit admin users' : `Edit user ${row.username}`,
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
      <SectionHeading variant="primary">All Users</SectionHeading>
      <n-button secondary @click="loadUsers" :loading="loading">
        <template #icon>
          <n-icon><Refresh /></n-icon>
        </template>
        Refresh
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
      :title="`Edit User: ${editingUser?.username}`"
      :style="{ width: '500px' }"
      :closable="true"
    >
      <div class="space-y-4 py-4">
        <!-- Email -->
        <FormField label="Email" for="edit-email" required>
          <n-input id="edit-email" v-model:value="editForm.email" placeholder="Enter email" />
        </FormField>

        <!-- First Name -->
        <FormField label="First Name" for="edit-firstName">
          <n-input
            id="edit-firstName"
            v-model:value="editForm.firstName"
            placeholder="Enter first name"
          />
        </FormField>

        <!-- Last Name -->
        <FormField label="Last Name" for="edit-lastName">
          <n-input
            id="edit-lastName"
            v-model:value="editForm.lastName"
            placeholder="Enter last name"
          />
        </FormField>

        <!-- Permissions Section -->
        <div
          class="bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 space-y-3"
        >
          <SubHeading>Permissions</SubHeading>

          <!-- Staff Permission -->
          <div class="flex items-center gap-2">
            <n-checkbox
              id="edit-isStaff"
              v-model:checked="editForm.isStaff"
              :disabled="editingUser?.isStaff"
            />
            <label for="edit-isStaff" class="text-gray-700 dark:text-gray-300 cursor-pointer">
              Admin Access
            </label>
          </div>

          <!-- Active Status -->
          <div class="flex items-center gap-2">
            <n-checkbox id="edit-isActive" v-model:checked="editForm.isActive" />
            <label for="edit-isActive" class="text-gray-700 dark:text-gray-300 cursor-pointer">
              Active Account
            </label>
          </div>

          <InfoBox v-if="editingUser?.isStaff" variant="warning">
            <p>⚠️ Admin users' permissions cannot be modified</p>
          </InfoBox>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <n-button @click="closeEditDialog" secondary> Cancel </n-button>
          <n-button type="primary" @click="saveUser"> Save Changes </n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>
