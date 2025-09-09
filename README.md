# React PDF Viewer

A modern React PDF viewer with continuous scrolling, text selection, and floating action buttons.

## Features

- 📄 **Continuous PDF Scrolling** - Smooth page-by-page scrolling like Adobe/Chrome viewers
- 🔍 **Zoom Controls** - Zoom in/out with scale indicator
- 📝 **Text Selection** - Select text within PDFs with floating action button
- 🎯 **Clean UI** - Minimal design with TailwindCSS
- 📱 **Responsive** - Works across different screen sizes

## Setup Instructions

### 1. Install Dependencies

```bash
npm install react-pdf pdfjs-dist tailwindcss autoprefixer postcss
```

### 2. Install React Scripts (if needed)

```bash
npm install react-scripts
```

### 3. Start Development Server

```bash
npm start
```

## Component Structure

- `PdfViewer.jsx` - Main PDF viewer component with text selection logic
- `Toolbar.jsx` - Top toolbar with file input, zoom controls, and page indicator  
- `FloatingButton.jsx` - Floating action button shown on text selection

## Usage

1. Click "Open PDF" to select a PDF file
2. Use zoom controls (+/-) to adjust viewing scale
3. Scroll through pages continuously
4. Select text to see the "Visualize" floating button
5. Click "Visualize" to trigger the action (currently logs to console)

## Technologies Used

- **React** - Frontend framework
- **react-pdf** - PDF rendering (pdf.js wrapper)
- **TailwindCSS** - Styling framework
- **pdfjs-dist** - PDF.js library

## Browser Compatibility

Works in all modern browsers that support PDF.js.
