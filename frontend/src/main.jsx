// Main entry point for React application
// Configures React 18 with the root component

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

console.log('🚀 main.jsx loading...')
const rootElement = document.getElementById('root')
console.log('✓ Root element found:', rootElement)

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

console.log('✓ React mounted successfully')
