import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  // Do not regenerate AGENTS.md / CLAUDE.md on every dev start.
  agentRules: false,
};

export default nextConfig;
