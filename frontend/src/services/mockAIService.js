/**
 * Mock AI Service
 * Simulates AI responses for demo/testing without requiring backend
 * Can be replaced with real backend API calls later
 */

/**
 * Extract video ID from YouTube URL
 */
const extractVideoId = (url) => {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match && match[1]) {
      return match[1];
    }
  }
  return null;
};

/**
 * Generate mock transcript (simulates video transcript extraction)
 */
const generateMockTranscript = (videoId) => {
  const transcripts = {
    jNQXAC9IVRw: `Welcome to this video on machine learning. Today we'll explore the fundamentals of machine learning, including supervised learning, unsupervised learning, and reinforcement learning.

Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. There are three main types: supervised learning where we have labeled data, unsupervised learning where we explore unlabeled data, and reinforcement learning where agents learn through interaction.

Key concepts include features, labels, models, and training. Features are input variables, labels are output variables, models are mathematical representations, and training is the process of adjusting model parameters.

Common algorithms include linear regression for continuous outputs, logistic regression for classification, decision trees for interpretable models, and neural networks for complex patterns.

Data preprocessing is crucial. We need to handle missing values, normalize features, and split data into training and testing sets. The training set helps the model learn patterns, while the testing set evaluates performance.

Evaluation metrics depend on the problem. For regression, we use mean squared error and R-squared. For classification, we use accuracy, precision, recall, and F1-score.

In practice, always remember: garbage in, garbage out. Quality data leads to quality models. Overfitting occurs when models memorize training data instead of learning patterns. Use regularization and cross-validation to prevent this.

Thank you for watching!`,
    default: `This video discusses an important topic in computer science. The content covers fundamental concepts, practical applications, and best practices. Key takeaways include understanding core principles, implementing solutions effectively, and continuous learning. The speaker emphasizes the importance of practice and real-world application. Throughout the video, various examples and use cases are presented to illustrate the concepts. The importance of staying updated with latest technologies is highlighted. Viewers are encouraged to experiment and build projects. Regular practice and learning from mistakes are crucial for mastery. The video concludes with resources for further learning and community engagement.`,
  };

  return transcripts[videoId] || transcripts.default;
};

/**
 * Generate mock summary
 */
const generateMockSummary = (transcript) => {
  const summaries = [
    'Machine learning is a subset of AI that enables systems to learn from data. There are three main types: supervised learning with labeled data, unsupervised learning for pattern discovery, and reinforcement learning through agent interaction. Proper data preprocessing and evaluation metrics are essential for building effective models.',
    'This video covers fundamental concepts and practical applications in the field. Key takeaways include understanding core principles, implementing effective solutions, and continuous learning through practice and experimentation. Staying updated with latest technologies and learning from mistakes are crucial for mastery.',
    'The content provides an overview of essential topics and best practices. Important principles are discussed with real-world examples and applications. The key message emphasizes the importance of understanding fundamentals, consistent practice, and community engagement for professional growth.',
  ];

  return summaries[Math.floor(Math.random() * summaries.length)];
};

/**
 * Generate mock key points
 */
const generateMockKeyPoints = (transcript) => {
  const keyPointsOptions = [
    [
      'Machine learning is a subset of AI that learns from data without explicit programming',
      'Three main types: supervised learning, unsupervised learning, and reinforcement learning',
      'Features are inputs, labels are outputs, models are mathematical representations',
      'Key algorithms: linear regression, logistic regression, decision trees, neural networks',
      'Data preprocessing includes handling missing values and feature normalization',
      'Evaluation metrics vary by problem: accuracy for classification, MSE for regression',
      'Prevent overfitting through regularization and cross-validation techniques',
    ],
    [
      'Understanding fundamental concepts is the foundation for practical implementation',
      'Real-world applications require effective problem-solving and critical thinking',
      'Continuous learning and staying updated with new technologies is essential',
      'Practice through building projects helps solidify theoretical knowledge',
      'Community engagement provides support and diverse perspectives',
      'Mistakes and failures are valuable learning opportunities',
      'Balancing theory and practice leads to professional expertise',
    ],
    [
      'Core principles provide the foundation for all advanced techniques',
      'Implementation requires careful planning and attention to detail',
      'Testing and validation ensure solution quality and reliability',
      'Documentation helps future maintenance and knowledge sharing',
      'Performance optimization improves efficiency and user experience',
      'Security considerations protect data and maintain system integrity',
      'Continuous improvement through feedback drives innovation',
    ],
  ];

  return keyPointsOptions[Math.floor(Math.random() * keyPointsOptions.length)];
};

/**
 * Generate mock quiz questions
 */
