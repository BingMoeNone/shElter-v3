<script setup lang="ts">
import MetroMap from '@/components/metro/MetroMap.vue'
</script>

<template>
  <div class="metro-view">
    <div class="header-section">
      <h1>Metro Network</h1>
      <p>Explore the interconnected realms of knowledge, soul, and echo.</p>
    </div>
    <MetroMap />
  </div>
</template>

<style scoped>
.metro-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.header-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #FF4444, #4444FF, #44FF44);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-section p {
  font-size: 1.2rem;
  color: #666;
}
</style>
