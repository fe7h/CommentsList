<template>
  <form @submit.prevent="submitForm" class="p-4">
    <!-- Username -->
    <div class="mb-3">
      <label class="form-label">User Name*</label>
      <input v-model="form.username" type="text" class="form-control" :class="{ 'is-invalid': v$.form.username.$error }" />
      <div class="invalid-feedback">Only letters and digits allowed</div>
    </div>

    <!-- Email -->
    <div class="mb-3">
      <label class="form-label">Email*</label>
      <input v-model="form.email" type="email" class="form-control" :class="{ 'is-invalid': v$.form.email.$error }" />
      <div class="invalid-feedback">Invalid email</div>
    </div>

    <!-- Homepage -->
    <div class="mb-3">
      <label class="form-label">Home Page</label>
      <input v-model="form.homepage" type="url" class="form-control" :class="{ 'is-invalid': v$.form.homepage.$error }" />
      <div class="invalid-feedback">Invalid URL</div>
    </div>

    <!-- Answer -->
    <input v-model="form.answer" type="hidden" />

    <div
      v-if="form.answer"
      class="alert alert-primary py-2 px-3 small d-inline-flex align-items-center gap-2"
      role="alert"
      style="font-size: 0.85rem; word-break: break-word;"
    >
      <span>
        Answer to <strong>{{ form.answer.user_name }}</strong>
      </span>

      <button
        type="button"
        class="btn-close ms-2"
        aria-label="Close"
        @click="store.commit('DEL_REPLY')"
      ></button>
    </div>

    <!-- Text input -->
    <div class="mb-2">
      <label class="form-label">Text*</label>
      <div class="btn-group mb-2" role="group">
        <button type="button" class="btn btn-outline-secondary btn-sm" @click="insertTag('i')">[i]</button>
        <button type="button" class="btn btn-outline-secondary btn-sm" @click="insertTag('strong')">[strong]</button>
        <button type="button" class="btn btn-outline-secondary btn-sm" @click="insertTag('code')">[code]</button>
        <button type="button" class="btn btn-outline-secondary btn-sm" @click="insertTag('a')">[a]</button>
      </div>
      <textarea v-model="form.text" ref="textarea" class="form-control" rows="5"
        :class="{ 'is-invalid': v$.form.text.$error }"></textarea>
      <div class="invalid-feedback">Text must be valid XHTML with only allowed tags</div>
    </div>

    <!-- File input -->
    <div class="mb-3">
      <label class="form-label">Attach Media (Image or TXT)</label>
      <input type="file" class="form-control" @change="handleFileUpload" ref="fileInput"/>
      <div v-if="fileError" class="alert alert-danger mt-2 p-2">{{ fileError }}</div>
      <img v-if="previewImage" :src="previewImage" class="img-fluid mt-2 rounded border" style="max-width: 320px; max-height: 240px;" />
    </div>

    <!-- reCAPTCHA -->
    <RecaptchaV2
      @widget-id="handleWidgetId"
    />

    <!-- Submit -->
    <button type="submit" class="btn btn-primary">Send</button>
  </form>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { useStore } from 'vuex'
import { required, email, helpers, url, minLength, maxLength } from '@vuelidate/validators'
import axios from 'axios'
import { RecaptchaV2, useRecaptcha } from "vue3-recaptcha-v2"
import FingerprintJS from '@fingerprintjs/fingerprintjs'

const { handleGetResponse } = useRecaptcha()
const { handleReset } = useRecaptcha()
const captchaId= ref(null)

const store = useStore()

const form = ref({
  username: '',
  email: '',
  homepage: '',
  text: '',
  file: null,
  answer: computed(() => store.state.replyToComment),
})

const rules = {
  form: {
    username: { required, minLength: minLength(1), maxLength: maxLength(30)},
    email: { required, email },
    homepage: { url: helpers.withMessage('Invalid URL', url), $autoDirty: true },
    text: { required, maxLength: maxLength(5000) },
    file: {},
    answer: {},
  },
}

const v$ = useVuelidate(rules, { form })
const fileError = ref('')
const previewImage = ref(null)
const textarea = ref(null)
const fileInput = ref(null)

const handleWidgetId = (widgetId) => {
  captchaId.value = widgetId
}

onMounted(async () => {
  try {
    axios.defaults.withCredentials = true;
    await axios.get(store.getters['API_URL'] + 'csrf/')
  } catch (error) {
    console.error('Ошибка при запросе CSRF токена:', error)
  }
})

function insertTag(tag) {
  const el = textarea.value
  const start = el.selectionStart
  const end = el.selectionEnd
  const value = form.value.text
  let insert

  if (tag === 'a') {
    insert = `<a href="" title="">${value.substring(start, end)}</a>`
  } else {
    insert = `<${tag}>${value.substring(start, end)}</${tag}>`
  }

  form.value.text = value.substring(0, start) + insert + value.substring(end)
}

