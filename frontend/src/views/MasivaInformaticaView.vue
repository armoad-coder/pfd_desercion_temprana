<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">
      Carga Masiva - Ingeniería Informática
    </h1>

    <!-- Dropzone -->
    <label
      class="w-full p-10 border-2 border-dashed border-gray-400 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:bg-gray-100 transition"
    >
      <input type="file" class="hidden" @change="onFileSelected" />
      <span class="text-gray-600 text-lg">
        Arrastra un archivo o haz clic para seleccionar
      </span>
      <span v-if="fileName" class="mt-2 text-blue-700 font-semibold">
        Archivo seleccionado: {{ fileName }}
      </span>
    </label>

    <!-- Botón subir -->
    <button
      class="mt-6 bg-blue-700 hover:bg-blue-800 text-white px-6 py-2 rounded shadow"
      :disabled="!file"
      @click="uploadFile"
    >
      Subir archivo
    </button>

    <!-- Resultado -->
    <div v-if="result" class="mt-6 bg-gray-200 p-4 rounded shadow">
      <h2 class="text-lg font-bold">Resultado:</h2>
      <p>Registros creados: {{ result.creados }}</p>
      <p>Registros actualizados: {{ result.actualizados }}</p>
    </div>

    <!-- Error -->
    <div v-if="error" class="mt-6 bg-red-600 text-white p-4 rounded shadow">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "@/api/api";

const file = ref(null);
const fileName = ref("");
const result = ref(null);
const error = ref("");

const onFileSelected = (event) => {
  file.value = event.target.files[0];
  fileName.value = file.value?.name || "";
};

const uploadFile = async () => {
  try {
    error.value = "";
    result.value = null;

    const formData = new FormData();
    formData.append("file", file.value);

    const response = await api.post(
      "/datos/informatica/carga_masiva",
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );

    result.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.error || "Error al procesar el archivo.";
  }
};
</script>
