<template>
  <div>
    <h1>{{ username }}</h1>
    <p>{{ lastLogin }}</p>
    <p>Group: {{ group }}</p>
    <div id="clock">
      <div id="Date">{{ date }}</div>
      <ul>
        <li id="hours">{{ hours }}</li>
        <li id="point">:</li>
        <li id="min">{{ minutes }}</li>
        <li id="point">:</li>
        <li id="sec">{{ seconds }}</li>
      </ul>
    </div>
  </div>
  <Notification :message="notificationMessage" :type="notificationType" :trigger="notificationTrigger" />
</template>

<script>
import { ref, onMounted } from 'vue';
import { backendUrl } from '../config.js';
import Notification from './Notification.vue';

export default {
  name: 'SummaryPage',
  components: {
    Notification
  },
  setup() {
    const username = ref('User');
    const hours = ref('');
    const minutes = ref('');
    const seconds = ref('');
    const date = ref('');
    const group = ref('');
    const notificationMessage = ref('');
    const notificationType = ref('success');
    const notificationTrigger = ref(0);

    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${backendUrl}/api/user/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await response.json();
        if (data) {
          if (data.first_name && data.last_name) {
            username.value = `Welcome, ${data.first_name} ${data.last_name}!`;
          } else {
            username.value = 'Welcome, User!';
            notificationMessage.value = 'Please update your profile with your first and last name.';
            notificationType.value = 'error';
            notificationTrigger.value++;
          }

          if (data.last_login) {
            const lastLoginDate = new Date(data.last_login);
            const localLastLogin = lastLoginDate.toLocaleString();
            lastLogin.value = `Last login: ${localLastLogin}`;
          }

          if (data.groups && data.groups.length > 0) {
            const isAdmin = data.groups.some(group => group.name === 'admin');
            group.value = isAdmin ? 'admin' : 'user';
          } else {
            group.value = 'user'; // Default to user if no groups
          }
        } else {
          username.value = 'Welcome, User!';
          group.value = 'user';
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        username.value = 'Welcome, User!';
        group.value = 'user';
        notificationMessage.value = 'Failed to fetch user data.';
        notificationType.value = 'error';
        notificationTrigger.value++;
      }
    };

    const lastLogin = ref('');

    const clock = () => {
      const day = new Date();
      hours.value = day.getHours().toString().padStart(2, '0');
      minutes.value = day.getMinutes().toString().padStart(2, '0');
      seconds.value = day.getSeconds().toString().padStart(2, '0');

      const year = day.getFullYear();
      const month = String(day.getMonth() + 1).padStart(2, '0');
      const dayOfMonth = String(day.getDate()).padStart(2, '0');
      const dayOfWeek = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'][day.getDay()];
      const timeZone = day.toLocaleTimeString('en-US', { timeZoneName: 'short' }).split(' ')[2];

      date.value = `${year}-${month}-${dayOfMonth} ${dayOfWeek} ${timeZone}`;
    };

    onMounted(() => {
      fetchUserData();
      clock();
      setInterval(clock, 1000);
    });

    return {
      username,
      hours,
      minutes,
      seconds,
      date,
      lastLogin,
      group,
      notificationMessage,
      notificationType,
      notificationTrigger
    };
  }
}
</script>

<style scoped>
#clock {
  font-family: 'Share Tech Mono', monospace;
  color: #ffffff;
  text-align: center;
  position: relative;
  left: 0;
  top: 0;
  transform: none;
  margin: 0 auto;
  padding: 30px;
  border: 1px solid #333;
  background: #1e1e1e;
}

.time {
    letter-spacing: 0.05em;
    font-size: 120px;
    padding: 5px 0;
    color: #daf6ff;
}

.date {
    letter-spacing: 0.1em;
    font-size: 36px;
    color: #daf6ff;
}

.text {
    letter-spacing: 0.1em;
    font-size: 12px;
    padding: 20px 0 0;
}

#clock ul {
  width: 800px;
  padding: 0px;
  margin: 0px;
}

#clock ul li {
  display: inline-block;
  font-size: 8em;
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  color: #fff;
}
</style>
