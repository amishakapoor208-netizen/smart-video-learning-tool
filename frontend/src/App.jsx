import { useState } from 'react'
import './App.css'
import VideoProcessor from './pages/VideoProcessor'
import Dashboard from './pages/Dashboard'

console.log('App.jsx loaded')

function App() {
  const [currentPage, setCurrentPage] = useState('processor')
  console.log('App rendered, currentPage:', currentPage)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">📚</span>
            <h1 className="text-2xl font-bold">Smart Video Learning Tool</h1>
          </div>
          <div className="flex gap-4">
            <NavButton
              label="🎬 Create"
              isActive={currentPage === 'processor'}
              onClick={() => setCurrentPage('processor')}
            />
            <NavButton
              label="📊 Dashboard"
              isActive={currentPage === 'dashboard'}
              onClick={() => setCurrentPage('dashboard')}
            />
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <div>
        {currentPage === 'processor' && <VideoProcessor />}
        {currentPage === 'dashboard' && <Dashboard />}
      </div>
    </div>
  )
}

function NavButton({ label, isActive, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-lg font-semibold transition ${
        isActive
          ? 'bg-white text-blue-600'
          : 'text-white hover:bg-white hover:bg-opacity-20'
      }`}
    >
      {label}
    </button>
  )
}

export default App
