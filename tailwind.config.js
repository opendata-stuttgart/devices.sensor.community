const colors = require('tailwindcss/colors')

module.exports = {
    purge: {
        enable: false,
        purge: ['./webapp/templates/**/*.html'],
        content: ["./webapp/templates/*.html"],
    },
    darkMode: false,
    theme: {
        colors: {
            gray: colors.coolGray,

        },
        extend: {
            colors: {
                brand: {
                    black: '#000000',
                    white: '#FFFFFF',
                    green: {
                        DEFAULT: '#084945',
                        dark: '#07403C',
                    },
                    greenBright: '#6EEFE6',
                    greenPastel: '#D1FAF7',
                    greenLight: '#EDFDFC',
                    yellow: '#E9A135',
                    yellowBright: '#EFBB6E',
                    yellowPastel: '#FAEAD1',
                    yellowLight: '#FDF6ED',
                    funcRed: '#E93559',
                    funcLime: '#5FE935',
                    funcPurple: '#2B0849'
                },
            },
            typography: {
                DEFAULT: {
                    css: {
                        a: {
                            color: '#E83559',
                            '&:hover': {
                                color: '#E83559',
                            },
                            'font-weight': '400',
                            'text-decoration': 'none',
                        },
                        img: {
                            display: 'inline',
                        },
                        blockquote: {
                            'border-left-color': '#E93559'
                        },
                    },
                },
            },
            animation: {
                heartBeat: "heartBeat 2s cubic-bezier(0, 0, 0.2, 1) infinite",
            },
            keyframes: {
                heartBeat: {
                    "0%": {
                        transform: "scale(0.6)",
                    },
                    "50%": {
                        transform: "scale(0.8)",
                    },
                    "100%": {
                        transform: "scale(0.6)",
                    }
                },
            }
        },
    },
    variants: {
        extend: {
            backgroundColor: ["active"],
        },
    },
    plugins: [
        require('tailwindcss/colors'),
        require('@tailwindcss/forms')
    ]
}