import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  
  // Adicione esta parte:
  webpack: (config) => {
    config.watchOptions = {
      poll: 1000,   // Verifica mudanças a cada 1000ms (1 segundo)
      aggregateTimeout: 300,
    }
    return config
  },
};

export default nextConfig;