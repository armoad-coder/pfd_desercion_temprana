<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

import DonutActividadCarreras from "@/components/dashboard/DonutActividadCarreras.vue";
import TopMateriasAplazadasBar from "@/components/dashboard/TopMateriasAplazadasBar.vue";

const router = useRouter();
const carreras = ref([]);

/* Navegación dinámica a predicción */
function irAPrediccion(carreraKey) {
  router.push(`/prediccion/${carreraKey}`);
}

onMounted(async () => {
  const res = await axios.get("/dashboard/data");
  const data = res.data;

  carreras.value = [
    {
      key: "informatica",
      title: "Ingeniería Informática",
      alumnos: data.informatica.alumnos,
      materias: data.informatica.materias,
      color: "bg-indigo-600",
    },
    {
      key: "electronica",
      title: "Ingeniería Electrónica",
      alumnos: data.electronica.alumnos,
      materias: data.electronica.materias,
      color: "bg-cyan-600",
    },
    {
      key: "electricidad",
      title: "Ingeniería Electricidad",
      alumnos: data.electricidad.alumnos,
      materias: data.electricidad.materias,
      color: "bg-amber-500",
    },
    {
      key: "civil",
      title: "Ingeniería Civil",
      alumnos: data.civil.alumnos,
      materias: data.civil.materias,
      color: "bg-stone-500",
    },
  ];
});
</script>

<template>
  <div class="p-6 space-y-8 bg-slate-50 min-h-screen">
    <!-- ================= KPIs SUPERIORES ================= -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      <div
        v-for="c in carreras"
        :key="c.key"
        class="relative bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg transition p-6"
      >
        <div
          :class="`h-2 w-full rounded-t-2xl absolute top-0 left-0 ${c.color}`"
        ></div>

        <h3 class="mt-4 text-lg font-bold text-slate-800">
          {{ c.title }}
        </h3>

        <div class="mt-4 space-y-2">
          <p class="text-3xl font-extrabold text-slate-900">
            {{ c.alumnos }}
            <span class="text-sm font-medium text-slate-500">Alumnos</span>
          </p>

          <p class="text-3xl font-extrabold text-slate-900">
            {{ c.materias }}
            <span class="text-sm font-medium text-slate-500">Materias</span>
          </p>
        </div>
        <button
          @click="irAPrediccion(c.key)"
          class="mt-5 w-full flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 border border-transparent bg-gradient-to-r from-indigo-600 to-indigo-500 text-white font-semibold hover:from-indigo-700 hover:to-indigo-600 active:scale-[0.98] transition-all duration-200 shadow-sm"
        >
          <span class="text-lg">🔮</span>
          Predicción IA
        </button>
      </div>
    </div>

    <!-- ================= PARTE INFERIOR ================= -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
      <!-- Representatividad -->
      <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <h4 class="text-lg font-semibold text-slate-800 mb-4">
          Representatividad por carrera
        </h4>

        <DonutActividadCarreras />
      </div>

      <!-- Top materias -->
      <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <h4 class="text-lg font-semibold text-slate-800 mb-4">
          Top materias con más aplazos
        </h4>
        <!-- Barras horizontales -->
        <TopMateriasAplazadasBar />
      </div>
    </div>
    <!-- ================= GRÁFICOS CENTRALES ================= -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
      <!-- Cantidad de alumnos -->
      <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <h4 class="text-lg font-semibold text-slate-800 mb-4">
          Cantidad de alumnos
        </h4>
        <div class="h-64 flex items-center justify-center text-slate-400">
          📈 Gráfico de líneas (mock)
        </div>
      </div>

      <!-- Cantidad de aplazados -->
      <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <h4 class="text-lg font-semibold text-slate-800 mb-4">
          Cantidad de aplazados
        </h4>
        <div class="h-64 flex items-center justify-center text-slate-400">
          📉 Gráfico de líneas (mock)
        </div>
      </div>
    </div>
    <!-- ================= BLOQUE FUTURO IA ================= -->
    <div
      class="bg-indigo-50 border-2 border-dashed border-indigo-300 rounded-2xl p-6 text-center"
    >
      <h4 class="text-lg font-semibold text-indigo-700 mb-2">
        🔮 Predicción IA (futuro)
      </h4>
      <p class="text-indigo-600">
        Este bloque se activará cuando integremos los modelos predictivos.
      </p>
    </div>
  </div>
</template>
