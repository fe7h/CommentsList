<template>
  <div class="comment mb-2 p-3 bg-light rounded">

  <div class="comment mb-3">
    <div class="d-flex align-items-center mb-1">
      <div class="d-flex align-items-center gap-3 flex-grow-1">
        <template v-if="comment.home_page">
          <a :href="comment.home_page" target="_blank" rel="noopener" class="fw-semibold fs-6 text-decoration-none">
            {{ comment.user_name }}
          </a>
        </template>
        <template v-else>
          <strong class="fs-6">{{ comment.user_name }}</strong>
        </template>
        •
        <span class="text-muted small">
          {{ formatDate(comment.time_create) }}
        </span>
      </div>

      <button
        class="btn btn-link btn-sm p-0"
        @click="store.commit('SET_REPLY', { comment })"
        style="white-space: nowrap;"
      >
        Reply
      </button>
    </div>

    <div class="text-muted small d-flex align-items-center gap-2 mb-2">
      <i class="bi bi-envelope-fill"></i>
      <a :href="`mailto:${comment.email}`" class="text-muted text-decoration-none">
        {{ comment.email }}
      </a>
    </div>

    <div class="bg-secondary bg-opacity-10 rounded p-3">
      <p v-html="sanitizedText" class="mb-3"></p>

      <div v-if="comment.attached_media && comment.attached_media.data" class="mt-2">
        <template v-if="isImage(comment.attached_media.data)">
          <img
            :src="comment.attached_media.data"
            alt="Attached image"
            class="img-fluid rounded border"
            style="max-height: 250px; object-fit: contain;"
          />
        </template>
        <template v-else-if="isTextFile(comment.attached_media.data)">
          <a
            :href="comment.attached_media.data"
            target="_blank"
            rel="noopener"
            class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center gap-1"
          >
            <i class="bi bi-file-earmark-text"></i> 📄 Download attachment txt
          </a>
        </template>
      </div>
    </div>
  </div>

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

const isImage = (url) => {
  return /\.(jpe?g|png|gif|webp|bmp)$/i.test(url);
}

const isTextFile = (url) => {
  return /\.txt$/i.test(url);
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