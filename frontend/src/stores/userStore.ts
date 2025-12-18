import { defineStore } from "pinia";

interface User {
  id: number;
  email: string;
  nombre: string | null;
  apellido: string | null;
}

interface UserState {
  token: string | null;
  user: User | null;
}

export const useUserStore = defineStore("userStore", {
  state: (): UserState => ({
    token: localStorage.getItem("token"),
    user: localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user") as string)
      : null,
  }),

  actions: {
    login(token: string, user: User) {
      this.token = token;
      this.user = user;

      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
    },

    logout() {
      this.token = null;
      this.user = null;

      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
  },
});
