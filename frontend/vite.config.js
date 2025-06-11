import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy any /api/* calls in dev to FastAPI on :8000
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false
      }
    }
  }
});
