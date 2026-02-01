<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { NButton, NTabs, NTabPane, NIcon } from 'naive-ui'
import { ArrowBack, LogOut } from '@vicons/ionicons5'
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
    <!-- Header -->
    <PageHeader>
      <template #back-button>
        <n-button text circle @click="goToDashboard">
          <template #icon>
            <n-icon><ArrowBack /></n-icon>
          </template>
        </n-button>
      </template>

      <template #title>
        <PageHeading>User Management</PageHeading>
      </template>

      <template #actions>
        <ThemeToggle />
        <n-button secondary @click="handleLogout">
          <template #icon>
            <n-icon><LogOut /></n-icon>
          </template>
          Logout
        </n-button>
      </template>
    </PageHeader>

    <!-- Main Content -->
    <PageContainer>
      <ContentCard>
        <n-tabs type="line" animated>
          <n-tab-pane name="admin" tab="Create Admin User">
            <div class="py-4">
              <BodyText class="mb-6">
                Create a new administrator account with full system access including user
                management.
              </BodyText>
              <CreateUserForm user-type="admin" />
            </div>
          </n-tab-pane>

          <n-tab-pane name="staff" tab="Create Staff User">
            <div class="py-4">
              <BodyText class="mb-6">
                Create a new staff account with elevated privileges but no user management access.
              </BodyText>
              <CreateUserForm user-type="staff" />
            </div>
          </n-tab-pane>

          <n-tab-pane name="normal" tab="Create Normal User">
            <div class="py-4">
              <BodyText class="mb-6">
                Create a new normal account with standard user access.
              </BodyText>
              <CreateUserForm user-type="normal" />
            </div>
          </n-tab-pane>

          <n-tab-pane name="manage" tab="Manage Users">
            <div class="py-4">
              <BodyText class="mb-6">
                View and manage all users. You can update user information and permissions for
                non-admin users.
              </BodyText>
              <UserList />
            </div>
          </n-tab-pane>
        </n-tabs>
      </ContentCard>
    </PageContainer>
  </PageWrapper>
</template>
