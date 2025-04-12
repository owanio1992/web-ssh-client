<template>
  <div>
    <h1>Terminal</h1>
    <p>Connecting to: {{ site }} - {{ server }}</p>
    <div id="terminal"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

export default {
  props: {
    site: {
      type: String,
      required: true
    },
    server: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const terminal = ref(null);

    onMounted(() => {
      const term = new Terminal();
      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      term.open(document.getElementById('terminal'));
      fitAddon.fit();

      term.writeln('Welcome to the terminal!');
      term.writeln(`Connecting to ${props.site} - ${props.server}...`);
    });

    return {
      terminal
    };
  }
}
</script>

<style scoped>
#terminal {
  width: 800px;
  height: 600px;
}
</style>
