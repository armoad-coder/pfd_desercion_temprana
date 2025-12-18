<template>
  <div class="p-4 md:p-6">
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-bold text-gray-800">Gestión de Usuarios</h1>

      <button
        class="px-4 py-2 rounded-md bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 shadow"
        @click="openCreateModal"
      >
        + Nuevo usuario
      </button>
    </div>

    <!-- Mensaje de error general -->
    <div
      v-if="errorMessage"
      class="mb-4 px-4 py-3 bg-red-600 text-white rounded"
    >
      {{ errorMessage }}
    </div>

    <!-- Tabla de usuarios -->
    <div
      class="bg-white rounded-lg shadow border border-gray-200 overflow-x-auto"
    >
      <table class="min-w-full text-sm">
        <thead class="bg-gray-100 border-b border-gray-200">
          <tr>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              ID
            </th>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Email
            </th>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Nombre
            </th>
            <th
              class="text-left px-4 py-2 text-xs font-semibold text-gray-600 uppercase"
            >
              Apellido
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
              Cargando usuarios...
            </td>
          </tr>
          <tr v-else-if="users.length === 0">
            <td colspan="5" class="px-4 py-4 text-center text-gray-500">
              No hay usuarios registrados.
            </td>
          </tr>
          <tr
            v-for="user in users"
            :key="user.id"
            class="border-t border-gray-100 hover:bg-gray-50"
          >
            <td class="px-4 py-2">{{ user.id }}</td>
            <td class="px-4 py-2">{{ user.email }}</td>
            <td class="px-4 py-2">{{ user.nombre }}</td>
            <td class="px-4 py-2">{{ user.apellido }}</td>
            <td class="px-4 py-2 text-right space-x-2">
              <button
                class="px-2 py-1 text-xs rounded-md border border-gray-300 hover:bg-gray-100"
                @click="openEditModal(user)"
              >
                Editar
              </button>
              <button
                class="px-2 py-1 text-xs rounded-md border border-yellow-500 text-yellow-700 hover:bg-yellow-50"
                @click="openResetModal(user)"
              >
                Reset pass
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL CREAR / EDITAR -->
    <div
      v-if="showFormModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-40"
    >
      <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">
          {{ isEditing ? "Editar usuario" : "Nuevo usuario" }}
        </h2>

        <div class="space-y-3">
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1"
              >Email</label
            >
            <input
              v-model="form.email"
              type="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200 focus:border-blue-500"
            />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1"
              >Nombre</label
            >
            <input
              v-model="form.nombre"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200 focus:border-blue-500"
            />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1"
              >Apellido</label
            >
            <input
              v-model="form.apellido"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200 focus:border-blue-500"
            />
          </div>

          <!-- Password solo en creación -->
          <div v-if="!isEditing">
            <label class="block text-xs font-medium text-gray-600 mb-1"
              >Contraseña</label
            >
            <input
              v-model="form.password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200 focus:border-blue-500"
            />
          </div>

          <div v-if="formError" class="text-sm text-red-600">
            {{ formError }}
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button
            class="px-3 py-1.5 text-sm rounded-md border border-gray-300 hover:bg-gray-100"
            @click="closeFormModal"
          >
            Cancelar
          </button>
          <button
            class="px-4 py-1.5 text-sm rounded-md bg-blue-600 text-white font-semibold hover:bg-blue-700"
            @click="submitForm"
          >
            {{ isEditing ? "Guardar cambios" : "Crear usuario" }}
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL RESET PASSWORD -->
    <div
      v-if="showResetModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-40"
    >
      <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">
          Resetear contraseña
        </h2>

        <p class="text-sm text-gray-600 mb-3">
          Usuario: <span class="font-semibold">{{ selectedUser?.email }}</span>
        </p>

        <div class="space-y-3">
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">
              Contraseña actual
            </label>
            <input
              v-model="resetForm.old_password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">
              Nueva contraseña
            </label>
            <input
              v-model="resetForm.new_password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">
              Repetir nueva contraseña
            </label>
            <input
              v-model="resetForm.reply_password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div v-if="resetError" class="text-sm text-red-600">
            {{ resetError }}
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button
            class="px-3 py-1.5 text-sm rounded-md border border-gray-300 hover:bg-gray-100"
            @click="closeResetModal"
          >
            Cancelar
          </button>
          <button
            class="px-4 py-1.5 text-sm rounded-md bg-yellow-500 text-white font-semibold hover:bg-yellow-600"
            @click="submitReset"
          >
            Resetear
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import api from "@/api/api";

interface User {
  id: number;
  email: string;
  nombre: string | null;
  apellido: string | null;
}

const users = ref<User[]>([]);
const loading = ref(false);
const errorMessage = ref("");

// Modal crear/editar
const showFormModal = ref(false);
const isEditing = ref(false);
const formError = ref("");
const form = ref({
  id: null as number | null,
  email: "",
  nombre: "",
  apellido: "",
  password: "",
});

// Reset password
const showResetModal = ref(false);
const resetError = ref("");
const resetForm = ref({
  old_password: "",
  new_password: "",
  reply_password: "",
});

const selectedUser = ref<User | null>(null);

// ----- Listar usuarios -----
const fetchUsers = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    const res = await api.get("/api/users/list");
    users.value = res.data;
  } catch (err: any) {
    errorMessage.value =
      err.response?.data?.error || "Error al cargar usuarios.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUsers();
});

// ----- Crear / Editar -----
const openCreateModal = () => {
  isEditing.value = false;
  formError.value = "";
  form.value = {
    id: null,
    email: "",
    nombre: "",
    apellido: "",
    password: "",
  };
  showFormModal.value = true;
};

const openEditModal = (user: User) => {
  isEditing.value = true;
  formError.value = "";
  form.value = {
    id: user.id,
    email: user.email,
    nombre: user.nombre || "",
    apellido: user.apellido || "",
    password: "",
  };
  showFormModal.value = true;
};

const closeFormModal = () => {
  showFormModal.value = false;
};

const submitForm = async () => {
  formError.value = "";

  try {
    if (isEditing.value && form.value.id !== null) {
      // UPDATE
      await api.put(`/api/users/update/${form.value.id}`, {
        email: form.value.email,
        nombre: form.value.nombre,
        apellido: form.value.apellido,
      });
    } else {
      // CREATE
      await api.post("/api/users/create", {
        email: form.value.email,
        nombre: form.value.nombre,
        apellido: form.value.apellido,
        password: form.value.password,
      });
    }

    showFormModal.value = false;
    await fetchUsers();
  } catch (err: any) {
    formError.value = err.response?.data?.error || "Error al guardar.";
  }
};

// ----- Reset password -----
const openResetModal = (user: User) => {
  selectedUser.value = user;
  resetError.value = "";
  resetForm.value = {
    old_password: "",
    new_password: "",
    reply_password: "",
  };
  showResetModal.value = true;
};

const closeResetModal = () => {
  showResetModal.value = false;
};

const submitReset = async () => {
  if (!selectedUser.value) return;

  resetError.value = "";

  try {
    await api.put(`/api/users/reset_password/${selectedUser.value.id}`, {
      old_password: resetForm.value.old_password,
      new_password: resetForm.value.new_password,
      reply_password: resetForm.value.reply_password,
    });

    showResetModal.value = false;
  } catch (err: any) {
    resetError.value =
      err.response?.data?.error || "Error al resetear contraseña.";
  }
};
</script>
