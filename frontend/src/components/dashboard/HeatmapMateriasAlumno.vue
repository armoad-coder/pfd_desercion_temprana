<template>
  <div class="w-full bg-white p-6 rounded-lg shadow-md border border-gray-100">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-bold text-gray-800">
        Mapa de Rendimiento Académico
      </h3>
      <div class="flex gap-2 text-xs text-gray-500">
        <span class="flex items-center"
          ><div class="w-2 h-2 bg-red-500 rounded-full mr-1"></div>
          1</span
        >
        <span class="flex items-center"
          ><div class="w-2 h-2 bg-yellow-400 rounded-full mr-1"></div>
          3</span
        >
        <span class="flex items-center"
          ><div class="w-2 h-2 bg-emerald-700 rounded-full mr-1"></div>
          5</span
        >
      </div>
    </div>

    <div v-if="loading" class="text-center py-20 text-gray-500">
      <div
        class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto mb-2"
      ></div>
      Cargando notas...
    </div>

    <div
      v-else-if="processedSubjects.length === 0"
      class="text-center py-10 text-gray-500 bg-gray-50 rounded-lg border border-dashed border-gray-300"
    >
      No hay materias registradas para este alumno.
    </div>

    <div v-else>
      <div
        class="grid grid-cols-2 md:grid-cols-5 lg:grid-cols-8 xl:grid-cols-10 gap-2 mb-6"
      >
        <div
          v-for="(subject, index) in paginatedSubjects"
          :key="index"
          class="flex flex-col items-center justify-center p-2 rounded-md text-white text-center transition-transform hover:scale-105 hover:shadow-lg cursor-default h-20 shadow-sm relative overflow-hidden group"
          :class="getGradeColor(subject.grade)"
          :title="subject.name + ': ' + subject.grade"
        >
          <span
            class="text-[0.65rem] font-medium uppercase leading-tight mb-1 line-clamp-2 px-1 w-full"
          >
            {{ formatName(subject.name) }}
          </span>

          <span class="text-lg font-bold">
            {{ subject.grade }}
          </span>

          <div
            class="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity"
          ></div>
        </div>
      </div>

      <div
        v-if="totalPages > 1"
        class="flex items-center justify-between border-t border-gray-200 pt-4"
      >
        <span class="text-xs text-gray-500">
          Viendo {{ pageStart + 1 }}-{{
            Math.min(pageEnd, processedSubjects.length)
          }}
          de {{ processedSubjects.length }}
        </span>

        <div class="inline-flex rounded-md shadow-sm h-8">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="px-3 bg-white border border-gray-300 rounded-l-md text-xs font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Anterior
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="px-3 bg-white border border-gray-300 rounded-r-md text-xs font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  materiasRaw: {
    type: Object,
    default: () => ({}),
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

// AQUI ESTA EL CAMBIO CLAVE: 90 items por página
const itemsPerPage = 90;
const currentPage = ref(1);

const processedSubjects = computed(() => {
  if (!props.materiasRaw) return [];

  // Convertimos a array y ordenamos por defecto (se puede cambiar orden aquí)
  // Tip: Ordenar por SEMESTRE sería ideal si tienes ese dato, sino alfabético está bien.
  return Object.entries(props.materiasRaw)
    .map(([name, grade]) => ({
      name: name,
      grade: parseFloat(grade),
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
});

const totalPages = computed(() =>
  Math.ceil(processedSubjects.value.length / itemsPerPage)
);
const pageStart = computed(() => (currentPage.value - 1) * itemsPerPage);
const pageEnd = computed(() => currentPage.value * itemsPerPage);

const paginatedSubjects = computed(() => {
  return processedSubjects.value.slice(pageStart.value, pageEnd.value);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

watch(
  () => props.materiasRaw,
  () => {
    currentPage.value = 1;
  }
);

// Colores ajustados para contraste en celdas más pequeñas
const getGradeColor = (grade) => {
  if (grade === 1) return "bg-red-500 border-red-600";
  if (grade > 1 && grade < 3) return "bg-orange-400 border-orange-500";
  if (grade >= 3 && grade < 4)
    return "bg-yellow-400 text-gray-900 border-yellow-500"; // Texto oscuro para contraste en amarillo
  if (grade >= 4 && grade < 5) return "bg-emerald-500 border-emerald-600";
  if (grade === 5) return "bg-emerald-700 border-emerald-800";
  return "bg-slate-300";
};

// Abreviar nombres muy largos automáticamente para que quepan
const formatName = (name) => {
  let clean = name.replace(/_/g, " ").toLowerCase();

  // Abreviaciones comunes
  clean = clean
    .replace("lenguaje de programacion", "leng. prog.")
    .replace("laboratorio", "lab.")
    .replace("ingenieria", "ing.")
    .replace("investigacion", "invest.")
    .replace("administracion", "admin.");

  return clean.replace(/\b\w/g, (l) => l.toUpperCase());
};
</script>
