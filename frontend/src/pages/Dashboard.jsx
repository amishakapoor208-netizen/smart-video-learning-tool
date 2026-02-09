import React, { useState, useEffect } from 'react';
import { localStorageService } from '../services/localStorageService';

export default function Dashboard() {
  const [videos, setVideos] = useState([]);
  const [stats, setStats] = useState({ totalVideos: 0, totalQuizzes: 0, averageScore: 0 });
  const [selectedVideo, setSelectedVideo] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    const allVideos = localStorageService.getAllVideos();
    setVideos(allVideos);
    setStats(localStorageService.getStats());
  };

  const handleDeleteVideo = (videoId) => {
    if (window.confirm('Are you sure you want to delete this video?')) {
      localStorageService.deleteVideo(videoId);
      loadData();
      setSelectedVideo(null);
    }
  };

  const handleClearAll = () => {
    if (window.confirm('This will delete ALL saved videos and quizzes. Are you sure?')) {
      localStorageService.clearAll();
      loadData();
      setSelectedVideo(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">📊 Dashboard</h1>
          <p className="text-gray-600">Your learning progress and saved videos</p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            icon="📹"
            title="Videos Processed"
            value={stats.totalVideos}
            color="from-blue-500 to-blue-600"
          />
          <StatCard
            icon="❓"
            title="Quizzes Taken"
            value={stats.totalQuizzes}
            color="from-purple-500 to-purple-600"
          />
          <StatCard
            icon="⭐"
            title="Average Score"
            value={`${stats.averageScore}%`}
            color="from-green-500 to-green-600"
          />
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Videos List */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">📚 Saved Videos</h2>

              {videos.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-gray-500 text-lg mb-4">No videos saved yet</p>
                  <p className="text-gray-400">
                    Process your first video to get started!
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {videos.map((video) => (
                    <button
                      key={video.video_id}
                      onClick={() => setSelectedVideo(video)}
                      className={`w-full text-left p-4 rounded-lg border-2 transition ${
                        selectedVideo?.video_id === video.video_id
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-semibold text-gray-800 truncate">
                            {video.video_id}
                          </h3>
                          <p className="text-sm text-gray-500">
                            Created: {new Date(video.createdAt).toLocaleDateString()}
                          </p>
                        </div>
                        <span className="text-xl">▶️</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}

              {videos.length > 0 && (
                <button
                  onClick={handleClearAll}
                  className="w-full mt-6 py-2 px-4 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 font-semibold transition"
                >
                  🗑️ Clear All Data
                </button>
              )}
            </div>
          </div>

          {/* Video Details */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
              {selectedVideo ? (
                <div>
                  <h3 className="text-xl font-bold text-gray-800 mb-4">Video Details</h3>

                  <div className="space-y-4 text-sm">
                    <div>
                      <p className="text-gray-500 mb-1">Video ID</p>
                      <p className="text-gray-800 font-mono break-all">
                        {selectedVideo.video_id}
                      </p>
                    </div>

                    <div>
                      <p className="text-gray-500 mb-1">Created</p>
                      <p className="text-gray-800">
                        {new Date(selectedVideo.createdAt).toLocaleString()}
                      </p>
                    </div>

                    <div>
                      <p className="text-gray-500 mb-1">Updated</p>
                      <p className="text-gray-800">
                        {new Date(selectedVideo.updatedAt).toLocaleString()}
                      </p>
                    </div>

                    <div>
                      <p className="text-gray-500 mb-1">Quiz Results</p>
                      <p className="text-gray-800">
                        {localStorageService.getVideoQuizResults(selectedVideo.video_id).length} attempt(s)
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-2 mt-6">
                    <button
                      onClick={() => handleDeleteVideo(selectedVideo.video_id)}
                      className="flex-1 py-2 px-3 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 font-semibold transition text-sm"
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <p className="text-gray-500">Select a video to view details</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quiz History */}
        {videos.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">📈 Quiz History</h2>
            <QuizHistoryTable />
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Stat Card Component
 */
function StatCard({ icon, title, value, color }) {
  return (
    <div className={`bg-gradient-to-r ${color} rounded-lg shadow-lg p-6 text-white`}>
      <div className="text-4xl mb-2">{icon}</div>
      <p className="text-sm opacity-90 mb-1">{title}</p>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}

/**
 * Quiz History Table Component
 */
function QuizHistoryTable() {
  const quizResults = localStorageService.getQuizResults();

  if (quizResults.length === 0) {
    return <p className="text-gray-500">No quiz attempts yet</p>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b-2 border-gray-200">
            <th className="text-left py-3 px-4 font-semibold text-gray-700">Video ID</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-700">Score</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-700">Percentage</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
          </tr>
        </thead>
        <tbody>
          {quizResults.slice(-10).reverse().map((result, index) => (
            <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
              <td className="py-3 px-4 text-gray-800 font-mono text-xs truncate">
                {result.videoId}
              </td>
              <td className="py-3 px-4 text-gray-800 font-semibold">
                {result.score}/{result.totalQuestions}
              </td>
              <td className="py-3 px-4">
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                  result.percentage >= 80
                    ? 'bg-green-100 text-green-800'
                    : result.percentage >= 60
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {result.percentage.toFixed(1)}%
                </span>
              </td>
              <td className="py-3 px-4 text-gray-500 text-xs">
                {new Date(result.completedAt).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
