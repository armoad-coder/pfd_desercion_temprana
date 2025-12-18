<script setup>
import { ref } from "vue";

const idAlumno = ref("");
const alumno = ref(null);
const loading = ref(false);
const error = ref("");

function buscarAlumno() {
  error.value = "";
  alumno.value = null;

  if (!idAlumno.value) {
    error.value = "Debe ingresar un ID de alumno";
    return;
  }

  loading.value = true;

  // MOCK – luego se conecta al backend
  setTimeout(() => {
    if (idAlumno.value === "123") {
      alumno.value = {
        id: 123,
        carrera: "Ingeniería Informática",
        estado: "Activo",
        promedio: 2.45,
        aplazos: 8,
        ausencias: 12,
      };
    } else {
      error.value = "Alumno no encontrado";
    }
    loading.value = false;
  }, 800);
}
</script>

<template>
  <div class="p-6 space-y-6 bg-slate-50 min-h-screen">
    <!-- Título -->
    <div>
      <h2 class="text-2xl font-bold text-slate-800">Predicción por Alumno</h2>
      <p class="text-slate-500">
        Consulta individual de rendimiento y riesgo académico
      </p>
    </div>

    <!-- Buscador -->
    <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <div class="flex gap-4 items-end">
        <div class="flex-1">
          <label class="block text-sm font-medium text-slate-600 mb-1">
            ID del Alumno
          </label>
          <input
            v-model="idAlumno"
            type="number"
            placeholder="Ej: 123"
            class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        <button
          @click="buscarAlumno"
          class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium"
        >
          Buscar
        </button>
      </div>

      <p v-if="error" class="mt-3 text-sm text-red-600">
        {{ error }}
      </p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center text-slate-500">
      Cargando información del alumno...
    </div>

    <!-- Datos del alumno -->
    <div
      v-if="alumno"
      class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm"
    >
      <h3 class="text-lg font-semibold text-slate-800 mb-4">
        Información del Alumno
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <div>
          <p class="text-sm text-slate-500">ID Alumno</p>
          <p class="font-bold text-slate-800">{{ alumno.id }}</p>
        </div>

        <div>
          <p class="text-sm text-slate-500">Carrera</p>
          <p class="font-bold text-slate-800">{{ alumno.carrera }}</p>
        </div>

        <div>
          <p class="text-sm text-slate-500">Estado</p>
          <p class="font-bold text-slate-800">{{ alumno.estado }}</p>
        </div>

        <div>
          <p class="text-sm text-slate-500">Promedio</p>
          <p class="font-bold text-slate-800">{{ alumno.promedio }}</p>
        </div>

        <div>
          <p class="text-sm text-slate-500">Aplazos</p>
          <p class="font-bold text-slate-800">{{ alumno.aplazos }}</p>
        </div>

        <div>
          <p class="text-sm text-slate-500">Ausencias</p>
          <p class="font-bold text-slate-800">{{ alumno.ausencias }}</p>
        </div>
      </div>
    </div>

    <!-- Predicción (placeholder) -->
    <div
      v-if="alumno"
      class="bg-indigo-50 border-2 border-dashed border-indigo-300 rounded-2xl p-6 text-center"
    >
      <h4 class="text-lg font-semibold text-indigo-700 mb-2">
        🔮 Predicción de Deserción
      </h4>
      <p class="text-indigo-600">
        Este bloque se activará cuando integremos el modelo predictivo.
      </p>
    </div>
  </div>
</template>
