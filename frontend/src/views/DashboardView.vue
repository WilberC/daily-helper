<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMessage } from 'naive-ui'
import { NButton, NCard, NIcon } from 'naive-ui'
import { LogOut, People, Shield, Person } from '@vicons/ionicons5'
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
import { useTranslation } from '@/composables/useTranslation'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const { t } = useTranslation()

const user = computed(() => authStore.currentUser)
const userRole = computed(() =>
  authStore.isAdmin ? t('users.types.admin') : t('users.types.staff'),
)

const handleLogout = async () => {
  const result = await authStore.logout()

  if (result.success) {
    message.success(result.message, { duration: 3000 })
    router.push({ name: 'login' })
  } else {
    message.error(result.message, { duration: 5000 })
  }
}

const goToUserManagement = () => {
  router.push({ name: 'users' })
}
</script>

<template>
  <PageWrapper>
    <!-- Header -->
    <PageHeader>
      <template #title>
        <PageHeading>{{ t('login.title') }}</PageHeading>
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
      <GridContainer cols="2">
        <!-- Welcome Card -->
        <n-card>
          <template #header>
            <div class="p-6 pb-0">
              <SectionHeading variant="primary">{{
                t('dashboard.welcome', { name: user?.username || '' })
              }}</SectionHeading>
            </div>
          </template>

          <div class="space-y-3">
            <DataField :label="t('users.table.username')" :value="user?.username" />
            <DataField :label="t('users.table.email')" :value="user?.email" />

            <DataField :label="t('users.table.role')">
              <n-icon :component="authStore.isAdmin ? Shield : Person" class="mr-2" />
              {{ userRole }}
            </DataField>
          </div>
        </n-card>

        <!-- Quick Actions Card -->
        <n-card v-if="authStore.isAdmin">
          <template #header>
            <div class="p-6 pb-0">
              <SectionHeading>{{ t('dashboard.quickActions') }}</SectionHeading>
            </div>
          </template>

          <div class="space-y-4">
            <BodyText>{{ t('dashboard.overview') }}</BodyText>

            <n-button type="primary" block @click="goToUserManagement">
              <template #icon>
                <n-icon><People /></n-icon>
              </template>
              {{ t('users.management') }}
            </n-button>
          </div>
        </n-card>

        <!-- Info Card for Non-Admin -->
        <n-card v-else>
          <template #header>
            <div class="p-6 pb-0">
              <SectionHeading variant="primary">Information</SectionHeading>
            </div>
          </template>

          <InfoBox variant="info">
            <p>{{ t('dashboard.overview') }}</p>
          </InfoBox>
        </n-card>
      </GridContainer>
    </PageContainer>
  </PageWrapper>
</template>
