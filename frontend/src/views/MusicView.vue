<script setup lang="ts">
import MusicPlayer from '@/components/music/MusicPlayer.vue'
</script>

<template>
  <div class="music-view">
    <div class="header-section">
      <h1>Echoom Chamber</h1>
      <p>Listen to the resonating sounds of the digital soul.</p>
    </div>
    <MusicPlayer />
  </div>
</template>

<style scoped>
.music-view {
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
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
}

.header-section p {
  font-size: 1.2rem;
  color: #666;
}
</style>
