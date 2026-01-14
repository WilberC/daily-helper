<script setup lang="ts">
</script>

<template>
  <header class="bg-surface-0 dark:bg-surface-900 border-b border-surface-200 dark:border-surface-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex justify-between items-center flex-wrap gap-4">
        <div class="flex items-center gap-4">
          <slot name="back-button" />
          <slot name="title" />
        </div>
        <div class="flex items-center gap-2">
          <slot name="actions" />
        </div>
      </div>
    </div>
  </header>
</template>
