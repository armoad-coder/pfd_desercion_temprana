<script setup lang="ts">
import { ref, computed } from "vue";
import axios from "axios";
import AcademicEvolution from "@/components/dashboard/AcademicEvolution.vue";
import HeatmapMateriasAlumno from "@/components/dashboard/HeatmapMateriasAlumno.vue";

// ==========================================
// ESTADO Y LÓGICA (INTACTOS)
// ==========================================
const idAlumno = ref<string>("");
const loading = ref(false);
const error = ref<string | null>(null);
const data = ref<any | null>(null);

const formatName = (name: string) => {
  return name
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (c) => c.toUpperCase())
    .replace("De", "de")
    .replace("Y", "y");
};

const maxProb = () => {
  if (!data.value) return 0;
  return Math.max(
    ...Object.values(data.value.probabilidades as Record<string, number>)
  );
};

const buscar = async () => {
  error.value = null;
  data.value = null;
  if (!idAlumno.value) {
    error.value = "Ingrese un ID de alumno";
    return;
  }
  try {
    loading.value = true;
    const res = await axios.get(
      `http://localhost:5000/prediccion/informatica/v1/${idAlumno.value}`
    );
    data.value = res.data;
  } catch (e) {
    console.error(e);
    error.value = "Alumno no encontrado o error en la predicción";
  } finally {
    loading.value = false;
  }
};

const recomendaciones = computed(() => {
  if (!data.value) return [];
  const recs = [];
  const mats = data.value.materias || {};
  if (data.value.prediccion && data.value.prediccion.includes("Deserción")) {
    recs.push({
      tipo: "urgente",
      msg: "Programar entrevista con Orientación inmediatamente.",
      icon: "🚨",
      color: "bg-red-50 text-red-700 border-red-100",
    });
  }
  const calc1 = mats["CALCULO I"];
  const alg1 = mats["ALGEBRA I"];
  if ((calc1 && calc1 < 2) || (alg1 && alg1 < 2)) {
    recs.push({
      tipo: "academico",
      msg: "Refuerzo necesario en Ciencias Básicas.",
      icon: "📐",
      color: "bg-blue-50 text-blue-700 border-blue-100",
    });
  }
  if (mats.Ausencias > 20) {
    recs.push({
      tipo: "conductual",
      msg: "Revisar situación de ausentismo.",
      icon: "📅",
      color: "bg-amber-50 text-amber-700 border-amber-100",
    });
  }
  if (recs.length === 0) {
    recs.push({
      tipo: "info",
      msg: "Trayectoria estable detectada.",
      icon: "✨",
      color: "bg-emerald-50 text-emerald-700 border-emerald-100",
    });
  }
  return recs;
});

const conteoNotas = computed(() => {
  if (!data.value || !data.value.materias) return null;
  const counts = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0 };
  const blacklist = [
    "Promedio",
    "Ausencias",
    "TiempoEstudio",
    "aplazos",
    "CincoF",
    "id_alumno",
  ];
  Object.entries(data.value.materias).forEach(([key, val]) => {
    if (blacklist.includes(key) || typeof val !== "number") return;
    let nota = Math.round(val);
    if (nota > 5) nota = 5;
    if (nota < 0) nota = 0;
    counts[nota]++;
  });
  const maxCount = Math.max(...Object.values(counts));
  return { counts, maxCount };
});
</script>

