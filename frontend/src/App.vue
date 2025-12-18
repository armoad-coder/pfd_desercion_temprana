<template>
  <div
    class="min-h-screen bg-slate-50 relative selection:bg-indigo-100 selection:text-indigo-700 font-sans text-slate-600"
  >
    <div
      class="fixed inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:24px_24px] opacity-40 pointer-events-none z-0"
    ></div>

    <header
      v-if="showLayout"
      class="fixed top-0 inset-x-0 h-16 z-40 border-b border-slate-200/60 bg-white/80 backdrop-blur-xl transition-all duration-300"
    >
      <div
        class="h-full px-4 md:px-6 flex items-center justify-between max-w-[1920px] mx-auto"
      >
        <div class="flex items-center gap-4">
          <button
            class="md:hidden p-2 rounded-xl text-slate-500 hover:bg-slate-100 hover:text-indigo-600 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            @click="toggleSidebar"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h7"
              ></path>
            </svg>
          </button>

          <div class="flex items-center gap-3">
            <div
              class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/30 text-white font-bold text-lg"
            >
              P
            </div>
            <div class="hidden md:flex flex-col">
              <span class="font-bold text-slate-800 leading-none"
                >Predicción App</span
              >
              <span
                class="text-[10px] uppercase tracking-wider text-slate-500 font-semibold mt-0.5"
                >Ingeniería</span
              >
            </div>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <div
            v-if="userStore.user"
            class="hidden sm:flex items-center gap-3 pl-4 border-l border-slate-200/60"
          >
            <div class="flex flex-col items-end">
              <span class="text-sm font-bold text-slate-700">
                {{ userStore.user.nombre }} {{ userStore.user.apellido }}
              </span>
              <span class="text-xs text-slate-400 font-medium">
                {{ userStore.user.email }}
              </span>
            </div>
            <div
              class="w-9 h-9 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-600 font-bold shadow-sm"
            >
              {{ userStore.user.nombre?.charAt(0) || "U" }}
            </div>
          </div>

          <button
            @click="handleLogout"
            class="group relative flex items-center justify-center p-2 rounded-xl text-slate-400 hover:text-red-600 hover:bg-red-50 transition-all duration-200"
            title="Cerrar Sesión"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <div
      v-if="showLayout && isSidebarOpen"
      class="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40 md:hidden transition-opacity"
      @click="closeSidebar"
    ></div>

    <aside
      v-if="showLayout"
      :class="[
        'fixed top-16 bottom-0 left-0 z-40 w-64 bg-white/90 backdrop-blur-xl border-r border-slate-200/60 transform transition-transform duration-300 cubic-bezier(0.4, 0, 0.2, 1)',
        isSidebarOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full',
        'md:translate-x-0 md:shadow-none',
      ]"
    >
      <nav
        class="h-full flex flex-col py-6 px-3 overflow-y-auto custom-scrollbar"
      >
        <div class="mb-2 px-3">
          <p
            class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2"
          >
            Principal
          </p>
        </div>

        <div class="space-y-1 mb-6">
          <RouterLink
            :to="{ name: 'Home' }"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="
                (e) => {
                  navigate(e);
                  closeSidebarOnMobile();
                }
              "
              class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
              :class="
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-sm ring-1 ring-indigo-200'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              "
            >
              <span
                class="text-lg filter grayscale group-hover:grayscale-0 transition-all duration-200"
                >🏠</span
              >
              <span>Inicio</span>
            </a>
          </RouterLink>
        </div>

        <div class="mb-2 px-3 pt-4 border-t border-slate-100">
          <p
            class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2"
          >
            Administración
          </p>
        </div>

        <div class="space-y-1 mb-6">
          <RouterLink
            :to="{ name: 'Usuarios' }"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="
                (e) => {
                  navigate(e);
                  closeSidebarOnMobile();
                }
              "
              class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
              :class="
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-sm ring-1 ring-indigo-200'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              "
            >
              <span
                class="text-lg filter grayscale group-hover:grayscale-0 transition-all"
                >👥</span
              >
              <span>Usuarios</span>
            </a>
          </RouterLink>

          <RouterLink
            :to="{ name: 'ConfigModelos' }"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="
                (e) => {
                  navigate(e);
                  closeSidebarOnMobile();
                }
              "
              class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
              :class="
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-sm ring-1 ring-indigo-200'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              "
            >
              <span
                class="text-lg filter grayscale group-hover:grayscale-0 transition-all"
                >⚙️</span
              >
              <span>Modelos IA</span>
            </a>
          </RouterLink>
        </div>

        <div class="mb-2 px-3 pt-4 border-t border-slate-100">
          <p
            class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2"
          >
            Importar Datos
          </p>
        </div>

        <div class="space-y-1">
          <RouterLink
            :to="{ name: 'CargaDatosInformatica' }"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="
                (e) => {
                  navigate(e);
                  closeSidebarOnMobile();
                }
              "
              class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
              :class="
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-sm ring-1 ring-indigo-200'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              "
            >
              <span
                class="flex items-center justify-center w-6 h-6 rounded-md bg-blue-100 text-blue-600 text-xs font-bold group-hover:bg-blue-600 group-hover:text-white transition-colors"
                >IN</span
              >
              <span>Informatica</span>
            </a>
          </RouterLink>

          <RouterLink
            :to="{ name: 'CargaDatosElectricidad' }"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="
                (e) => {
                  navigate(e);
                  closeSidebarOnMobile();
                }
              "
              class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
              :class="
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-sm ring-1 ring-indigo-200'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              "
            >
              <span
                class="flex items-center justify-center w-6 h-6 rounded-md bg-amber-100 text-amber-600 text-xs font-bold group-hover:bg-amber-500 group-hover:text-white transition-colors"
                >EL</span
              >
              <span>Electricidad</span>
            </a>
          </RouterLink>

          <RouterLink
            :to="{ name: 'CargaDatosCivil' }"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="
                (e) => {
                  navigate(e);
                  closeSidebarOnMobile();
                }
              "
              class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
              :class="
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-sm ring-1 ring-indigo-200'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              "
            >
              <span
                class="flex items-center justify-center w-6 h-6 rounded-md bg-stone-100 text-stone-600 text-xs font-bold group-hover:bg-stone-600 group-hover:text-white transition-colors"
                >CI</span
              >
              <span>Civil</span>
            </a>
          </RouterLink>

          <RouterLink
            :to="{ name: 'CargaDatosElectronica' }"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="
                (e) => {
                  navigate(e);
                  closeSidebarOnMobile();
                }
              "
              class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
              :class="
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-sm ring-1 ring-indigo-200'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              "
            >
              <span
                class="flex items-center justify-center w-6 h-6 rounded-md bg-emerald-100 text-emerald-600 text-xs font-bold group-hover:bg-emerald-600 group-hover:text-white transition-colors"
                >EC</span
              >
              <span>Electrónica</span>
            </a>
          </RouterLink>
        </div>

        <div class="mt-auto pt-6 px-3">
          <div
            class="p-3 bg-slate-50 rounded-xl border border-slate-100 text-center"
          >
            <p class="text-[10px] text-slate-400 font-medium">
              © {{ new Date().getFullYear() }} Predicción App v1.2
            </p>
          </div>
        </div>
      </nav>
    </aside>

    <main
      :class="[
        'relative z-0 min-h-screen transition-all duration-300 ease-in-out',
        showLayout ? 'pt-20 md:pl-64 pr-4 pl-4 md:pr-8' : '',
      ]"
    >
      <RouterView v-slot="{ Component }">
        <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
        >
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute, useRouter, RouterView, RouterLink } from "vue-router";
import { useUserStore } from "@/stores/userStore";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const isSidebarOpen = ref(false);

const showLayout = computed(() => route.name !== "Login");

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const closeSidebar = () => {
  isSidebarOpen.value = false;
};

const closeSidebarOnMobile = () => {
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false;
  }
};

const handleLogout = () => {
  userStore.logout();
  router.push("/login");
};
</script>

<style scoped>
/* Scrollbar bonita para el sidebar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e2e8f0;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #cbd5e1;
}
</style>
