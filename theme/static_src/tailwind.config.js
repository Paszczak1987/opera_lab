/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{css,js}",
    "../../templates/**/*.{html,js}",
    "../../home/templates/**/*.{html,js}",
    "../../users/templates/**/*.{html,js}",
    "../../**/*.py"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