<template>
  <div
    class="min-h-screen bg-slate-50 relative selection:bg-indigo-100 selection:text-indigo-700"
  >
    <div
      class="absolute inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:24px_24px] opacity-40 pointer-events-none"
    ></div>

    <div class="relative max-w-7xl mx-auto p-6 md:p-8 space-y-8">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">
            Dashboard Académico
          </h1>
          <p class="text-slate-500 font-medium">
            Ingeniería Informática • Análisis Predictivo
          </p>
        </div>

        <div class="w-full md:w-auto min-w-[320px] relative group">
          <div
            class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none"
          >
            <svg
              class="h-5 w-5 text-slate-400 group-focus-within:text-indigo-500 transition-colors"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <input
            v-model="idAlumno"
            type="number"
            placeholder="Buscar por ID (ej: 1001)..."
            class="block w-full pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-full text-sm placeholder-slate-400 shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all duration-300"
            @keyup.enter="buscar"
          />
          <button
            @click="buscar"
            :disabled="loading"
            class="absolute right-1.5 top-1.5 bottom-1.5 px-5 bg-slate-900 hover:bg-indigo-600 text-white rounded-full text-sm font-semibold transition-colors shadow-md disabled:opacity-70"
          >
            <span v-if="loading" class="animate-pulse">...</span>
            <span v-else>Ir</span>
          </button>
        </div>
      </div>

      <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform -translate-y-2 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
      >
        <div
          v-if="error"
          class="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-lg shadow-sm flex items-center"
        >
          <span class="text-red-700 font-medium">{{ error }}</span>
        </div>
      </transition>

      <div
        v-if="data"
        class="grid grid-cols-1 xl:grid-cols-3 gap-6 animate-in fade-in zoom-in-95 duration-500"
      >
        <div
          class="group relative overflow-hidden rounded-3xl bg-slate-900 p-8 text-white shadow-xl h-[340px] flex flex-col justify-between border border-slate-700/50"
        >
          <div
            class="absolute inset-0 bg-gradient-to-br from-violet-600 via-indigo-600 to-blue-700 opacity-90 group-hover:opacity-100 transition-opacity duration-500"
          ></div>
          <div
            class="absolute -top-24 -right-24 w-64 h-64 bg-white/10 rounded-full blur-3xl group-hover:bg-white/20 transition-all duration-700"
          ></div>

          <div class="relative z-10">
            <div
              class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/10 text-xs font-semibold tracking-wider uppercase mb-4"
            >
              <span
                class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"
              ></span>
              Diagnóstico IA
            </div>
            <div
              class="text-5xl font-black tracking-tight leading-tight drop-shadow-sm"
            >
              {{ data.prediccion }}
            </div>
          </div>

          <div class="relative z-10 grid grid-cols-2 gap-4 mt-auto">
            <div
              class="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10"
            >
              <div
                class="text-xs text-indigo-100 font-medium uppercase opacity-80"
              >
                Certeza
              </div>
              <div class="text-2xl font-bold">{{ maxProb().toFixed(1) }}%</div>
            </div>
            <div
              class="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10"
            >
              <div
                class="text-xs text-indigo-100 font-medium uppercase opacity-80"
              >
                Carrera
              </div>
              <div class="text-lg font-bold truncate">Ing. Informática</div>
            </div>
          </div>
        </div>

        <div
          class="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 h-[340px] flex flex-col relative overflow-hidden"
        >
          <h3
            class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2"
          >
            <span class="p-1.5 bg-indigo-50 text-indigo-600 rounded-lg"
              >💡</span
            >
            Recomendaciones
          </h3>
          <div class="overflow-y-auto pr-2 space-y-3 custom-scrollbar flex-1">
            <div
              v-for="(rec, idx) in recomendaciones"
              :key="idx"
              class="flex gap-4 p-4 rounded-2xl border transition-all hover:shadow-md cursor-default"
              :class="rec.color || 'bg-slate-50 border-slate-100'"
            >
              <span class="text-2xl shrink-0 filter drop-shadow-sm">{{
                rec.icon
              }}</span>
              <p class="text-sm font-medium text-slate-700 leading-snug">
                {{ rec.msg }}
              </p>
            </div>
          </div>
          <div
            class="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-white to-transparent pointer-events-none"
          ></div>
        </div>

        <div
          class="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 h-[340px] flex flex-col"
        >
          <h3
            class="text-lg font-bold text-slate-800 mb-5 flex items-center gap-2"
          >
            <span class="p-1.5 bg-indigo-50 text-indigo-600 rounded-lg"
              >📊</span
            >
            Escenarios
          </h3>
          <div class="space-y-5 overflow-y-auto pr-2 custom-scrollbar flex-1">
            <div
              v-for="(prob, estado) in data.probabilidades"
              :key="estado"
              class="group"
            >
              <div class="flex justify-between items-end mb-2">
                <span
                  class="text-sm font-semibold text-slate-600 group-hover:text-indigo-600 transition-colors"
                  >{{ estado }}</span
                >
                <span class="text-sm font-bold text-slate-800"
                  >{{ prob }}%</span
                >
              </div>
              <div
                class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden"
              >
                <div
                  class="h-full rounded-full transition-all duration-1000 ease-out relative"
                  :class="prob > 50 ? 'bg-indigo-600' : 'bg-slate-400'"
                  :style="{ width: prob + '%' }"
                >
                  <div
                    class="absolute inset-0 bg-white/20 w-full animate-[shimmer_2s_infinite]"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="xl:col-span-3 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            class="bg-white rounded-3xl border border-slate-200 shadow-sm p-1 h-[400px] hover:shadow-lg transition-shadow duration-300"
          >
            <AcademicEvolution :materias="data.materias" />
          </div>

          <div
            class="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 h-[400px] flex flex-col"
          >
            <div class="flex items-center justify-between mb-6">
              <h3
                class="text-lg font-bold text-slate-800 flex items-center gap-2"
              >
                <span class="p-1.5 bg-indigo-50 text-indigo-600 rounded-lg"
                  >🎯</span
                >
                Distribución
              </h3>
              <span
                class="text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded-md"
                >Total:
                {{
                  Object.values(conteoNotas.counts).reduce((a, b) => a + b, 0)
                }}
                materias</span
              >
            </div>

            <div
              v-if="conteoNotas"
              class="space-y-3 overflow-y-auto pr-2 flex-1 custom-scrollbar"
            >
              <div
                v-for="nota in [5, 4, 3, 2, 1, 0]"
                :key="nota"
                class="group flex items-center gap-4 p-2 rounded-xl hover:bg-slate-50 transition-colors"
              >
                <div
                  class="w-10 h-10 flex items-center justify-center rounded-xl font-bold text-white shadow-sm shrink-0 text-sm transition-transform group-hover:scale-110"
                  :class="{
                    'bg-emerald-500 ring-4 ring-emerald-50 text-emerald-50':
                      nota === 5,
                    'bg-blue-500 ring-4 ring-blue-50 text-blue-50': nota === 4,
                    'bg-amber-400 ring-4 ring-amber-50 text-white': nota === 3,
                    'bg-orange-500 ring-4 ring-orange-50 text-orange-50':
                      nota === 2,
                    'bg-rose-500 ring-4 ring-rose-50 text-rose-50': nota === 1,
                    'bg-slate-400 ring-4 ring-slate-50 text-slate-50':
                      nota === 0,
                  }"
                >
                  {{ nota === 0 ? "🚫" : nota }}
                </div>

                <div class="flex-1 flex flex-col gap-1">
                  <div
                    class="flex justify-between text-xs font-medium text-slate-500"
                  >
                    <span>{{
                      nota === 0 ? "Ausente / Abandono" : `Nota ${nota}`
                    }}</span>
                    <span class="text-slate-700 font-bold">{{
                      conteoNotas.counts[nota]
                    }}</span>
                  </div>
                  <div class="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all duration-1000"
                      :class="{
                        'bg-emerald-500': nota === 5,
                        'bg-blue-500': nota === 4,
                        'bg-amber-400': nota === 3,
                        'bg-orange-500': nota === 2,
                        'bg-rose-500': nota === 1,
                        'bg-slate-400': nota === 0,
                      }"
                      :style="{
                        width:
                          conteoNotas.maxCount > 0
                            ? (conteoNotas.counts[nota] /
                                conteoNotas.maxCount) *
                                100 +
                              '%'
                            : '0%',
                      }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            <div
              v-else
              class="flex items-center justify-center h-full text-slate-400"
            >
              Sin datos
            </div>
          </div>
        </div>

        <div class="xl:col-span-3">
          <HeatmapMateriasAlumno
            :materias-raw="data.materias"
            :loading="loading"
          />
        </div>
      </div>

      <div
        v-else-if="loading && !data"
        class="flex flex-col items-center justify-center py-32 opacity-70"
      >
        <div class="relative w-16 h-16">
          <div
            class="absolute top-0 left-0 w-full h-full border-4 border-slate-200 rounded-full"
          ></div>
          <div
            class="absolute top-0 left-0 w-full h-full border-4 border-indigo-600 rounded-full animate-spin border-t-transparent"
          ></div>
        </div>
        <p class="mt-4 text-slate-500 font-medium animate-pulse">
          Analizando historial académico...
        </p>
      </div>

      <div
        v-else-if="!data && !loading && !error"
        class="text-center py-20 opacity-60"
      >
        <div class="text-6xl mb-4">🎓</div>
        <h2 class="text-2xl font-bold text-slate-800">
          Bienvenido al Dashboard
        </h2>
        <p class="text-slate-500">
          Ingresa el ID del alumno para comenzar el análisis.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scrollbar bonita para contenedores internos */
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 20px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}

/* Animación de shimmer opcional */
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
