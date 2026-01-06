# Fonts Directory

This directory contains web fonts for the Stationery World project.

## Font Structure

- `nexa/` - Nexa font family files
- `poppins/` - Poppins font family files  
- `montserrat/` - Montserrat font family files

## How to Add Fonts

1. Download font files (TTF, OTF, WOFF, WOFF2 formats)
2. Place them in the appropriate font family folder
3. Update `fonts.css` with the font-face declarations
4. Include the fonts in your HTML templates

## Supported Formats

- `.woff2` (recommended for web)
- `.woff`
- `.ttf`
- `.otf`

## Usage

Include the fonts.css file in your base template and use the font-family names in your CSS:

```css
body {
    font-family: 'Poppins', sans-serif;
}

.heading {
    font-family: 'Nexa', sans-serif;
}
