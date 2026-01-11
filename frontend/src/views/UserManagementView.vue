<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import CreateUserForm from '@/components/users/CreateUserForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const goToDashboard = () => {
  router.push({ name: 'dashboard' })
}

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-screen bg-dark-bg">
    <Toast />
    
    <!-- Header -->
    <header class="bg-dark-surface border-b border-dark-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center flex-wrap gap-4">
          <div class="flex items-center gap-4">
            <Button
              icon="pi pi-arrow-left"
              severity="secondary"
              text
              @click="goToDashboard"
            />
            <h1 class="text-2xl font-bold text-dark-text">User Management</h1>
          </div>
          <Button
            label="Logout"
            icon="pi pi-sign-out"
            severity="danger"
            outlined
            @click="handleLogout"
          />
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-dark-surface border border-dark-border rounded-lg p-6">
        <TabView>
          <TabPanel header="Create Admin User">
            <div class="py-4">
              <p class="text-dark-text-secondary mb-6">
                Create a new administrator account with full system access.
              </p>
              <CreateUserForm :is-admin="true" />
            </div>
          </TabPanel>
          
          <TabPanel header="Create Staff User">
            <div class="py-4">
              <p class="text-dark-text-secondary mb-6">
                Create a new staff account with limited access.
              </p>
              <CreateUserForm :is-admin="false" />
            </div>
          </TabPanel>
        </TabView>
      </div>
    </main>
  </div>
</template>

<style scoped>
:deep(.p-tabview) {
  background: transparent;
}

:deep(.p-tabview-nav) {
  background: transparent;
  border-bottom-color: #334155;
}

:deep(.p-tabview-nav-link) {
  background: transparent;
  border-color: transparent;
  color: #94a3b8;
}

:deep(.p-tabview-nav-link:hover) {
  background: rgba(255, 255, 255, 0.05);
  color: #f1f5f9;
}

:deep(.p-tabview-nav li.p-highlight .p-tabview-nav-link) {
  background: transparent;
  border-color: #3b82f6;
  color: #f1f5f9;
}

:deep(.p-tabview-panels) {
  background: transparent;
  color: #f1f5f9;
}
</style>
