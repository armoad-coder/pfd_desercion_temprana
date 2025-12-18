<template>
  <div class="bg-white p-4 rounded-2xl shadow h-full flex flex-col">
    <h3 class="text-lg font-semibold text-slate-800 mb-4 text-center">
      🎯 Perfil de Habilidades
    </h3>

    <div class="flex-1 relative min-h-[250px]">
      <Radar v-if="chartData" :data="chartData" :options="chartOptions" />
      <div
        v-else
        class="flex items-center justify-center h-full text-slate-400"
      >
        Faltan datos para generar el perfil
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { Radar } from "vue-chartjs";

// Registramos los componentes necesarios de Chart.js
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const props = defineProps({
  materias: {
    type: Object,
    default: () => ({}),
  },
});

// === CONFIGURACIÓN DE GRUPOS ===
// Agrupamos las materias del CSV en categorías lógicas
const groups = {
  "Programación y Soft.": [
    "INFORMATICA I",
    "COMPUTACION I",
    "COMPUTACION II",
    "COMPUTACION III",
    "LENGUAJE DE PROGRAMACION I",
    "LENGUAJE DE PROGRAMACION II",
    "LENGUAJES DE PROGRAMACION III",
    "LENGUAJE DE PROGRAMACION IV",
    "ESTRUCTURA DE DATOS I",
    "BASES DE DATOS I",
    "BASES DE DATOS II",
    "INGENIERIA DE SOFTWARE I",
    "DISENO DE SISTEMA INFORMATICO I",
  ],
  "Ciencias Básicas": [
    "CALCULO I",
    "CALCULO II",
    "CALCULO III",
    "ALGEBRA I",
    "ALGEBRA II",
    "FISICA I",
    "FISICA II",
    "FISICA III",
    "GEOMETRIA ANALITICA Y VECTORIAL",
    "MATEMATICA APLICADA",
    "PROBABILIDADES Y ESTADISTICAS",
    "METODOS NUMERICOS",
    "QUIMICA",
  ],
  "Hardware y Redes": [
    "ELECTRONICA I",
    "REDES DE COMPUTADORAS I",
    "REDES DE COMPUTADORAS II",
    "SISTEMAS OPERATIVOS I",
    "SISTEMAS OPERATIVOS II",
    "TALLER DE HARDWARE I",
    "TALLER DE HARDWARE II",
    "DISENO TECNICO",
  ],
  "Gestión y Humanidades": [
    "ADMINISTRACION Y MERCADOTECNIA",
    "CONTABILIDAD I",
    "EMPRENDEDORISMO",
    "DERECHO INTELECTUAL Y LABORAL",
    "ETICA PROFESIONAL",
    "METODOLOGIA DE LA INVESTIGACION I",
    "INVESTIGACION DE OPERACIONES I",
    "INGLES I",
    "INGLES II",
    "INGLES III",
    "IDIOMAS I",
    "EXPRESION ORAL Y ESCRITA",
  ],
};

// === CÁLCULO DE PROMEDIOS POR GRUPO ===
const categoryScores = computed(() => {
  const scores = [];

  for (const [category, subjects] of Object.entries(groups)) {
    let sum = 0;
    let count = 0;

    subjects.forEach((sub) => {
      // Normalizamos nombres (por si acaso espacios extras) y buscamos en props
      // Tu API devuelve keys exactas, así que buscamos directo
      const grade = props.materias[sub];
      if (grade !== undefined && grade !== null) {
        sum += parseFloat(grade);
        count++;
      }
    });

    // Si no tiene materias cursadas en esa área, dejamos 0 o null
    scores.push(count > 0 ? (sum / count).toFixed(2) : 0);
  }
  return scores;
});

// === DATA PARA CHART.JS ===
const chartData = computed(() => {
  return {
    labels: Object.keys(groups),
    datasets: [
      {
        label: "Promedio por Área",
        backgroundColor: "rgba(79, 70, 229, 0.2)", // Indigo con transparencia
        borderColor: "rgba(79, 70, 229, 1)", // Indigo sólido
        pointBackgroundColor: "rgba(79, 70, 229, 1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(79, 70, 229, 1)",
        data: categoryScores.value,
      },
    ],
  };
});

// === OPCIONES VISUALES ===
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      angleLines: { color: "#e2e8f0" }, // Color lineas radiales
      grid: { color: "#e2e8f0" }, // Color red circular
      pointLabels: {
        font: { size: 11, weight: "bold" },
        color: "#475569", // Slate-600
      },
      suggestedMin: 0,
      suggestedMax: 5, // Escala fija de 0 a 5
      ticks: {
        stepSize: 1,
        backdropColor: "transparent", // Quitar fondo blanco de los números
      },
    },
  },
  plugins: {
    legend: { display: false }, // Ocultamos leyenda porque es un solo dataset
  },
};
</script>
