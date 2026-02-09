import React, { useState, useEffect } from 'react';
import { mockAIService } from '../services/mockAIService';
import { localStorageService } from '../services/localStorageService';

export default function VideoProcessor() {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('summary');

  const handleProcess = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!mockAIService.validateYouTubeUrl(youtubeUrl)) {
        throw new Error('Please enter a valid YouTube URL');
      }

      const result = await mockAIService.processVideo(youtubeUrl);
      
      // Save to local storage
      localStorageService.saveVideo(result);
      
      setResult(result);
      setYoutubeUrl('');
      setActiveTab('summary');
    } catch (err) {
      setError(err.message || 'Failed to process video');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            📚 Smart Video Learning Tool
          </h1>
          <p className="text-gray-600">
            Transform YouTube videos into structured learning materials
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <form onSubmit={handleProcess}>
            <div className="mb-4">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                YouTube URL
              </label>
              <input
                type="url"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                placeholder="https://www.youtube.com/watch?v=..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                disabled={loading}
              />
              <p className="text-xs text-gray-500 mt-1">
                Example: https://www.youtube.com/watch?v=jNQXAC9IVRw
              </p>
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 text-sm">❌ {error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 rounded-lg font-semibold transition ${
                loading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Processing... (please wait)
                </span>
              ) : (
                '🚀 Generate Learning Material'
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        {result && (
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Tabs */}
            <div className="flex border-b">
              {[
                { id: 'summary', label: '📝 Summary', icon: '📝' },
                { id: 'keypoints', label: '⭐ Key Points', icon: '⭐' },
                { id: 'quiz', label: '❓ Quiz', icon: '❓' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 px-4 py-3 font-semibold transition ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="p-8">
              {activeTab === 'summary' && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">Summary</h2>
                  <p className="text-gray-700 leading-relaxed">{result.summary}</p>
                </div>
              )}

              {activeTab === 'keypoints' && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">Key Points</h2>
                  <ul className="space-y-3">
                    {result.key_points.map((point, index) => (
                      <li key={index} className="flex items-start">
                        <span className="flex-shrink-0 h-6 w-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-semibold text-sm mr-3 mt-0.5">
                          {index + 1}
                        </span>
                        <span className="text-gray-700">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {activeTab === 'quiz' && (
                <QuizComponent quiz={result.quiz} videoId={result.video_id} />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Quiz Component
 */
function QuizComponent({ quiz, videoId }) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [userAnswers, setUserAnswers] = useState({});

  const handleAnswerSelect = (answerLetter) => {
    const question = quiz[currentQuestion];
    const isCorrect = answerLetter === question.correct_answer;

    setUserAnswers({
      ...userAnswers,
      [currentQuestion]: {
        selected: answerLetter,
        correct: question.correct_answer,
        isCorrect,
      },
    });

    if (isCorrect) {
      setScore(score + 1);
    }

    // Auto-move to next question after selection
    setTimeout(() => {
      if (currentQuestion < quiz.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
      } else {
        setShowResults(true);
        // Save results to local storage
        localStorageService.saveQuizResult(videoId, {
          score,
          totalQuestions: quiz.length,
          percentage: ((score + 1) / quiz.length) * 100,
          answers: userAnswers,
        });
      }
    }, 500);
  };

  const question = quiz[currentQuestion];
  const answerLetters = ['A', 'B', 'C', 'D'];

  if (showResults) {
    const percentage = ((score + 1) / quiz.length) * 100;
    return (
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Quiz Results</h2>
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-8 text-center">
          <div className="text-6xl font-bold text-blue-600 mb-2">{score + 1}/{quiz.length}</div>
          <div className="text-3xl font-semibold text-gray-800 mb-4">
            {percentage.toFixed(1)}%
          </div>
          <div className="text-lg text-gray-600 mb-6">
            {percentage >= 80
              ? '🎉 Excellent! You mastered this topic!'
              : percentage >= 60
              ? '✨ Good job! Review the missed questions.'
              : '📚 Keep practicing! Review all concepts.'}
          </div>
          <button
            onClick={() => {
              setCurrentQuestion(0);
              setScore(0);
              setShowResults(false);
              setUserAnswers({});
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition"
          >
            Retake Quiz
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          Question {currentQuestion + 1}/{quiz.length}
        </h2>
        <span className="text-lg font-semibold text-blue-600">
          Score: {score}/{quiz.length}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${((currentQuestion + 1) / quiz.length) * 100}%` }}
        />
      </div>

      {/* Question */}
      <h3 className="text-xl font-semibold text-gray-800 mb-6">{question.question}</h3>

      {/* Options */}
      <div className="space-y-3">
        {question.options.map((option, index) => (
          <button
            key={index}
            onClick={() => handleAnswerSelect(answerLetters[index])}
            className="w-full text-left p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition"
          >
            <span className="font-semibold text-blue-600 mr-3">{answerLetters[index]}.</span>
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}