const generateMockQuiz = (transcript) => {
  const quizzesOptions = [
    [
      {
        question: 'What is machine learning?',
        options: [
          'A subset of AI that learns from data without explicit programming',
          'A type of programming language',
          'A hardware technology',
          'A social media platform',
        ],
        correct_answer: 'A',
      },
      {
        question: 'How many main types of machine learning are there?',
        options: ['Two', 'Three', 'Four', 'Five'],
        correct_answer: 'B',
      },
      {
        question: 'What is a feature in machine learning?',
        options: [
          'A label value',
          'An input variable',
          'A trained model',
          'A testing set',
        ],
        correct_answer: 'B',
      },
      {
        question: 'Which algorithm is used for continuous outputs?',
        options: [
          'Logistic regression',
          'Decision trees',
          'Linear regression',
          'K-means clustering',
        ],
        correct_answer: 'C',
      },
      {
        question: 'What does data preprocessing involve?',
        options: [
          'Only splitting data',
          'Only normalizing features',
          'Handling missing values and normalizing features',
          'Creating new datasets',
        ],
        correct_answer: 'C',
      },
      {
        question: 'What is overfitting?',
        options: [
          'Using too many features',
          'Models memorizing training data instead of learning patterns',
          'Having insufficient training data',
          'Using complex algorithms',
        ],
        correct_answer: 'B',
      },
      {
        question: 'Which metric is used for classification problems?',
        options: ['Mean squared error', 'R-squared', 'Accuracy', 'RMSE'],
        correct_answer: 'C',
      },
      {
        question: 'What is cross-validation used for?',
        options: [
          'Data preprocessing',
          'Model training',
          'Preventing overfitting',
          'Feature selection',
        ],
        correct_answer: 'C',
      },
      {
        question: 'Which type of learning uses labeled data?',
        options: [
          'Unsupervised learning',
          'Reinforcement learning',
          'Supervised learning',
          'Self-learning',
        ],
        correct_answer: 'C',
      },
      {
        question: 'What is the golden rule of machine learning?',
        options: [
          'Always use complex models',
          'Garbage in, garbage out',
          'More data is always better',
          'Features are more important than data',
        ],
        correct_answer: 'B',
      },
    ],
    [
      {
        question: 'What is the first step in most projects?',
        options: [
          'Implement solutions',
          'Understand requirements',
          'Deploy to production',
          'Test thoroughly',
        ],
        correct_answer: 'B',
      },
      {
        question: 'Why is practice important?',
        options: [
          'It wastes time',
          'It solidifies theoretical knowledge',
          'It is not necessary',
          'It causes confusion',
        ],
        correct_answer: 'B',
      },
      {
        question: 'How should mistakes be viewed?',
        options: [
          'As failures to avoid',
          'As valuable learning opportunities',
          'As signs of incompetence',
          'As reasons to quit',
        ],
        correct_answer: 'B',
      },
      {
        question: 'What does staying updated mean?',
        options: [
          'Ignoring new technologies',
          'Following latest trends continuously',
          'Learning new tools and methodologies',
          'Rejecting old practices',
        ],
        correct_answer: 'C',
      },
      {
        question: 'Why is community engagement valuable?',
        options: [
          'It wastes time',
          'It provides support and diverse perspectives',
          'It is not necessary',
          'It slows down progress',
        ],
        correct_answer: 'B',
      },
      {
        question: 'What is the balance between theory and practice?',
        options: [
          'Only theory is needed',
          'Only practice is needed',
          'Both are essential for expertise',
          'Neither is important',
        ],
        correct_answer: 'C',
      },
      {
        question: 'How should feedback be handled?',
        options: [
          'Ignored completely',
          'Used for continuous improvement',
          'Viewed as criticism only',
          'Dismissed immediately',
        ],
        correct_answer: 'B',
      },
      {
        question: 'What drives professional growth?',
        options: [
          'Staying comfortable',
          'Avoiding challenges',
          'Continuous learning and practice',
          'Ignoring feedback',
        ],
        correct_answer: 'C',
      },
      {
        question: 'Why is documentation important?',
        options: [
          'It is unnecessary',
          'It helps future maintenance and knowledge sharing',
          'It slows development',
          'It is only for large projects',
        ],
        correct_answer: 'B',
      },
      {
        question: 'What is the key to mastery?',
        options: [
          'Quick learning',
          'Avoiding mistakes',
          'Consistent practice and continuous improvement',
          'Natural talent alone',
        ],
        correct_answer: 'C',
      },
    ],
  ];

  return quizzesOptions[Math.floor(Math.random() * quizzesOptions.length)];
};

/**
 * Process video and generate learning package
 * This simulates what the backend API would do
 */
export const mockAIService = {
  /**
   * Process a YouTube video and generate learning content
   */
  processVideo: async (youtubeUrl) => {
    return new Promise((resolve, reject) => {
      try {
        // Simulate network delay
        setTimeout(() => {
          const videoId = extractVideoId(youtubeUrl);

          if (!videoId) {
            reject(new Error('Invalid YouTube URL. Please provide a valid YouTube link.'));
            return;
          }

          const transcript = generateMockTranscript(videoId);
          const summary = generateMockSummary(transcript);
          const keyPoints = generateMockKeyPoints(transcript);
          const quiz = generateMockQuiz(transcript);

          resolve({
            video_id: videoId,
            youtube_url: youtubeUrl,
            transcript,
            summary,
            key_points: keyPoints,
            quiz,
          });
        }, 2000); // 2-second delay to simulate API call
      } catch (error) {
        reject(error);
      }
    });
  },

  /**
   * Extract video ID from URL
   */
  extractVideoId,

  /**
   * Validate YouTube URL
   */
  validateYouTubeUrl: (url) => {
    try {
      new URL(url);
      return extractVideoId(url) !== null;
    } catch {
      return false;
    }
  },
};
