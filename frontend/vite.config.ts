import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(), // Tailwind 4
  ],

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/dashboard": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});
