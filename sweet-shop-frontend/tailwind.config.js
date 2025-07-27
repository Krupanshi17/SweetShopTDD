/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        lobster: ['Lobster', 'cursive'],
      },
      colors: {
        primaryDark: '#000000',
        accentCTA: '#CFFFE2',
        secondary: '#A2D5C6',
        background: '#F6F6F6',
      },
    },
  },
  plugins: [],
}
