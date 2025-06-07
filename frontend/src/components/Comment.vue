<template>
        <div class="comment mb-2 p-3 bg-light rounded">
          <div class="mb-1">
            <strong>{{ comment.user_name }}</strong>
            <span class="text-muted small">• {{ formatDate(comment.time_create) }}</span>
            <button class="btn btn-link btn-sm p-0 mb-1">Ответить</button>
          </div>
          <p v-html="sanitizedText"></p>

          <button
              class="btn btn-sm btn-outline-primary mt-2 toggle-replies-btn"
              type="button"
              @click="handleShowReplies"
              :disabled="isLoading"
          >
            Показать ответы
          </button>

          <!-- Ответы -->
          <div class="comment-reply mt-3">

            <Comment v-for="obj in nestedComments" :key="obj.id" :comment="obj"/>

            <button v-if="nextPageUrl" @click="fetchData">More</button>

            <div v-if="showReplys && nestedComments.length === 0">
              <!-- Скрытая часть -->
              <div class="no-replies-text text-muted fst-italic">Нет ответов</div>
            </div>

          </div>
        </div>
</template>

<script setup>
import {defineAsyncComponent, computed, ref} from 'vue'

const props = defineProps({
  comment: Object
})

const Comment = defineAsyncComponent(() => import('./Comment.vue'))
const showReplys = ref(false)
const isLoading = ref(false)
const nestedComments = ref([])
import { useStore } from 'vuex'
import xss from 'xss'

let nextPageUrl = ''
const store = useStore()

const sanitizedText = computed(() => {
  const xssOptions = {
    whiteList: {
      a: ['href', 'title'],
      code: [],
      i: [],
      strong: [],
    },
  }

  return xss(props.comment.text, xssOptions)
})

const formatDate = (isoStr) => {
  return new Date(isoStr).toLocaleString('en', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

const fetchData = async () => {
  try {
    let response

    if (nextPageUrl) {
      response = await fetch(nextPageUrl)
    } else {
      response = await fetch(`http://localhost:8000/api/comments/${props.comment.id}/nested/`)
    }

    if (!response.ok) {
      throw new Error(`Ошибка запроса: ${response.status}`)
    }

    const data = await response.json()
    nestedComments.value.push(...data.results)
    nextPageUrl = data.next

    if (nextPageUrl === null) {
        store.commit('ADD_BRANCHES', {id: props.comment.id, nestedComments })
    }

  } catch (error) {
    console.error('Ошибка при загрузке данных:', error)
  }
}

const handleShowReplies = async () => {
  if (isLoading.value) return

  isLoading.value = true
  try {
    await fetchData()
    showReplys.value = true
  } catch (e) {
    console.error(e)
  }
}
</script>

<style>
.comment-reply {
  margin-left: 1.5rem;
  border-left: 2px solid #dee2e6;
  padding-left: 1rem;
}
</style>