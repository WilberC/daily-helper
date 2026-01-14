<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Toast from 'primevue/toast'
import ThemeToggle from '@/components/ThemeToggle.vue'
import PageWrapper from '@/components/layout/PageWrapper.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import PageHeading from '@/components/common/typography/PageHeading.vue'
import SectionHeading from '@/components/common/typography/SectionHeading.vue'
import BodyText from '@/components/common/typography/BodyText.vue'
import DataField from '@/components/common/display/DataField.vue'
import InfoBox from '@/components/common/feedback/InfoBox.vue'
import GridContainer from '@/components/layout/GridContainer.vue'

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
  <PageWrapper>
    <Toast />
    
    <!-- Header -->
    <PageHeader>
      <template #title>
        <PageHeading>Daily Helper</PageHeading>
      </template>
      
      <template #actions>
        <ThemeToggle />
        <Button
          label="Logout"
          icon="pi pi-sign-out"
          severity="danger"
          outlined
          @click="handleLogout"
        />
      </template>
    </PageHeader>

    <!-- Main Content -->
    <PageContainer>
      <GridContainer cols="2">
        <!-- Welcome Card -->
        <Card>
          <template #header>
            <div class="p-6 pb-0">
              <SectionHeading variant="primary">Welcome Back!</SectionHeading>
            </div>
          </template>
          
          <template #content>
            <div class="space-y-3">
              <DataField label="Username" :value="user?.username" />
              <DataField label="Email" :value="user?.email" />
              
              <DataField label="Role">
                <i :class="authStore.isAdmin ? 'pi pi-shield' : 'pi pi-user'" class="mr-2"></i>
                {{ userRole }}
              </DataField>
            </div>
          </template>
        </Card>

        <!-- Quick Actions Card -->
        <Card v-if="authStore.isAdmin">
          <template #header>
            <div class="p-6 pb-0">
              <SectionHeading>Quick Actions</SectionHeading>
            </div>
          </template>
          
          <template #content>
            <div class="space-y-4">
              <BodyText>
                As an administrator, you have access to user management features.
              </BodyText>
              
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
        <Card v-else>
          <template #header>
            <div class="p-6 pb-0">
              <SectionHeading variant="primary">Information</SectionHeading>
            </div>
          </template>
          
          <template #content>
            <InfoBox variant="info">
              <template #default="{ textColor }">
                <p :class="textColor">
                  You are logged in as a staff member. Contact an administrator for user management access.
                </p>
              </template>
            </InfoBox>
          </template>
        </Card>
      </GridContainer>
    </PageContainer>
  </PageWrapper>
</template>
