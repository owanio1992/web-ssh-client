import './assets/main.css'

import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from './components/LoginPage.vue';
import Homepage from './components/Homepage.vue';
import TerminalPage from './components/TerminalPage.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    { path: '/login', component: LoginPage },
    { path: '/homepage', component: Homepage, meta: { requiresAuth: true } },
    { path: '/terminal', component: TerminalPage, meta: { requiresAuth: true } },
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token');
    const expiry = localStorage.getItem('expiry');

    if (!token || !expiry) {
      next('/login');
      return;
    }

    const now = new Date().getTime();
    if (now > parseInt(expiry)) {
      localStorage.removeItem('token');
      localStorage.removeItem('expiry');
      next('/login');
      return;
    }

    next();
  } else {
    next();
  }
});

const app = createApp(App);
app.use(router);
app.mount('#app');
