<script setup lang="ts">
import { RouterView } from 'vue-router'
import TheHeader from '@/components/layout/TheHeader.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
</script>

<template>
  <div class="app">
    <TheHeader />
    <main class="main-content">
      <RouterView />
    </main>
    <TheFooter />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
  color: #333;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

a {
  color: #42b883;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

button {
  cursor: pointer;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #42b883;
  color: white;
  font-size: 14px;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #3aa876;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

input, textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #42b883;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
