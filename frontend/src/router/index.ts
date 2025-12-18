import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import UsersView from "@/views/UsersView.vue";
import ConfigModelosView from "@/views/ConfigModelosView.vue";
import PrediccionAlumnoView from "@/views/PrediccionAlumnoView.vue";
import PrediccionAlumnoCivilView from "@/views/PrediccionAlumnoCivilView.vue";
import PrediccionAlumnoElectricidadView from "@/views/PrediccionAlumnoElectricidadView.vue";
import PrediccionAlumnoElectronicaView from "@/views/PrediccionAlumnoElectronicaView.vue";
import PrediccionAlumnoInformaticaView from "@/views/PrediccionAlumnoInformaticaView.vue";

import { useUserStore } from "@/stores/userStore";

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/home",
    name: "Home",
    component: HomeView,
    meta: { requiresAuth: true }, // ruta protegida
  },
  {
    path: "/usuarios",
    name: "Usuarios",
    component: UsersView,
    meta: { requiresAuth: true }, // también protegido
  },
  {
    path: "/config/modelos",
    name: "ConfigModelos",
    component: ConfigModelosView,
    meta: { requiresAuth: true },
  },
  {
    path: "/config/carga-datos/informatica",
    name: "CargaDatosInformatica",
    component: () => import("@/views/MasivaInformaticaView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/config/carga-datos/electricidad",
    name: "CargaDatosElectricidad",
    component: () => import("@/views/MasivaElectricidadView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/config/carga-datos/civil",
    name: "CargaDatosCivil",
    component: () => import("@/views/MasivaCivilView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/config/carga-datos/electronica",
    name: "CargaDatosElectronica",
    component: () => import("@/views/MasivaElectronicaView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/login",
  },

  {
    path: "/prediccion-alumno",
    name: "PrediccionAlumno",
    component: PrediccionAlumnoView,
  },
  {
    path: "/prediccion/informatica",
    name: "PrediccionInformatica",
    component: PrediccionAlumnoInformaticaView,
  },
  {
    path: "/prediccion/electronica",
    component: PrediccionAlumnoElectronicaView,
  },
  {
    path: "/prediccion/electricidad",
    component: PrediccionAlumnoElectricidadView,
  },
  {
    path: "/prediccion/civil",
    component: PrediccionAlumnoCivilView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ==== GUARD GLOBAL DE AUTENTICACIÓN ====
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isAuthenticated = !!userStore.token;

  // Si la ruta requiere login y NO tenemos token
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: "Login" });
  }

  // Si YA hay token y el usuario intenta ir a /login
  if (to.name === "Login" && isAuthenticated) {
    return next({ name: "Home" });
  }

  next();
});

export default router;
