<template>
  <transition
    enter-active-class="duration-300 ease-in"
    leave-active-class="duration-300 ease-[cubic-bezier(0, 1, 0.5, 1)]"
    enter-to-class="max-h-[200px] overflow-hidden"
    leave-from-class="max-h-[200px] overflow-hidden"
    enter-from-class="max-h-0 overflow-hidden"
    leave-to-class="max-h-0 overflow-hidden"
  >
    <div v-if="opened">
      <slot v-bind="{ opened, open, close, toggle }" />
    </div>
  </transition>
</template>
<script setup>
import { ref } from 'vue'
const props = defineProps({
  label: {
    type: String,
    default: '',
  },
  hideLabel: {
    type: Boolean,
    default: false,
  },
  isOpened: {
    type: Boolean,
    default: true,
  },
})
function toggle() {
  opened.value = !opened.value
}

function open() {
  opened.value = true
}

function close() {
  opened.value = false
}

let opened = ref(props.isOpened)
let hide = ref(props.hideLabel)
</script>
