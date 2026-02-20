<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { metroApi } from '@/services/api'
import type { Line, Station } from '@/types/metro_music'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const lines = ref<Line[]>([])
const stations = ref<Station[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  await loadData()
})

async function loadData() {
  loading.value = true
  error.value = null
  
  try {
    const [linesRes, stationsRes] = await Promise.all([
      metroApi.getLines(),
      metroApi.getStations()
    ])
    lines.value = linesRes.data || []
    stations.value = stationsRes.data || []
  } catch (err: any) {
    console.error('Failed to load metro data', err)
    error.value = err.response?.data?.message || '加载地铁数据失败'
    toast.error('无法加载地铁地图，请稍后重试')
  } finally {
    loading.value = false
  }
}

function retryLoad() {
  loadData()
}
</script>

<template>
  <div class="metro-map">
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载地铁地图中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <span class="error-icon">⚠️</span>
      <p>{{ error }}</p>
      <button @click="retryLoad" class="retry-btn">重新加载</button>
    </div>
    
    <template v-else>
      <div v-if="lines.length === 0 && stations.length === 0" class="empty-state">
        <span class="empty-icon">🚇</span>
        <p>暂无地铁数据</p>
      </div>
      
      <template v-else>
        <h2>Metro Lines</h2>
        <div v-if="lines.length > 0" class="lines-section">
          <div v-for="line in lines" :key="line.id" class="line-card" :style="{ borderColor: line.color }">
            <h3 :style="{ color: line.color }">{{ line.name }}</h3>
            <p>Required Level: {{ line.requiredLevel }}</p>
          </div>
        </div>
        <div v-else class="empty-section">
          <p>暂无线路信息</p>
        </div>
        
        <h2>Stations</h2>
        <div v-if="stations.length > 0" class="stations-grid">
          <div v-for="station in stations" :key="station.id" class="station-card">
            <h3>{{ station.name }}</h3>
            <p>{{ station.description || '暂无描述' }}</p>
            <router-link :to="`/metro/station/${station.pathKey}`" class="enter-btn">Enter Station</router-link>
          </div>
        </div>
        <div v-else class="empty-section">
          <p>暂无站点信息</p>
        </div>
      </template>
    </template>
  </div>
</template>

<style scoped>
.metro-map {
  padding: 20px;
}

.metro-map h2 {
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
  margin-bottom: 16px;
  margin-top: 24px;
}

.metro-map h2:first-child {
  margin-top: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  color: #ff4444;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.retry-btn {
  margin-top: 16px;
  padding: 8px 24px;
  background: rgba(255, 68, 68, 0.1);
  border: 1px solid #ff4444;
  color: #ff4444;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: #ff4444;
  color: white;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  color: var(--color-text-muted);
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-section {
  text-align: center;
  padding: 40px;
  color: var(--color-text-muted);
  border: 1px dashed var(--color-border);
  border-radius: 8px;
}

/* Line Cards */
.lines-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.line-card {
  border-left: 5px solid;
  padding: 15px;
  background: var(--color-surface);
  border-radius: 4px;
  border: 1px solid var(--color-border);
  border-left-width: 5px;
  color: var(--color-text);
  transition: transform 0.2s, box-shadow 0.2s;
}

.line-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Station Cards */
.stations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.station-card {
  border: 1px solid var(--color-primary);
  padding: 15px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.5);
  transition: transform 0.2s;
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.1);
}

.station-card h3 {
  color: var(--color-accent);
  margin-top: 0;
  margin-bottom: 8px;
}

.station-card p {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.station-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(0, 255, 157, 0.3);
}

.enter-btn {
  display: inline-block;
  padding: 8px 16px;
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  text-decoration: none;
  border-radius: 4px;
  border: 1px solid var(--color-primary);
  transition: all 0.3s;
  font-size: 0.9rem;
}

.enter-btn:hover {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}
</style>
