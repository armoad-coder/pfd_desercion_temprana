<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const cards = ref([
  {
    id: 1,
    key: "civil",
    title: "Ingeniería Civil",
    description: "Planificación de infraestructuras y gestión de obras.",
    category: "Construcción",
    color: "bg-stone-500",
    dotColor: "bg-stone-400",
    students: null,
    subjects: null,
  },
  {
    id: 2,
    key: "electronica",
    title: "Ingeniería Electrónica",
    description: "Diseño de circuitos y sistemas embebidos.",
    category: "Hardware",
    color: "bg-cyan-600",
    dotColor: "bg-cyan-500",
    students: null,
    subjects: null,
  },
  {
    id: 3,
    key: "informatica",
    title: "Ingeniería Informática",
    description: "Desarrollo de software y arquitectura de sistemas.",
    category: "Software",
    color: "bg-indigo-600",
    dotColor: "bg-indigo-500",
    students: null,
    subjects: null,
  },
  {
    id: 4,
    key: "electricidad",
    title: "Ingeniería Electricidad",
    description: "Sistemas de potencia y redes de distribución.",
    category: "Energía",
    color: "bg-amber-500",
    dotColor: "bg-amber-400",
    students: null,
    subjects: null,
  },
]);

onMounted(async () => {
  try {
    const res = await axios.get("http://localhost:5000/dashboard/data");
    const data = res.data;

    // Asignar valores reales a cada card
    cards.value.forEach((card) => {
      const carreraData = data[card.key];
      if (carreraData) {
        card.students = carreraData.alumnos;
        card.subjects = carreraData.materias;
      }
    });
  } catch (error) {
    console.error("Error cargando datos de dashboard:", error);
  }
});
</script>

<template>
  <div class="p-6">
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      <div
        v-for="card in cards"
        :key="card.id"
        class="group relative flex flex-col justify-between bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 overflow-hidden"
      >
        <div :class="`h-2 w-full ${card.color}`"></div>

        <div class="p-5 flex-grow">
          <span
            class="inline-block px-3 py-1 mb-3 text-xs font-semibold tracking-wider text-slate-500 uppercase bg-slate-100 rounded-full dark:bg-slate-700 dark:text-slate-300"
          >
            {{ card.category }}
          </span>

          <h3
            class="text-xl font-bold text-slate-800 dark:text-white mb-2 group-hover:text-indigo-600 transition-colors"
          >
            {{ card.title }}
          </h3>

          <p
            class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed mb-4"
          >
            {{ card.description }}
          </p>

          <div
            class="bg-slate-50 dark:bg-slate-700/30 rounded-lg p-3 border border-slate-100 dark:border-slate-700"
          >
            <ul class="space-y-2">
              <li class="flex items-center justify-between text-sm">
                <div
                  class="flex items-center text-slate-600 dark:text-slate-300"
                >
                  <span
                    :class="`w-2 h-2 rounded-full mr-2 ${card.dotColor}`"
                  ></span>
                  Cantidad de Alumnos:
                </div>
                <span class="font-bold text-slate-800 dark:text-white">
                  {{ card.students ?? "..." }}
                </span>
              </li>

              <li
                class="border-t border-slate-200 dark:border-slate-600 border-dashed"
              ></li>

              <li class="flex items-center justify-between text-sm">
                <div
                  class="flex items-center text-slate-600 dark:text-slate-300"
                >
                  <span
                    :class="`w-2 h-2 rounded-full mr-2 ${card.dotColor}`"
                  ></span>
                  Cantidad de Materias:
                </div>
                <span class="font-bold text-slate-800 dark:text-white">
                  {{ card.subjects ?? "..." }}
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div class="p-5 pt-0 mt-auto">
          <button
            class="w-full py-2 px-4 bg-transparent border border-indigo-600 text-indigo-600 rounded-lg hover:bg-indigo-600 hover:text-white font-medium transition-colors duration-200 cursor-pointer"
          >
            Ver Malla Curricular
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
