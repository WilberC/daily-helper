<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import type { User, UpdateUserInput } from '@/types/user'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Checkbox from 'primevue/checkbox'
import Tag from 'primevue/tag'

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

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

onMounted(() => {
  loadUsers()
})
</script>

<template>
  <div class="user-list-container">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-dark-text">All Users</h2>
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
    >
      <Column field="username" header="Username" sortable>
        <template #body="{ data }">
          <div class="flex items-center gap-2">
            <i class="pi pi-user text-blue-400"></i>
            <span class="font-medium">{{ data.username }}</span>
          </div>
        </template>
      </Column>

      <Column field="email" header="Email" sortable />

      <Column field="firstName" header="First Name" sortable />

      <Column field="lastName" header="Last Name" sortable />

      <Column field="isStaff" header="Role" sortable>
        <template #body="{ data }">
          <Tag
            :value="data.isStaff ? 'Admin' : 'Staff'"
            :severity="data.isStaff ? 'danger' : 'info'"
          />
        </template>
      </Column>

      <Column field="isActive" header="Status" sortable>
        <template #body="{ data }">
          <Tag
            :value="data.isActive ? 'Active' : 'Inactive'"
            :severity="data.isActive ? 'success' : 'warning'"
          />
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
        <div class="flex flex-col gap-2">
          <label for="edit-email" class="text-dark-text font-medium">
            Email <span class="text-red-400">*</span>
          </label>
          <InputText
            id="edit-email"
            v-model="editForm.email"
            type="email"
            placeholder="Enter email"
            class="w-full"
          />
        </div>

        <!-- First Name -->
        <div class="flex flex-col gap-2">
          <label for="edit-firstName" class="text-dark-text font-medium">First Name</label>
          <InputText
            id="edit-firstName"
            v-model="editForm.firstName"
            placeholder="Enter first name"
            class="w-full"
          />
        </div>

        <!-- Last Name -->
        <div class="flex flex-col gap-2">
          <label for="edit-lastName" class="text-dark-text font-medium">Last Name</label>
          <InputText
            id="edit-lastName"
            v-model="editForm.lastName"
            placeholder="Enter last name"
            class="w-full"
          />
        </div>

        <!-- Permissions Section -->
        <div class="bg-slate-800 border border-slate-700 rounded-lg p-4 space-y-3">
          <h3 class="text-dark-text font-medium mb-3">Permissions</h3>
          
          <!-- Staff Permission -->
          <div class="flex items-center gap-2">
            <Checkbox
              id="edit-isStaff"
              v-model="editForm.isStaff"
              :binary="true"
              :disabled="editingUser?.isStaff"
            />
            <label for="edit-isStaff" class="text-dark-text cursor-pointer">
              Admin Access
            </label>
          </div>

          <!-- Active Status -->
          <div class="flex items-center gap-2">
            <Checkbox
              id="edit-isActive"
              v-model="editForm.isActive"
              :binary="true"
            />
            <label for="edit-isActive" class="text-dark-text cursor-pointer">
              Active Account
            </label>
          </div>

          <p v-if="editingUser?.isStaff" class="text-yellow-400 text-sm mt-2">
            <i class="pi pi-exclamation-triangle mr-1"></i>
            Admin users' permissions cannot be modified
          </p>
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
        <Button
          label="Save Changes"
          icon="pi pi-check"
          @click="saveUser"
          severity="primary"
        />
      </template>
    </Dialog>
  </div>
</template>

<style scoped>
.user-list-container {
  width: 100%;
}

:deep(.user-table) {
  background: transparent;
}

:deep(.p-datatable .p-datatable-header) {
  background: #1e293b;
  border-color: #334155;
  color: #f1f5f9;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background: #1e293b;
  border-color: #334155;
  color: #f1f5f9;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
  background: #0f172a;
  color: #f1f5f9;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background: rgba(59, 130, 246, 0.1);
}

:deep(.p-datatable .p-datatable-tbody > tr.p-row-odd) {
  background: #1e293b;
}

:deep(.p-datatable .p-datatable-tbody > tr.p-row-odd:hover) {
  background: rgba(59, 130, 246, 0.15);
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  border-color: #334155;
}

:deep(.p-paginator) {
  background: #1e293b;
  border-color: #334155;
  color: #f1f5f9;
}

:deep(.p-paginator .p-paginator-pages .p-paginator-page) {
  color: #94a3b8;
}

:deep(.p-paginator .p-paginator-pages .p-paginator-page.p-highlight) {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #f1f5f9;
}

:deep(.p-dialog) {
  background: #1e293b;
  border: 1px solid #334155;
}

:deep(.p-dialog .p-dialog-header) {
  background: #1e293b;
  border-bottom: 1px solid #334155;
  color: #f1f5f9;
}

:deep(.p-dialog .p-dialog-content) {
  background: #1e293b;
  color: #f1f5f9;
}

:deep(.p-dialog .p-dialog-footer) {
  background: #1e293b;
  border-top: 1px solid #334155;
}

:deep(.p-inputtext) {
  background: #0f172a;
  border-color: #334155;
  color: #f1f5f9;
}

:deep(.p-inputtext:enabled:hover) {
  border-color: #475569;
}

:deep(.p-inputtext:enabled:focus) {
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
  font-weight: 600;
}
</style>
