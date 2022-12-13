/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/src/**/*.js"],
  theme: {
    extend: {
      backgroundColor: {
        brand: "#2563EB",
        "brand-dark": "#1E3A8A",
        "brand-light": "#BFDBFE",
      },
      colors: {
        accent: "#FDE047",
        "accent-dark": "#CA8A04",
      },
      outlineColor: {
        brand: "#2563EB",
      },
    },
  },
  plugins: [],
};
