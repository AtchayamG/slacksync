import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Relative base so the production bundle works both at a domain root and from a
// GitHub Pages project subpath (https://<user>.github.io/slacksync/).
export default defineConfig({
  base: "./",
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5174
  }
});
