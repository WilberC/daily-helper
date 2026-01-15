/** * Displays a list of users in a data table with edit capabilities. * Allows administrators to
view and update user information. * @component */
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import type { User, UpdateUserInput } from '@/types/user'
import { formatDate } from '@/composables/useFormatters'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Checkbox from 'primevue/checkbox'
import Tag from 'primevue/tag'
import SectionHeading from '@/components/common/typography/SectionHeading.vue'
import SubHeading from '@/components/common/typography/SubHeading.vue'
import FormField from '@/components/common/form/FormField.vue'
import InfoBox from '@/components/common/feedback/InfoBox.vue'
import Badge from '@/components/common/utils/Badge.vue'

const toast = useToast()
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
    toast.add({
      severity: 'success',
      summary: 'User Updated',
      detail: result.message,
      life: 5000,
    })
    closeEditDialog()
    await loadUsers()
  } else {
    toast.add({
      severity: 'error',
      summary: 'Update Failed',
      detail: result.message,
      life: 5000,
    })
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<template>
  <div class="user-list-container">
    <div class="flex justify-between items-center mb-6">
      <SectionHeading variant="primary">All Users</SectionHeading>
      <Button
        label="Refresh"
        icon="pi pi-refresh"
        @click="loadUsers"
        :loading="loading"
        severity="secondary"
        outlined
      />
    </div>

    <DataTable
      :value="users"
      :loading="loading"
      stripedRows
      paginator
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      class="user-table"
      responsiveLayout="scroll"
      aria-label="User list table"
    >
      <Column field="username" header="Username" sortable>
        <template #body="{ data }">
          <div class="flex items-center gap-2">
            <i class="pi pi-user text-primary-400" aria-hidden="true"></i>
            <span class="font-medium">{{ data.username }}</span>
          </div>
        </template>
      </Column>

      <Column field="email" header="Email" sortable />

      <Column field="firstName" header="First Name" sortable />

      <Column field="lastName" header="Last Name" sortable />

      <Column field="isStaff" header="Role" sortable>
        <template #body="{ data }">
          <Badge :variant="data.isStaff ? 'admin' : 'staff'" />
        </template>
      </Column>

      <Column field="isActive" header="Status" sortable>
        <template #body="{ data }">
          <Badge :variant="data.isActive ? 'active' : 'inactive'" />
        </template>
      </Column>

      <Column field="dateJoined" header="Joined" sortable>
        <template #body="{ data }">
          {{ formatDate(data.dateJoined) }}
        </template>
      </Column>

      <Column header="Actions">
        <template #body="{ data }">
          <Button
            icon="pi pi-pencil"
            severity="info"
            text
            rounded
            @click="openEditDialog(data)"
            :disabled="data.isStaff"
            :aria-label="data.isStaff ? 'Cannot edit admin users' : `Edit user ${data.username}`"
            v-tooltip.top="data.isStaff ? 'Cannot edit admin users' : 'Edit user'"
          />
        </template>
      </Column>
    </DataTable>

    <!-- Edit User Dialog -->
    <Dialog
      v-model:visible="editDialogVisible"
      :header="`Edit User: ${editingUser?.username}`"
      :modal="true"
      :closable="true"
      :style="{ width: '500px' }"
      class="edit-dialog"
    >
      <div class="space-y-4 py-4">
        <!-- Email -->
        <FormField label="Email" for="edit-email" required>
          <InputText
            id="edit-email"
            v-model="editForm.email"
            type="email"
            placeholder="Enter email"
            class="w-full"
          />
        </FormField>

        <!-- First Name -->
        <FormField label="First Name" for="edit-firstName">
          <InputText
            id="edit-firstName"
            v-model="editForm.firstName"
            placeholder="Enter first name"
            class="w-full"
          />
        </FormField>

        <!-- Last Name -->
        <FormField label="Last Name" for="edit-lastName">
          <InputText
            id="edit-lastName"
            v-model="editForm.lastName"
            placeholder="Enter last name"
            class="w-full"
          />
        </FormField>

        <!-- Permissions Section -->
        <div
          class="bg-surface-0 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg p-4 space-y-3"
        >
          <SubHeading>Permissions</SubHeading>

          <!-- Staff Permission -->
          <div class="flex items-center gap-2">
            <Checkbox
              id="edit-isStaff"
              v-model="editForm.isStaff"
              :binary="true"
              :disabled="editingUser?.isStaff"
            />
            <label for="edit-isStaff" class="text-surface-700 dark:text-dark-text cursor-pointer">
              Admin Access
            </label>
          </div>

          <!-- Active Status -->
          <div class="flex items-center gap-2">
            <Checkbox id="edit-isActive" v-model="editForm.isActive" :binary="true" />
            <label for="edit-isActive" class="text-surface-700 dark:text-dark-text cursor-pointer">
              Active Account
            </label>
          </div>

          <InfoBox v-if="editingUser?.isStaff" variant="warning">
            <template #default="{ textColor }">
              <p :class="textColor">
                <i class="pi pi-exclamation-triangle mr-1"></i>
                Admin users' permissions cannot be modified
              </p>
            </template>
          </InfoBox>
        </div>
      </div>

      <template #footer>
        <Button
          label="Cancel"
          icon="pi pi-times"
          @click="closeEditDialog"
          severity="secondary"
          outlined
        />
        <Button label="Save Changes" icon="pi pi-check" @click="saveUser" severity="primary" />
      </template>
    </Dialog>
  </div>
</template>
