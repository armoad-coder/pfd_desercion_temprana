<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const canvasRef = ref(null);
let chartInstance = null;

onMounted(async () => {
  await nextTick();

  // 🔢 Datos reales (luego vendrán del backend)
  const labels = [
    "Ingeniería Informática",
    "Ingeniería Electrónica",
    "Ingeniería Electricidad",
    "Ingeniería Civil",
  ];

  const alumnos = [145, 86, 255, 159];
  const total = alumnos.reduce((a, b) => a + b, 0);

  const porcentajes = alumnos.map((v) => ((v / total) * 100).toFixed(1));

  chartInstance = new Chart(canvasRef.value, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: porcentajes,
          backgroundColor: [
            "#4f46e5", // informática
            "#06b6d4", // electrónica
            "#f59e0b", // electricidad
            "#78716c", // civil
          ],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "75%", // 🔥 dona más fina y moderna
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            font: { size: 13 },
            padding: 16,
            generateLabels(chart) {
              const data = chart.data;
              return data.labels.map((label, i) => ({
                text: `${label} — ${data.datasets[0].data[i]}%`,
                fillStyle: data.datasets[0].backgroundColor[i],
                strokeStyle: data.datasets[0].backgroundColor[i],
                index: i,
              }));
            },
          },
        },
        tooltip: {
          callbacks: {
            label: (context) =>
              `${context.label}: ${context.parsed}% del total`,
          },
        },
      },
    },
  });
});

onBeforeUnmount(() => {
  chartInstance?.destroy();
});
</script>

<template>
  <div class="relative w-full h-64">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>
