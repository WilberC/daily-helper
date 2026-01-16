<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import CreateUserForm from '@/components/users/CreateUserForm.vue'
import UserList from '@/components/users/UserList.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import PageWrapper from '@/components/layout/PageWrapper.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import PageContainer from '@/components/layout/PageContainer.vue'
import PageHeading from '@/components/common/typography/PageHeading.vue'
import BodyText from '@/components/common/typography/BodyText.vue'
import ContentCard from '@/components/layout/ContentCard.vue'

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
  <PageWrapper>
    <Toast />

    <!-- Header -->
    <PageHeader>
      <template #back-button>
        <Button icon="pi pi-arrow-left" severity="secondary" text @click="goToDashboard" />
      </template>

      <template #title>
        <PageHeading>User Management</PageHeading>
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
      <ContentCard>
        <TabView>
          <TabPanel header="Create Admin User">
            <div class="py-4">
              <BodyText class="mb-6">
                Create a new administrator account with full system access including user
                management.
              </BodyText>
              <CreateUserForm user-type="admin" />
            </div>
          </TabPanel>

          <TabPanel header="Create Staff User">
            <div class="py-4">
              <BodyText class="mb-6">
                Create a new staff account with elevated privileges but no user management access.
              </BodyText>
              <CreateUserForm user-type="staff" />
            </div>
          </TabPanel>

          <TabPanel header="Create Normal User">
            <div class="py-4">
              <BodyText class="mb-6">
                Create a new normal account with standard user access.
              </BodyText>
              <CreateUserForm user-type="normal" />
            </div>
          </TabPanel>

          <TabPanel header="Manage Users">
            <div class="py-4">
              <BodyText class="mb-6">
                View and manage all users. You can update user information and permissions for
                non-admin users.
              </BodyText>
              <UserList />
            </div>
          </TabPanel>
        </TabView>
      </ContentCard>
    </PageContainer>
  </PageWrapper>
</template>
