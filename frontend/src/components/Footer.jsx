/**
 * Footer.jsx
 * 
 * Purpose:
 * Reusable footer component for consistent page footer.
 * Displays copyright and project information.
 */

function Footer() {
  const currentYear = new Date().getFullYear()
  
  return (
    <footer className="bg-gray-800 text-white mt-12 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-gray-400">
            Smart Video Learning Tool – AI-Based
          </p>
          <p className="text-gray-500 text-sm mt-2">
            © {currentYear} Final Year BCA Project. All rights reserved.
          </p>
          <p className="text-gray-500 text-sm mt-2">
            Powered by React, Vite, FastAPI, and Tailwind CSS
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
