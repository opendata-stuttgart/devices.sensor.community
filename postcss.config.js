const purgecss = require('@fullhuman/postcss-purgecss')
const path = require('path');

console.log(path)

module.exports = {
    plugins: [
        require('postcss-import'),
        require('tailwindcss')(path.resolve(__dirname, 'tailwind.config.js')),
        require('autoprefixer'),
        // only needed if you want to purge
        process.env.FLASK_PROD === 'production' ? require('autoprefixer') : null,
        purgecss({
            content: ["./webapp/templates/*.html", "./webapp/templates/security/*.html"],
            defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
        })
    ]
}