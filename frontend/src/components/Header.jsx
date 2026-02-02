/**
 * Header.jsx
 * 
 * Purpose:
 * Reusable header component for navigation and branding.
 * 
 * Props:
 * - title (string): Page title to display
 * 
 * Note: Placeholder for future navigation logic
 */

function Header({ title = "Smart Video Learning Tool" }) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
      </div>
    </header>
  )
}

export default Header
