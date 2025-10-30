/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{css,js}",
    "../../templates/**/*.{html,js}",
    "../../home/templates/**/*.{html,js}",
    "../../users/templates/**/*.{html,js}",
    "../../labsites/templates/**/*.{html,js}",
    "../../worksites/templates/**/*.{html,js}",
    "../../**/*.py"
  ],
  safelist: [
    'flex-[1]',
    'flex-[2]',
    'flex-[3]',
    'flex-[4]',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
