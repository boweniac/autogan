/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        APP_NAME: "AI 博闻",
        GATE_WAY_PROTOCOL: "http://",
        GATE_WAY_HOST: "192.168.0.103",
        GATE_WAY_PORT: "60302"
        // GATE_WAY_PROTOCOL: "http://",
        // GATE_WAY_HOST: "192.168.50.84",
        // GATE_WAY_PORT: "60302"
        // GATE_WAY_PROTOCOL: "https://",
        // GATE_WAY_HOST: "nas.boweniac.top",
        // GATE_WAY_PORT: "44403"
    },
}

module.exports = nextConfig
