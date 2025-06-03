<template>
        <div class="comment mb-2 p-3 bg-light rounded">
          <div class="mb-1">
            <strong>{{ comment.user_name }}</strong>
            <span class="text-muted small">• {{ formatDate(comment.time_create) }}</span>
            <button class="btn btn-link btn-sm p-0 mb-1">Ответить</button>
          </div>
          <p>{{ comment.text }}</p>
          <button class="btn btn-sm btn-outline-primary mt-2 toggle-replies-btn" type="button">Показать ответы</button>

          <!-- Нет ответов -->
          <div class="comment-reply mt-3">
            <div class="no-replies-text text-muted fst-italic">Нет ответов</div>
          </div>
        </div>
</template>

<script setup>

const props = defineProps({
  comment: Object
})

import { defineAsyncComponent } from 'vue'
const Comment = defineAsyncComponent(() => import('./Comment.vue'))

const formatDate = (isoStr) => {
  return new Date(isoStr).toLocaleString('en', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

</script>

<style>
.comment-reply {
  margin-left: 1.5rem;
  border-left: 2px solid #dee2e6;
  padding-left: 1rem;
}
</style>