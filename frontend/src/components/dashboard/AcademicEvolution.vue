<template>
  <div class="bg-white p-4 rounded-2xl shadow h-full flex flex-col">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold text-slate-800">
        📈 Evolución Semestral Real
      </h3>
      <span
        class="text-xs font-bold px-2 py-1 rounded"
        :class="trendStatus.color"
      >
        {{ trendStatus.text }}
      </span>
    </div>

    <div class="flex-1 relative min-h-[250px]">
      <Line v-if="chartData" :data="chartData" :options="chartOptions" />
      <div
        v-else
        class="flex items-center justify-center h-full text-slate-400"
      >
        Insuficientes datos para calcular tendencia
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const props = defineProps({
  materias: {
    type: Object,
    default: () => ({}),
  },
});

// ==========================================
// 1. MALLA CURRICULAR OFICIAL
// ==========================================
const SEMESTRES_OFICIALES = {
  "1er Semestre": [
    "COMPUTACION I",
    "ELECTRONICA I",
    "FISICA I",
    "ALGEBRA I",
    "CALCULO I",
    "GEOMETRIA ANALITICA Y VECTORIAL",
    "DISENO TECNICO",
    "QUIMICA",
    "INGLES I",
    "EVENTOS Y DEPORTES I",
  ],
  "2do Semestre": [
    "COMPUTACION II",
    "INFORMATICA I",
    "LABORATORIO I",
    "FISICA II",
    "CALCULO II",
    "ALGEBRA II",
    "ADMINISTRACION Y MERCADOTECNIA",
    "INGLES II",
    "EVENTOS Y DEPORTES II",
  ],
  "3er Semestre": [
    "ESTRUCTURA DE DATOS I",
    "LENGUAJE DE PROGRAMACION I",
    "COMPUTACION III",
    "FISICA III",
    "PROBABILIDADES Y ESTADISTICAS",
    "CALCULO III",
    "METODOLOGIA DE LA INVESTIGACION I",
    "EXPRESION ORAL Y ESCRITA",
    "EVENTOS Y DEPORTES III",
  ],
  "4to Semestre": [
    "BASES DE DATOS I",
    "DISENO DE SISTEMA INFORMATICO I",
    "LENGUAJE DE PROGRAMACION II",
    "TALLER DE HARDWARE I",
    "CONTABILIDAD I",
    "DERECHO INTELECTUAL Y LABORAL",
    "EMPRENDEDORISMO",
    "INGLES III",
    "EVENTOS Y DEPORTES IV",
  ],
  "5to Semestre": [
    "INGENIERIA DE SOFTWARE I",
    "INVESTIGACION DE OPERACIONES I",
    "LENGUAJES DE PROGRAMACION III",
    "REDES DE COMPUTADORAS I",
    "SISTEMAS OPERATIVOS I",
    "TALLER DE HARDWARE II",
    "MATEMATICA APLICADA",
    "IDIOMAS I",
    "EVENTOS Y DEPORTES V",
  ],
  "6to Semestre": [
    "BASES DE DATOS II",
    "ESTRUCTURAS DE LOS LENGUAJES",
    "LENGUAJE DE PROGRAMACION IV",
    "REDES DE COMPUTADORAS II",
    "SISTEMAS OPERATIVOS II",
    "METODOS NUMERICOS",
    "ETICA PROFESIONAL",
    "LABORATORIO DE IDIOMAS I",
    "EVENTOS Y DEPORTES VI",
  ],
};

// ==========================================
// 2. BUSCADOR DE NOTAS INTELIGENTE
// ==========================================
// Como el JSON del backend usa claves específicas (ej: SIN acentos),
// esta función ayuda a encontrar la materia aunque haya pequeñas diferencias de texto.
const findGrade = (subjectName) => {
  if (!props.materias) return null;

  // 1. Intento directo (Exact Match)
  let val = props.materias[subjectName];
  if (val !== undefined && val !== null) return parseFloat(val);

  // 2. Intento normalizado (Quitar Ñ, Acentos, Plurales conflictivos)
  // Ej: Convertir "DISEÑO" a "DISENO" o "BASES" a "BASE"
  const normalize = (str) =>
    str
      .toUpperCase()
      .replace(/Ñ/g, "N")
      .replace(/Á/g, "A")
      .replace(/É/g, "E")
      .replace(/Í/g, "I")
      .replace(/Ó/g, "O")
      .replace(/Ú/g, "U")
      .replace("BASE DE DATOS", "BASES DE DATOS") // Corrección especifica plural/singular
      .replace("LENGUAJES DE", "LENGUAJE DE"); // Corrección especifica plural/singular

  // Buscamos en las keys del backend cuál coincide con nuestra versión normalizada
  const cleanSubject = normalize(subjectName);

  const backendKey = Object.keys(props.materias).find(
    (k) => normalize(k) === cleanSubject
  );

  if (backendKey) {
    val = props.materias[backendKey];
    if (val !== undefined && val !== null) return parseFloat(val);
  }

  return null;
};

// ==========================================
// 3. CÁLCULO DE DATOS
// ==========================================
const evolutionData = computed(() => {
  const dataPoints = [];

  for (const [semName, materiasList] of Object.entries(SEMESTRES_OFICIALES)) {
    let sum = 0;
    let count = 0;

    materiasList.forEach((materia) => {
      const grade = findGrade(materia);
      if (grade !== null) {
        sum += grade;
        count++;
      }
    });

    // Solo agregamos el semestre al gráfico si tiene al menos 1 materia cursada
    if (count > 0) {
      dataPoints.push({
        sem: semName.replace(" Semestre", ""), // "1er", "2do"... para ahorrar espacio
        avg: (sum / count).toFixed(2),
      });
    }
  }

  return dataPoints;
});

// Detectar tendencia
const trendStatus = computed(() => {
  const data = evolutionData.value;
  if (data.length < 2)
    return { text: "Datos insuficientes", color: "bg-gray-100 text-gray-500" };

  const last = parseFloat(data[data.length - 1].avg);
  const prev = parseFloat(data[data.length - 2].avg);

  // Umbral de 0.1 para considerar cambio
  if (last > prev + 0.1)
    return {
      text: "Tendencia Positiva ↗",
      color: "bg-green-100 text-green-700",
    };
  if (last < prev - 0.1)
    return { text: "Rendimiento en Baja ↘", color: "bg-red-100 text-red-700" };
  return { text: "Estable ➡", color: "bg-blue-100 text-blue-700" };
});

const chartData = computed(() => {
  // Si no hay datos, retornamos null para manejar el estado vacío en el template
  if (evolutionData.value.length === 0) return null;

  return {
    labels: evolutionData.value.map((d) => d.sem),
    datasets: [
      {
        label: "Promedio Semestral",
        backgroundColor: (context) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, "rgba(79, 70, 229, 0.5)");
          gradient.addColorStop(1, "rgba(79, 70, 229, 0.0)");
          return gradient;
        },
        borderColor: "#4f46e5",
        pointBackgroundColor: "#fff",
        pointBorderColor: "#4f46e5",
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        data: evolutionData.value.map((d) => d.avg),
        fill: true,
        tension: 0.3,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      min: 1,
      max: 5,
      grid: { borderDash: [4, 4], color: "#e2e8f0" },
      title: { display: true, text: "Nota Promedio" },
    },
    x: {
      grid: { display: false },
    },
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => `Promedio: ${context.raw}`,
      },
    },
  },
};
</script>
