/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        subida: "#16a34a",
        descida: "#dc2626",
        neutro: "#64748b",
      },
    },
  },
  plugins: [],
};
