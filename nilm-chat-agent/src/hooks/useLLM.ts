// src/hooks/useLLM.ts
import { useState } from 'react';
import axios from 'axios';


// Configuration from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const CHAT_ENDPOINT = '/api/chat';

// Define interface for possible response types
interface ResponseObject {
  text?: string;
  message?: string;
  content?: string;
  response?: string;
  answer?: string;
  [key: string]: any; // Allow for other properties
}

export const useLLM = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (message: string): Promise<string> => {
    setLoading(true);
    setError(null);

    try {
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
      
      // Extract the response text from the API response
      const responseData = response.data.response || response.data;
      
      // Make sure we return a string
      if (typeof responseData === 'string') {
        return responseData;
      } else if (responseData && typeof responseData === 'object') {
        const responseObj = responseData as ResponseObject;
        return responseObj.text || 
               responseObj.message || 
               responseObj.content || 
               responseObj.answer || 
               JSON.stringify(responseObj);
      }
      
      return String(responseData);
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