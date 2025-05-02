// src/hooks/useLLM.ts
import { useState } from 'react';
import axios from 'axios';
import { getMockChatResponse } from '../services/mockService';

// Configuration from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true';
const CHAT_ENDPOINT = '/api/chat';

export const useLLM = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (message: string) => {
    setLoading(true);
    setError(null);

    try {
      if (USE_MOCK_DATA) {
        const response = await getMockChatResponse(message);
        setLoading(false);
        return response;
      }

      const response = await axios.post(
        `${API_BASE_URL}${CHAT_ENDPOINT}`,
        { message },
        {
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          timeout: 10000 // 10 second timeout
        }
      );

      if (!response.data) {
        throw new Error('Empty response from server');
      }

      setLoading(false);
      return response.data.response || response.data;
    } catch (err) {
      console.error('API Error:', err);
      setLoading(false);

      let errorMessage = 'Failed to communicate with the NILM service.';
      
      if (axios.isAxiosError(err)) {
        errorMessage = err.response?.data?.message || 
                       err.message || 
                       'Network error occurred';
      }

      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  return { sendMessage, loading, error };
};