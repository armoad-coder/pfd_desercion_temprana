<script setup>
import { ref, onMounted, watch, nextTick, onBeforeUnmount } from "vue";
import axios from "axios";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const canvasRef = ref(null);
let chartInstance = null;

// CAMBIO 1: Reordenamos para que "Compuesto" sea el primero en la lista visual
const carreras = [
  { key: "compuesto", label: "Gráfico Compuesto (Comparativo)" },
  { key: "informatica", label: "Ingeniería Informática" },
  { key: "electronica", label: "Ingeniería Electrónica" },
  { key: "electricidad", label: "Ingeniería Electricidad" },
  { key: "civil", label: "Ingeniería Civil" },
];

// CAMBIO 2: Seleccionamos "compuesto" por defecto al iniciar
const carreraSeleccionada = ref("compuesto");
const dataPorCarrera = ref({});

const SINGLE_COLORS = ["#be123c", "#e11d48", "#f43f5e", "#fb7185", "#fda4af"];
const COMPOUND_COLORS = {
  informatica: "#4f46e5",
  electronica: "#06b6d4",
  electricidad: "#f59e0b",
  civil: "#78716c",
};

function formatearNombre(texto) {
  if (!texto) return "";
  return texto
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

async function cargarDatos() {
  try {
    // const res = await axios.get("/dashboard/top-aplazos-por-carrera");
    // dataPorCarrera.value = res.data;

    await new Promise((r) => setTimeout(r, 100));

    dataPorCarrera.value = {
      // Asumimos que el backend ahora devuelve porcentajes o tratamos estos números como tal
      informatica: [
        { materia: "calculo_ii", aplazos: 45 },
        { materia: "fisica_i", aplazos: 38 },
        { materia: "algoritmos", aplazos: 30 },
        { materia: "estadistica", aplazos: 22 },
        { materia: "logica", aplazos: 15 },
      ],
      electronica: [
        { materia: "circuitos_electricos", aplazos: 42 },
        { materia: "teoria_electromagnetica", aplazos: 35 },
        { materia: "senales_y_sistemas", aplazos: 28 },
        { materia: "electronica_digital", aplazos: 20 },
        { materia: "fisica_iii", aplazos: 18 },
      ],
      electricidad: [
        { materia: "maquinas_electricas", aplazos: 50 },
        { materia: "sistemas_de_potencia", aplazos: 45 },
        { materia: "circuitos_iii", aplazos: 30 },
        { materia: "instalaciones", aplazos: 25 },
        { materia: "termodinamica", aplazos: 20 },
      ],
      civil: [
        { materia: "resistencia_de_materiales", aplazos: 55 },
        { materia: "hidraulica", aplazos: 48 },
        { materia: "estructuras_isostaticas", aplazos: 40 },
        { materia: "mecanica_de_suelos", aplazos: 32 },
        { materia: "topografia", aplazos: 25 },
      ],
      compuesto: {
        labels: ["calculo_i", "fisica_i", "probabilidad_y_estadistica"],
        datasets: [
          { label: "Informática", data: [45, 30, 25], key: "informatica" },
          { label: "Electrónica", data: [38, 42, 20], key: "electronica" },
          { label: "Electricidad", data: [50, 35, 15], key: "electricidad" },
          { label: "Civil", data: [60, 28, 40], key: "civil" },
        ],
      },
    };
  } catch (error) {
    console.error("Error cargando datos:", error);
  }
}

function renderChart() {
  if (chartInstance) chartInstance.destroy();

  const isComposite = carreraSeleccionada.value === "compuesto";
  let config = {};

  if (isComposite) {
    const rawData = dataPorCarrera.value.compuesto;
    config = {
      type: "bar",
      data: {
        labels: rawData.labels.map((l) => formatearNombre(l)),
        datasets: rawData.datasets.map((ds) => ({
          label: ds.label,
          data: ds.data,
          backgroundColor: COMPOUND_COLORS[ds.key],
          borderRadius: 4,
          borderSkipped: false,
          barPercentage: 0.7,
          categoryPercentage: 0.8,
        })),
      },
      options: {
        indexAxis: "x",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: "top",
            align: "end",
            labels: { usePointStyle: true, boxWidth: 8, font: { size: 11 } },
          },
          tooltip: {
            mode: "index",
            intersect: false,
            backgroundColor: "#fff",
            titleColor: "#1e293b",
            bodyColor: "#64748b",
            borderColor: "#e2e8f0",
            borderWidth: 1,
            titleFont: { weight: "bold" },
            callbacks: {
              // CAMBIO 3: Formato % en Tooltip Compuesto
              label: (context) => {
                let label = context.dataset.label || "";
                if (label) {
                  label += ": ";
                }
                if (context.parsed.y !== null) {
                  label += context.parsed.y + "%"; // Agregamos %
                }
                return label;
              },
            },
          },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#64748b", font: { weight: 600 } },
          },
          y: {
            beginAtZero: true,
            max: 100, // Opcional: Si son porcentajes, forzar tope a 100 se ve bien
            grid: { color: "#f1f5f9", borderDash: [5, 5] },
            ticks: {
              // CAMBIO 4: Formato % en Eje Y (Vertical)
              callback: function (value) {
                return value + "%";
              },
              color: "#94a3b8",
            },
          },
        },
      },
    };
  } else {
    const data = dataPorCarrera.value[carreraSeleccionada.value] || [];
    const labels = data.map((d) => formatearNombre(d.materia));
    const values = data.map((d) => d.aplazos);

    config = {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Indice de Reprobación", // Cambiamos etiqueta
            data: values,
            backgroundColor: SINGLE_COLORS.slice(0, values.length),
            borderRadius: 6,
            borderSkipped: false,
            barThickness: 24,
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { right: 20 } },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#fff",
            titleColor: "#1e293b",
            bodyColor: "#64748b",
            borderColor: "#e2e8f0",
            borderWidth: 1,
            padding: 12,
            callbacks: {
              // CAMBIO 5: Formato % en Tooltip Individual
              label: (ctx) => ` ${ctx.parsed.x}% Reprobados`,
            },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            max: 100, // Opcional: Tope 100
            grid: { color: "#f1f5f9", borderDash: [5, 5] },
            ticks: {
              // CAMBIO 6: Formato % en Eje X (Horizontal)
              color: "#94a3b8",
              callback: function (value) {
                return value + "%";
              },
            },
          },
          y: {
            grid: { display: false },
            ticks: { color: "#334155", font: { weight: 600 } },
          },
        },
      },
    };
  }

  chartInstance = new Chart(canvasRef.value, config);
}

