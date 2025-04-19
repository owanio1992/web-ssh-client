<template>
  <teleport to="body">
    <transition name="fade">
      <div v-if="visible" class="notification" :class="type">
        {{ message }}
      </div>
    </transition>
  </teleport>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  props: {
    message: String,
    type: {
      type: String,
      default: 'success', // 'success' or 'error'
    },
    duration: {
      type: Number,
      default: 3000, // milliseconds
    },
    trigger: Number, // A prop to trigger the notification visibility
  },
  setup(props) {
    const visible = ref(false);
    let timeoutId = null;

    watch(() => props.trigger, () => {
      if (props.message) {
        visible.value = true;
        clearTimeout(timeoutId); // Clear previous timeout if any
        timeoutId = setTimeout(() => {
          visible.value = false;
        }, props.duration);
      }
    });

    return {
      visible,
    };
  },
};
</script>

<style scoped>
.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 5px;
  color: white;
  font-size: 1em;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.notification.success {
  background-color: #4CAF50; /* Green */
}

.notification.error {
  background-color: #f44336; /* Red */
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
