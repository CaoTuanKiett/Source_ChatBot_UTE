/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    theme: {
        extend: {
            colors: {
                vue: '#42b883',
                'vue-shade': '#2E805B',
                'tk-primary-color': '#11212E',
                'tk-btn-color': '#509D9D',
                'tk-btn-color-primary': '#373977',
                'tk-active': 'rgb(193 130 38)',
                'tk-inactive': 'rgb(183 183 183)',
                'tk-hover': '#5a690d',
                'tk-color': '#0879A6',
                'tk-text-sidebar': '#5B691B'
            },
            boxShadow: {
                'tk-btn': 'rgba(0, 0, 0, 0.35) 0px 5px 15px;',
                'vue-card-hover': '0 4px 8px 0 rgba(0,0,0,0.10)',
                'vue-card-active': '0 8px 16px 0 rgba(0,0,0,0.10)',
                'tk-btn-2':
                    'rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px'
            },
            fontFamily: {
                montserrat: ['Montserrat', 'sans-serif']
            }
        }
    },
    plugins: []
}
