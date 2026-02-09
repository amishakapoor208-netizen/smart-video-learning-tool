/**
 * Local Storage Service
 * Handles all data persistence to browser's local storage
 */

const STORAGE_KEYS = {
  VIDEOS: 'svlt_videos',
  CURRENT_VIDEO: 'svlt_current_video',
  QUIZ_RESULTS: 'svlt_quiz_results',
};

export const localStorageService = {
  /**
   * Save a processed video to local storage
   */
  saveVideo: (videoData) => {
    try {
      const videos = localStorageService.getAllVideos();
      const existingIndex = videos.findIndex((v) => v.video_id === videoData.video_id);

      if (existingIndex >= 0) {
        videos[existingIndex] = { ...videos[existingIndex], ...videoData, updatedAt: new Date().toISOString() };
      } else {
        videos.push({
          ...videoData,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        });
      }

      localStorage.setItem(STORAGE_KEYS.VIDEOS, JSON.stringify(videos));
      return true;
    } catch (error) {
      console.error('Error saving video:', error);
      return false;
    }
  },

  /**
   * Get all videos from local storage
   */
  getAllVideos: () => {
    try {
      const videos = localStorage.getItem(STORAGE_KEYS.VIDEOS);
      return videos ? JSON.parse(videos) : [];
    } catch (error) {
      console.error('Error getting videos:', error);
      return [];
    }
  },

  /**
   * Get a specific video by ID
   */
  getVideo: (videoId) => {
    try {
      const videos = localStorageService.getAllVideos();
      return videos.find((v) => v.video_id === videoId) || null;
    } catch (error) {
      console.error('Error getting video:', error);
      return null;
    }
  },

  /**
   * Delete a video from local storage
   */
  deleteVideo: (videoId) => {
    try {
      const videos = localStorageService.getAllVideos();
      const filtered = videos.filter((v) => v.video_id !== videoId);
      localStorage.setItem(STORAGE_KEYS.VIDEOS, JSON.stringify(filtered));
      return true;
    } catch (error) {
      console.error('Error deleting video:', error);
      return false;
    }
  },

  /**
   * Save current video being viewed
   */
  setCurrentVideo: (videoId) => {
    try {
      localStorage.setItem(STORAGE_KEYS.CURRENT_VIDEO, videoId);
      return true;
    } catch (error) {
      console.error('Error setting current video:', error);
      return false;
    }
  },

  /**
   * Get current video ID
   */
  getCurrentVideo: () => {
    try {
      return localStorage.getItem(STORAGE_KEYS.CURRENT_VIDEO) || null;
    } catch (error) {
      console.error('Error getting current video:', error);
      return null;
    }
  },

  /**
   * Save quiz result
   */
  saveQuizResult: (videoId, quizResult) => {
    try {
      const results = localStorageService.getQuizResults();
      results.push({
        videoId,
        ...quizResult,
        completedAt: new Date().toISOString(),
      });
      localStorage.setItem(STORAGE_KEYS.QUIZ_RESULTS, JSON.stringify(results));
      return true;
    } catch (error) {
      console.error('Error saving quiz result:', error);
      return false;
    }
  },

  /**
   * Get all quiz results
   */
  getQuizResults: () => {
    try {
      const results = localStorage.getItem(STORAGE_KEYS.QUIZ_RESULTS);
      return results ? JSON.parse(results) : [];
    } catch (error) {
      console.error('Error getting quiz results:', error);
      return [];
    }
  },

  /**
   * Get quiz results for specific video
   */
  getVideoQuizResults: (videoId) => {
    try {
      const results = localStorageService.getQuizResults();
      return results.filter((r) => r.videoId === videoId);
    } catch (error) {
      console.error('Error getting video quiz results:', error);
      return [];
    }
  },

  /**
   * Clear all local storage data
   */
  clearAll: () => {
    try {
      localStorage.removeItem(STORAGE_KEYS.VIDEOS);
      localStorage.removeItem(STORAGE_KEYS.CURRENT_VIDEO);
      localStorage.removeItem(STORAGE_KEYS.QUIZ_RESULTS);
      return true;
    } catch (error) {
      console.error('Error clearing local storage:', error);
      return false;
    }
  },

  /**
   * Get storage statistics
   */
  getStats: () => {
    try {
      const videos = localStorageService.getAllVideos();
      const quizResults = localStorageService.getQuizResults();
      return {
        totalVideos: videos.length,
        totalQuizzes: quizResults.length,
        averageScore: quizResults.length > 0
          ? (quizResults.reduce((sum, r) => sum + (r.score || 0), 0) / quizResults.length).toFixed(2)
          : 0,
      };
    } catch (error) {
      console.error('Error getting stats:', error);
      return { totalVideos: 0, totalQuizzes: 0, averageScore: 0 };
    }
  },
};
