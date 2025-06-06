<template>
  <div>
    <div class="d-flex gap-2 mb-3">
      <button
          v-for="field in orderingFields"
          :key="field"
          type="button"
          class="btn"
          :class="currentOrdering.field === field ? 'btn-primary' : 'btn-outline-primary'"
          @click="toggleOrdering(field)"
      >
        {{ fieldLabels[field] }}
        <span v-if="currentOrdering.field === field">
      {{ currentOrdering.desc ? '↓' : '↑' }}
        </span>
      </button>
    </div>

      <Comment v-for="obj in topComments" :key="obj.id" :comment="obj"/>

      <button v-if="nextPageUrl" @click="fetchTopData">More</button>
      <p v-show="!nextPageUrl">END</p>

    <Form />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Comment from "@/components/Comment.vue"
import Form from "@/components/Form.vue"

const topComments = ref([])
let nextPageUrl = 'http://localhost:8000/api/comments/top/'
const currentOrdering = ref({ field: 'time_create', desc: true })
const orderingFields = ['user_name', 'email', 'time_create']
const fieldLabels = {
  user_name: 'User Name',
  email: 'Email',
  time_create: 'Created'
}

const buildUrl = () => {
  const orderParam = currentOrdering.value.desc
    ? `-${currentOrdering.value.field}`
    : currentOrdering.value.field
  return `http://localhost:8000/api/comments/top/?ordering=${orderParam}`
}

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

const toggleOrdering = (field) => {
  if (currentOrdering.value.field === field) {
    currentOrdering.value.desc = !currentOrdering.value.desc
  } else {
    currentOrdering.value.field = field
    currentOrdering.value.desc = false
  }

  topComments.value = []
  nextPageUrl = buildUrl()
  fetchTopData()
}

onMounted(() => {
  fetchTopData()
})
</script>

<style scoped>

</style>
