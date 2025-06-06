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

    <!-- Tag panel -->
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
      <input type="file" class="form-control" @change="handleFileUpload" />
      <div v-if="fileError" class="alert alert-danger mt-2 p-2">{{ fileError }}</div>
      <img v-if="previewImage" :src="previewImage" class="img-fluid mt-2 rounded border" style="max-width: 320px; max-height: 240px;" />
    </div>

    <!-- Submit -->
    <button type="submit" class="btn btn-primary">Send</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers, url, minLength, maxLength } from '@vuelidate/validators'

const allowedTags = ['a', 'code', 'i', 'strong']

function isValidXHTML(value) {
  const parser = new DOMParser()
  const wrapped = `<body>${value}</body>`
  const doc = parser.parseFromString(wrapped, 'application/xhtml+xml')
  const parserError = doc.querySelector('parsererror')
  if (parserError) return false

  const nodes = doc.body.querySelectorAll('*')
  for (const node of nodes) {
    const tag = node.tagName.toLowerCase()
    if (!allowedTags.includes(tag)) return false
    if (tag === 'a' && (!node.hasAttribute('href') || !node.hasAttribute('title'))) {
      return false
    }
  }
  return true
}

const htmlValidation = helpers.withMessage(
  'Text must be valid XHTML and use only allowed tags',
  value => isValidXHTML(value)
)

const form = ref({
  username: '',
  email: '',
  homepage: '',
  text: '',
})

const rules = {
  form: {
    username: { required, minLength: minLength(1), maxLength: maxLength(30)},
    email: { required, email },
    homepage: { url: helpers.withMessage('Invalid URL', url), $autoDirty: true },
    text: { required, htmlValidation },
  },
}

const v$ = useVuelidate(rules, { form })
console.log("v$ object: ", v$)
const fileError = ref('')
const previewImage = ref(null)
const textarea = ref(null)

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

function submitForm() {
  v$.value.$touch()
  if (!v$.value.$invalid && !fileError.value) {
    alert('Form is valid and ready for submission!')
  } else {
    alert('Please fix the errors.')
  }
}
</script>
