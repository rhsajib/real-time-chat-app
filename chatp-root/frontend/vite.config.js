import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],

    // this is for development
    server: {
        watch: {
            usePolling: true,
        },
        host: true, // needed for the Docker Container port mapping to work
        strictPort: true,
        port: 8080, // you can replace this port with any port
    },

    // this is for production
    // we need to define which port the project will run on when we execute npm run preview
    // host: true will expose the project in public address
    preview: {
        port: 8080, // you can replace this port with any port
        host: true, // needed for the Docker Container port mapping to work
    },
});
