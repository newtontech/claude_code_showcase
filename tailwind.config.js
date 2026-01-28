/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#ff4800',
        secondary: '#00f0ff',
        accent: '#ff00ff',
        bg: '#080808',
      },
      fontFamily: {
        display: ['Orbitron', 'sans-serif'],
        body: ['Outfit', 'sans-serif'],
        code: ['JetBrains Mono', 'monospace'],
      },
      keyframes: {
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
      animation: {
        marquee: 'marquee 20s linear infinite',
      },
    },
  },
  plugins: [],
}
