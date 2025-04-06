import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from './components/LoginPage.vue'
import Homepage from './components/Homepage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    { path: '/login', component: LoginPage },
    { path: '/homepage', component: Homepage },
  ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')
