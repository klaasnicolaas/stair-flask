/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../blueprints/**/*.html',
    './static/**/*.js',
    "./node_modules/flowbite/**/*.js",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          '50': '#f1f8fe',
          '100': '#e3eefb',
          '200': '#c0def7',
          '300': '#88c4f1',
          '400': '#48a6e8',
          '500': '#218ad6',
          '600': '#1269b0',
          '700': '#105794',
          '800': '#124b7a',
          '900': '#143f66',
          '950': '#0d2844',
        },
        secondary: {
          '50': '#effaff',
          '100': '#def5ff',
          '200': '#b6edff',
          '300': '#75e1ff',
          '400': '#2cd3ff',
          '500': '#00b6ed',
          '600': '#0099d4',
          '700': '#0079ab',
          '800': '#00668d',
          '900': '#065574',
          '950': '#04364d',
        },
        accent: {
          '50': '#fffbea',
          '100': '#fff3c5',
          '200': '#ffe687',
          '300': '#ffd448',
          '400': '#ffbf1e',
          '500': '#fc9d04',
          '600': '#ef7d00',
          '700': '#b95004',
          '800': '#963d0a',
          '900': '#7b330c',
          '950': '#471801',
        },
      }
    },
    fontFamily: {
      'body': [
        'Inter', 
        'ui-sans-serif', 
        'system-ui', 
        '-apple-system', 
        'system-ui', 
        'Segoe UI', 
        'Roboto', 
        'Helvetica Neue', 
        'Arial', 
        'Noto Sans', 
        'sans-serif', 
        'Apple Color Emoji', 
        'Segoe UI Emoji', 
        'Segoe UI Symbol', 
        'Noto Color Emoji'
      ],
      'sans': [
        'Inter', 
        'ui-sans-serif', 
        'system-ui', 
        '-apple-system', 
        'system-ui', 
        'Segoe UI', 
        'Roboto', 
        'Helvetica Neue', 
        'Arial', 
        'Noto Sans', 
        'sans-serif', 
        'Apple Color Emoji', 
        'Segoe UI Emoji', 
        'Segoe UI Symbol', 
        'Noto Color Emoji'
      ]
    },
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

