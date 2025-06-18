<template>
  <div class="comments-container">
    <div class="comments-wrapper">
      <div>
        <h1 class="mb-4">Comments</h1>
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

        <div class="container my-5">
          <Comment v-for="obj in topComments" :key="obj.id" :comment="obj"/>
          <button
            v-if="nextPageUrl"
            @click="fetchTopData"
            type="button"
            class="btn btn-primary"
          >
            Load more
          </button>

          <p v-show="!nextPageUrl" class="text-center text-muted fst-italic mt-3">
            That's all!
          </p>
        </div>

        <div v-if="store.getters['GET_FORM_STATE']" class="floating-form">
          <Form />
        </div>

        <button class="floating-btn" @click="store.commit('FORM_VISIBLE')">
          <transition name="fade" mode="out-in">
            <span :key="store.getters['GET_FORM_STATE']">
             {{ store.getters['GET_FORM_STATE'] ? '–' : '+' }}
            </span>
          </transition>
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Comment from "@/components/Comment.vue"
import Form from "@/components/Form.vue"
import { useStore } from 'vuex'

const store = useStore()

const topComments = ref([])
let nextPageUrl = store.getters['API_URL'] + 'comments/top/'
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
  return store.getters['API_URL'] + `comments/top/?ordering=${orderParam}`
}

const fetchTopData = async () => {
  try {
    const response = await fetch(nextPageUrl)
    if (!response.ok) {
      throw new Error(`Ошибка запроса: ${response.status}`)
    }

    const data = await response.json()
    topComments.value.push(...data.results)
    store.commit('ADD_BRANCHES', {id: 'top', commentsBranch: topComments })
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
  store.dispatch('createWebSocket', 'ws://localhost:8000/ws/connect/')
  fetchTopData()
})
</script>

<style scoped>
.floating-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #0d6efd;
  color: #fff;
  border: none;
  font-size: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  z-index: 1000;
}

.floating-btn:hover {
  background-color: #0b5ed7;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
  transform: scale(1);
}

.floating-form {
  position: fixed;
  bottom: 100px;
  right: 20px;
  width: 500px;
  max-height: 80vh;
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  z-index: 1001;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.comments-container {
  display: flex;
  justify-content: left;
  align-items: center;
  height: 100vh;       /* 100% высоты окна браузера */
  width: 100vw;        /* 100% ширины окна браузера */
  overflow: visible;   /* чтобы не было прокруток внутри */
  box-sizing: border-box;
  padding: 20px;       /* отступы чтобы не прилегало к краям */
}

.comments-wrapper {
  width: 850px;        /* фиксированная ширина */
  height: 700px;       /* фиксированная высота */
  overflow: visible;   /* без прокрутки */
 /* для видимости блока */
  border-radius: 8px;
  padding: 1rem;

  box-sizing: border-box;
}
</style>
