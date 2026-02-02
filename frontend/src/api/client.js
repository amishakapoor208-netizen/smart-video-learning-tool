/**
 * Axios API Client Configuration
 * 
 * Purpose:
 * - Centralized HTTP client for all API communication
 * - Automatically uses environment-based API URL
 * - Includes request/response interceptors for future enhancements
 * 
 * Usage:
 * import apiClient from './api/client'
 * apiClient.get('/endpoint').then(res => console.log(res.data))
 */

import axios from 'axios'

// Get API base URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create Axios instance with base URL
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request Interceptor (for future use)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available (future implementation)
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

// Response Interceptor (for future use)
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle common errors globally (future implementation)
    console.error('API Error:', error.message)
    return Promise.reject(error)
  }
)

export default apiClient
