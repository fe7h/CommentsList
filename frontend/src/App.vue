<template>
  <div>

    <Comment v-for="obj in topComments" :key="obj.id" :comment="obj"/>

    <button v-if="nextPageUrl" @click="fetchTopData">More</button>
    <p v-show="!nextPageUrl">END</p>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Comment from "@/components/Comment.vue";

const topComments = ref([])
let nextPageUrl = 'http://localhost:8000/api/comments/top/'

const fetchTopData = async () => {
  try {
    const response = await fetch(nextPageUrl)
    if (!response.ok) {
      throw new Error(`Ошибка запроса: ${response.status}`)
    }

    const data = await response.json()
    topComments.value.push(...data.results)
    nextPageUrl = data.next
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
