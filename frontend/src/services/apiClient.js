/**
 * apiClient.js
 * 
 * Purpose:
 * Centralized HTTP client for all backend API communication.
 * Handles environment-based URL switching and request configuration.
 * 
 * Features:
 * - Environment-aware base URL (development vs production)
 * - Request/response interceptors for future auth/error handling
 * - Consistent error handling structure
 * - Timeout configuration for production
 * 
 * Usage:
 * import apiClient from '@/services/apiClient'
 * apiClient.get('/endpoint').then(res => console.log(res.data))
 */

import axios from 'axios'

// Get API base URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  }
})

/**
 * Request Interceptor
 * Runs before each API request
 * Use for: Adding auth tokens, headers, etc.
 */
apiClient.interceptors.request.use(
  (config) => {
    // Example: Add auth token if available
    // const token = localStorage.getItem('authToken')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Response Interceptor
 * Runs after receiving API response
 * Use for: Global error handling, token refresh, etc.
 */
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Log errors for debugging (remove in production)
    console.error('API Error:', error.message)
    
    // Example: Handle specific status codes
    // if (error.response?.status === 401) {
    //   // Handle unauthorized - redirect to login
    // }
    
    return Promise.reject(error)
  }
)

export default apiClient
