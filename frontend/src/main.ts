import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./style.css"; // o main.css, según tu proyecto

const app = createApp(App);

app.use(createPinia()); // primero Pinia
app.use(router); // luego el router

app.mount("#app");
