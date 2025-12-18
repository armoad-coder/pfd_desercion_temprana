<template>
  <div class="p-4 md:p-6">
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-bold text-gray-800">
        Configuración de modelos de predicción
      </h1>
    </div>

    <!-- Mensajes -->
    <div
      v-if="errorMessage"
      class="mb-4 px-4 py-3 rounded bg-red-600 text-white text-sm"
    >
      {{ errorMessage }}
    </div>
    <div
      v-if="successMessage"
      class="mb-4 px-4 py-3 rounded bg-green-600 text-white text-sm"
    >
      {{ successMessage }}
    </div>

    <!-- Tabla -->
    <div
      class="bg-white rounded-lg shadow border border-gray-200 overflow-x-auto"
    >
      <table class="min-w-full text-sm">
        <thead class="bg-gray-100 border-b border-gray-200">
          <tr>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Carrera
            </th>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Algoritmo
            </th>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Archivo modelo (.joblib)
            </th>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Archivo scaler (.joblib)
            </th>
            <th
              class="text-right px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Acciones
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="5" class="px-4 py-4 text-center text-gray-500">
              Cargando configuración...
            </td>
          </tr>
          <tr v-else-if="configs.length === 0">
            <td colspan="5" class="px-4 py-4 text-center text-gray-500">
              No hay configuraciones registradas.
            </td>
          </tr>
          <tr
            v-for="cfg in configs"
            :key="cfg.career"
            class="border-t border-gray-100 hover:bg-gray-50"
          >
            <td class="px-4 py-2">
              {{ careerLabel(cfg.career) }}
            </td>
            <td class="px-4 py-2">
              {{ algorithmLabel(cfg.algorithm) }}
            </td>
            <td class="px-4 py-2 font-mono text-xs break-all">
              {{ cfg.model_file }}
            </td>
            <td class="px-4 py-2 font-mono text-xs break-all">
              {{ cfg.scaler_file }}
            </td>
            <td class="px-4 py-2 text-right">
              <button
                class="px-3 py-1.5 text-xs rounded-md border border-gray-300 hover:bg-gray-100"
                @click="openEditModal(cfg)"
              >
                Editar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL EDITAR CONFIGURACIÓN -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-40"
    >
      <div class="bg-white rounded-lg shadow-lg w-full max-w-lg p-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">
          Editar configuración – {{ selectedCareerLabel }}
        </h2>

        <div class="space-y-4">
          <!-- Algoritmo -->
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">
              Algoritmo
            </label>
            <select
              v-model="editForm.algorithm"
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring focus:ring-blue-200 focus:border-blue-500"
            >
              <option
                v-for="alg in availableAlgorithms"
                :key="alg.value"
                :value="alg.value"
              >
                {{ alg.label }}
              </option>
            </select>
          </div>

          <!-- Archivo modelo -->
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">
              Ruta archivo modelo (.joblib)
            </label>
            <input
              v-model="editForm.model_file"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring focus:ring-blue-200 focus:border-blue-500 font-mono"
            />
            <p class="mt-1 text-[11px] text-gray-500">
              Ejemplo: src/utils/modelos/modelo_knn_informatica.joblib
            </p>
          </div>

          <!-- Archivo scaler -->
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">
              Ruta archivo scaler (.joblib)
            </label>
            <input
              v-model="editForm.scaler_file"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring focus:ring-blue-200 focus:border-blue-500 font-mono"
            />
            <p class="mt-1 text-[11px] text-gray-500">
              Ejemplo: src/utils/scalers/scaler_informatica.joblib
            </p>
          </div>

          <div v-if="modalError" class="text-sm text-red-600">
            {{ modalError }}
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button
            class="px-3 py-1.5 text-sm rounded-md border border-gray-300 hover:bg-gray-100"
            @click="closeModal"
          >
            Cancelar
          </button>
          <button
            class="px-4 py-1.5 text-sm rounded-md bg-blue-600 text-white font-semibold hover:bg-blue-700"
            @click="saveConfig"
          >
            Guardar cambios
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import api from "@/api/api";

interface PredictionConfig {
  career: string;
  algorithm: string;
  model_file: string;
  scaler_file: string;
}

const configs = ref<PredictionConfig[]>([]);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

// Modal
const showModal = ref(false);
const selectedConfig = ref<PredictionConfig | null>(null);
const modalError = ref("");

const editForm = ref({
  career: "",
  algorithm: "",
  model_file: "",
  scaler_file: "",
});

// Algoritmos disponibles (etiqueta bonita + valor técnico)
const availableAlgorithms = [
  { value: "knn", label: "K-Nearest Neighbors (KNN)" },
  { value: "decision_tree", label: "Árbol de Decisión (DT)" },
  { value: "random_forest", label: "Random Forest" },
  { value: "logistic_regression", label: "Regresión Logística (RL)" },
  { value: "svm", label: "SVM" },
];

// ---- Utilidades de labels ----
const careerLabel = (career: string): string => {
  switch (career) {
    case "informatica":
      return "Ingeniería Informática";
    case "electricidad":
      return "Ingeniería Electricidad";
    case "civil":
      return "Ingeniería Civil";
    case "electronica":
      return "Ingeniería Electrónica";
    default:
      return career;
  }
};

const algorithmLabel = (algorithm: string): string => {
  const found = availableAlgorithms.find((a) => a.value === algorithm);
  return found ? found.label : algorithm;
};

const selectedCareerLabel = computed(() =>
  selectedConfig.value ? careerLabel(selectedConfig.value.career) : ""
);

// ---- Carga inicial ----
const fetchConfigs = async () => {
  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    const res = await api.get("/config/models"); // ajusta a /api/config/models si tu blueprint usa /api
    configs.value = res.data;
  } catch (err: any) {
    errorMessage.value =
      err?.response?.data?.error || "Error al cargar configuraciones.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchConfigs();
});

// ---- Modal edición ----
const openEditModal = (cfg: PredictionConfig) => {
  selectedConfig.value = { ...cfg };
  modalError.value = "";
  editForm.value = {
    career: cfg.career,
    algorithm: cfg.algorithm,
    model_file: cfg.model_file,
    scaler_file: cfg.scaler_file,
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  selectedConfig.value = null;
  modalError.value = "";
};

const saveConfig = async () => {
  if (!editForm.value.career) return;

  modalError.value = "";
  successMessage.value = "";

  try {
    const career = editForm.value.career;

    const payload = {
      algorithm: editForm.value.algorithm,
      model_file: editForm.value.model_file,
      scaler_file: editForm.value.scaler_file,
    };

    const res = await api.put(`/config/models/${career}`, payload);

    // Actualizar la lista local con lo que devolvió el backend
    const updated = res.data.config;
    const idx = configs.value.findIndex((c) => c.career === career);
    if (idx !== -1) {
      configs.value[idx] = updated;
    }

    successMessage.value = "Configuración actualizada correctamente.";
    showModal.value = false;
  } catch (err: any) {
    modalError.value =
      err?.response?.data?.error || "Error al guardar la configuración.";
  }
};
</script>
