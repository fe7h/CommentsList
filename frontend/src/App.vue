<template>
  <div>
    <h2>Топ комментарии</h2>
    <ul>
      <li v-for="item in topData" :key="item.id">
        <strong>{{ item.user_name }}</strong>: {{ item.text }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const topData = ref([])

const fetchTopData = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/top/')
    if (!response.ok) {
      throw new Error(`Ошибка запроса: ${response.status}`)
    }

    const data = await response.json()
    topData.value = data.results
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error)
  }
}

onMounted(() => {
  fetchTopData()
})
</script>

<style scoped>

</style>
