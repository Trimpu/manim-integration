// API service for communicating with Flask backend
const API_BASE_URL = 'http://localhost:5000/api';

export const mathVideoAPI = {
  // Generate video from selected text
  generateVideo: async (selectedText, options = {}) => {
    try {
      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          topic: selectedText,
          difficulty: options.difficulty || 'intermediate',
          duration: options.duration || 45,
          quality: options.quality || 'medium_quality'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error generating video:', error);
      throw error;
    }
  },

  // Check generation status
  checkStatus: async (taskId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/status/${taskId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error checking status:', error);
      throw error;
    }
  },

  // Download video
  downloadVideo: (videoPath) => {
    const downloadUrl = `${API_BASE_URL}/download/${encodeURIComponent(videoPath)}`;
    window.open(downloadUrl, '_blank');
  },

  // Check if backend is properly set up
  checkSetup: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/setup`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error checking setup:', error);
      return { status: 'error', message: 'Backend unavailable' };
    }
  },

  // List all generated videos
  listVideos: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/videos`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error listing videos:', error);
      return [];
    }
  }
};