function handleFileUpload(event) {
  const file = event.target.files[0]
  fileError.value = ''
  previewImage.value = null
  if (!file) return

  form.value.file = file

  const isImage = ['image/jpeg', 'image/png', 'image/gif'].includes(file.type)
  const isText = file.type === 'text/plain'

  if (isImage) {
    const img = new Image()
    const reader = new FileReader()
    reader.onload = e => {
      img.src = e.target.result
      img.onload = () => {
        const { width, height } = img
        const maxWidth = 320
        const maxHeight = 240

        if (width > maxWidth || height > maxHeight) {
          const ratio = Math.min(maxWidth / width, maxHeight / height)
          const canvas = document.createElement('canvas')
          canvas.width = width * ratio
          canvas.height = height * ratio
          const ctx = canvas.getContext('2d')
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
          previewImage.value = canvas.toDataURL(file.type)
        } else {
          previewImage.value = img.src
        }
      }
    }
    reader.readAsDataURL(file)
  } else if (isText) {
    if (file.size > 102400) {
      fileError.value = 'Text file must be under 100KB'
    } else {
      fileError.value = ''
    }
  } else {
    fileError.value = 'Only JPG, PNG, GIF, or TXT files are allowed'
  }
}

function commentData(formData) {
  let resourcetype = 'topcomment'
  formData.append('user_name', form.value.username)
  formData.append('email', form.value.email)
  formData.append('home_page', form.value.homepage)
  formData.append('text', form.value.text)
  if (form.value.answer){
    formData.append('parent_comment_id', form.value.answer.id)
    resourcetype = 'nestedcomment'
    console.log(form.value.answer)
  }
  formData.append('resourcetype', resourcetype)
}

function mediaData(formData) {
  const PREFIX = 'attached_media.'
  let resourcetype = ''

  formData.append(PREFIX + 'data', form.value.file)

  const isImage = ['image/jpeg', 'image/png', 'image/gif'].includes(form.value.file.type)
  const isText = form.value.file.type === 'text/plain'
  if (isImage) {
    resourcetype = 'attachedimage'
  } else if(isText) {
    resourcetype = 'attachedfile'
  }

  formData.append(PREFIX + 'resourcetype', resourcetype)
}

async function userData(formData) {
  const fp = await FingerprintJS.load()
  const result = await fp.get()

  const components = result.components

  console.log(components)

  const userAgentFull = navigator.userAgent
  const userAgentBase = userAgentFull.split(' ')[0] || userAgentFull

  const userData = {
    user_agent: userAgentBase,
    screen_resolution: components.screenResolution ?
        `${components.screenResolution.value.width}x${components.screenResolution.value.height}` : '',
    color_depth: components.colorDepth ?
        components.colorDepth.value : 0,
    language: components.languages ?
        components.languages.value : '',
    timezone_offset: components.timezone ?
        components.timezone.value : '',
    cookie_enabled: components.cookiesEnabled ?
        components.cookiesEnabled.value : '',

    plugins: components.plugins ?
      components.plugins.value.map(p => p.name || JSON.stringify(p)).join(', ') : undefined,
    canvas_fp: components.canvas ?
        components.canvas.value : undefined,
    webgl_fp: components.webgl ?
        components.webgl.value : undefined,
    device_memory: components.deviceMemory && components.deviceMemory.value !== undefined ?
        components.deviceMemory.value : undefined,
    platform: components.platform ?
        components.platform.value.toString(): undefined,
  }

  const userDataJSON = JSON.stringify(userData)

  formData.append('user_data', userDataJSON)
}

function getCSRFToken() {
    let name = 'csrftoken';
    let value = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return value ? value.pop() : '';
}

async function submitForm() {
  v$.value.$touch()
  if (!v$.value.$invalid && !fileError.value) {
    let recaptchaData = handleGetResponse(captchaId.value)
    if (!recaptchaData) {
      alert('Please complete the captcha.')
    } else {
        try {
          const formData = new FormData()

          formData.append('recaptcha', recaptchaData)

          commentData(formData)
          await userData(formData)

          if (form.value.file) {
            mediaData(formData)
          }

          handleReset(captchaId.value)
          console.log(formData)

          const response = await axios.post(store.getters['API_URL'] + 'comments/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': getCSRFToken(),
            }
          })
          console.log('Form submitted successfully:', response.data)
          alert('Form submitted successfully!')
          store.commit('DEL_REPLY')
          form.value.text = ''
          form.value.file = null
          fileError.value = false
          previewImage.value = null

          if (fileInput.value) {
            fileInput.value.value = null
          }

          v$.value.$reset()
      } catch (error) {
          console.error('Error submitting form:', error)
          alert('There was an error submitting the form.')
      }
    }
  } else {
    alert('Please fix the errors.')
  }
}
</script>
