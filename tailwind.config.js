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
          DEFAULT: '#D97757', // Terra Cotta
          light: '#F2A085',
          dark: '#B55A3B',
        },
        secondary: {
          DEFAULT: '#5E6A75', // Slate Grey
          light: '#8898AA',
          dark: '#3A4249',
        },
        accent: {
          DEFAULT: '#B89B6D', // Gold/Sand
          light: '#D4B483',
          dark: '#9C8259',
        },
        bg: {
          DEFAULT: '#FFFFFF', // White
          lighter: '#F9FAFB',
          darker: '#F5F5F7',
        },
        surface: '#FFFFFF',
        text: {
          primary: '#1A1A1E',
          secondary: '#5E6A75',
          light: '#8898AA',
        }
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
