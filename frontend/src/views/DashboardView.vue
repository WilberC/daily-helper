<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Toast from 'primevue/toast'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const user = computed(() => authStore.currentUser)
const userRole = computed(() => (authStore.isAdmin ? 'Administrator' : 'Staff'))

const handleLogout = async () => {
  const result = await authStore.logout()
  
  if (result.success) {
    toast.add({
      severity: 'success',
      summary: 'Logged Out',
      detail: result.message,
      life: 3000,
    })
    router.push({ name: 'login' })
  } else {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: result.message,
      life: 5000,
    })
  }
}

const goToUserManagement = () => {
  router.push({ name: 'users' })
}
</script>

<template>
  <div class="min-h-screen bg-dark-bg">
    <Toast />
    
    <!-- Header -->
    <header class="bg-dark-surface border-b border-dark-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-dark-text">Daily Helper</h1>
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
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Welcome Card -->
        <Card class="bg-dark-surface border border-dark-border">
          <template #header>
            <div class="p-6 pb-0">
              <h2 class="text-xl font-semibold text-dark-text">Welcome Back!</h2>
            </div>
          </template>
          
          <template #content>
            <div class="space-y-3">
              <div>
                <p class="text-sm text-dark-text-secondary">Username</p>
                <p class="text-lg font-medium text-dark-text">{{ user?.username }}</p>
              </div>
              
              <div>
                <p class="text-sm text-dark-text-secondary">Email</p>
                <p class="text-lg font-medium text-dark-text">{{ user?.email }}</p>
              </div>
              
              <div>
                <p class="text-sm text-dark-text-secondary">Role</p>
                <p class="text-lg font-medium text-dark-text">
                  <i :class="authStore.isAdmin ? 'pi pi-shield' : 'pi pi-user'" class="mr-2"></i>
                  {{ userRole }}
                </p>
              </div>
            </div>
          </template>
        </Card>

        <!-- Quick Actions Card -->
        <Card v-if="authStore.isAdmin" class="bg-dark-surface border border-dark-border">
          <template #header>
            <div class="p-6 pb-0">
              <h2 class="text-xl font-semibold text-dark-text">Quick Actions</h2>
            </div>
          </template>
          
          <template #content>
            <div class="space-y-4">
              <p class="text-dark-text-secondary">
                As an administrator, you have access to user management features.
              </p>
              
              <Button
                label="Manage Users"
                icon="pi pi-users"
                severity="primary"
                class="w-full"
                @click="goToUserManagement"
              />
            </div>
          </template>
        </Card>

        <!-- Info Card for Non-Admin -->
        <Card v-else class="bg-dark-surface border border-dark-border">
          <template #header>
            <div class="p-6 pb-0">
              <h2 class="text-xl font-semibold text-dark-text">Information</h2>
            </div>
          </template>
          
          <template #content>
            <p class="text-dark-text-secondary">
              You are logged in as a staff member. Contact an administrator for user management access.
            </p>
          </template>
        </Card>
      </div>
    </main>
  </div>
</template>

<style scoped>
:deep(.p-card) {
  background: var(--p-surface-0);
  border-radius: 0.75rem;
}

:deep(.p-button) {
  font-weight: 600;
}
</style>
