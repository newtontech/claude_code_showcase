/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#D97757', // Anthropic-ish Terra Cotta
          light: '#F2A085',
          dark: '#B55A3B',
        },
        secondary: {
          DEFAULT: '#8898AA', // Cool Grey
          light: '#AAB8C8',
          dark: '#667585',
        },
        accent: {
          DEFAULT: '#D4B483', // Champagne
          light: '#E6C99C',
          dark: '#B89B6D',
        },
        bg: {
          DEFAULT: '#0D0D0F', // Deep Charcoal
          lighter: '#1A1A1E',
          darker: '#050506',
        },
        surface: '#1E1E21',
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
