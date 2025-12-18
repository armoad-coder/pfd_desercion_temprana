<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-200">
    <div
      class="w-full max-w-sm bg-white p-8 rounded-lg shadow-lg border border-gray-300"
    >
      <!-- LOGO -->
      <img src="/logo_fct.png" class="mx-auto mb-4 w-48 object-contain" />

      <!-- TITULO -->
      <h2 class="text-xl font-bold text-gray-700 mb-6 text-center">
        Iniciar Sesión
      </h2>

      <!-- FORM -->
      <form @submit.prevent="login">
        <!-- Usuario -->
        <div class="mb-4">
          <label class="block text-gray-600 font-medium mb-1">Usuario</label>
          <input
            v-model="username"
            type="text"
            class="w-full px-3 py-2 border border-gray-400 rounded focus:ring-blue-600 focus:border-blue-600"
            placeholder="Ingresa tu usuario"
          />
        </div>

        <!-- Contraseña -->
        <div class="mb-5">
          <label class="block text-gray-600 font-medium mb-1">Contraseña</label>
          <input
            v-model="password"
            type="password"
            class="w-full px-3 py-2 border border-gray-400 rounded focus:ring-blue-600 focus:border-blue-600"
            placeholder="Ingresa tu contraseña"
          />
        </div>

        <!-- Error -->
        <transition name="fade">
          <div
            v-if="errorMessage"
            class="mb-4 px-4 py-3 bg-red-600 text-white rounded shadow-md text-sm font-medium"
          >
            {{ errorMessage }}
          </div>
        </transition>

        <!-- Botón -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-700 text-white py-2 rounded-md hover:bg-blue-800 transition font-semibold shadow disabled:opacity-60 disabled:cursor-not-allowed"
        >
          <span v-if="!loading">Ingresar</span>
          <span v-else>Ingresando...</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import api from "@/api/api";
import { useUserStore } from "@/stores/userStore";
import router from "@/router";

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);

const userStore = useUserStore();

const login = async () => {
  errorMessage.value = "";

  if (!username.value || !password.value) {
    errorMessage.value = "Debe ingresar usuario y contraseña.";
    return;
  }

  loading.value = true;

  try {
    const res = await api.post("/auth/login", {
      // El backend espera "email" y "password"
      email: username.value,
      password: password.value,
    });

    const { access_token, user } = res.data;

    // Guardamos en el store (y localStorage)
    userStore.login(access_token, user);

    // Redirigir a la ruta que consideres "inicio" (ajusta si quieres otra)
    router.push("/home");
  } catch (err: any) {
    errorMessage.value =
      err?.response?.data?.error || "Error al iniciar sesión.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