onMounted(async () => {
  await cargarDatos();
  await nextTick();
  renderChart();
});

watch(carreraSeleccionada, async () => {
  await nextTick();
  renderChart();
});

onBeforeUnmount(() => {
  chartInstance?.destroy();
});
</script>

<template>
  <div
    class="w-full bg-white rounded-2xl p-6 shadow-xl shadow-slate-200/60 border border-slate-100"
  >
    <div
      class="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-4"
    >
      <div>
        <h2 class="text-xl font-bold text-slate-800 tracking-tight">
          Tasa de Reprobación
        </h2>
        <p class="text-sm text-slate-500 mt-1">
          {{
            carreraSeleccionada === "compuesto"
              ? "Comparativa porcentual entre carreras"
              : "Top 5 asignaturas con mayor porcentaje de fallo"
          }}
        </p>
      </div>

      <div class="relative min-w-[240px]">
        <select
          v-model="carreraSeleccionada"
          class="appearance-none w-full bg-slate-50 border border-slate-200 text-slate-700 font-medium py-2.5 pl-4 pr-10 rounded-xl cursor-pointer transition-all duration-200 outline-none hover:bg-slate-100 focus:bg-white focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500"
        >
          <option v-for="c in carreras" :key="c.key" :value="c.key">
            {{ c.label }}
          </option>
        </select>

        <div
          class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-500"
        >
          <svg
            class="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </div>
      </div>
    </div>

    <div class="relative w-full h-80">
      <canvas ref="canvasRef"></canvas>
    </div>
  </div>
</template>
