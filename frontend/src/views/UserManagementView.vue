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
import { useTranslation } from '@/composables/useTranslation'

const router = useRouter()
const authStore = useAuthStore()
const { t } = useTranslation()

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
        <PageHeading>{{ t('users.management') }}</PageHeading>
      </template>

      <template #actions>
        <ThemeToggle />
        <n-button secondary @click="handleLogout">
          <template #icon>
            <n-icon><LogOut /></n-icon>
          </template>
          {{ t('nav.logout') }}
        </n-button>
      </template>
    </PageHeader>

    <!-- Main Content -->
    <PageContainer>
      <ContentCard>
        <n-tabs type="line" animated>
          <n-tab-pane name="admin" :tab="t('users.createAdmin')">
            <div class="py-4">
              <BodyText class="mb-6">{{ t('users.info.adminDescription') }}</BodyText>
              <CreateUserForm user-type="admin" />
            </div>
          </n-tab-pane>

          <n-tab-pane name="staff" :tab="t('users.createStaff')">
            <div class="py-4">
              <BodyText class="mb-6">{{ t('users.info.staffDescription') }}</BodyText>
              <CreateUserForm user-type="staff" />
            </div>
          </n-tab-pane>

          <n-tab-pane name="normal" :tab="t('users.createNormal')">
            <div class="py-4">
              <BodyText class="mb-6">{{ t('users.info.normalDescription') }}</BodyText>
              <CreateUserForm user-type="normal" />
            </div>
          </n-tab-pane>

          <n-tab-pane name="manage" :tab="t('users.list')">
            <div class="py-4">
              <BodyText class="mb-6">{{ t('dashboard.overview') }}</BodyText>
              <UserList />
            </div>
          </n-tab-pane>
        </n-tabs>
      </ContentCard>
    </PageContainer>
  </PageWrapper>
</template>
