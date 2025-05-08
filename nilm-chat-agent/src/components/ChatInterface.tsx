// src/components/ChatInterface.tsx
import { useState, useRef, useEffect } from 'react';
import Message from './Message';
import { useLLM } from '../hooks/useLLM';
import { FiSend, FiPlusCircle } from 'react-icons/fi';

export interface MessageType {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

// Define interface for possible response object types
interface ResponseObject {
  text?: string;
  message?: string;
  content?: string;
  answer?: string;
  [key: string]: any; // Allow for other properties
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { sendMessage, loading } = useLLM();

  // Add a welcome message when the component mounts
  useEffect(() => {
    setMessages([
      {
        id: '0',
        content: 'Hello! I\'m your NILM Chat Agent. Ask me about your electrical usage, devices, or power metrics like THD.',
        role: 'assistant',
        timestamp: new Date(),
      },
    ]);
  }, []);

  // Auto-scroll to the bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage: MessageType = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      // sendMessage now returns string directly due to the changes in useLLM
      const responseText = await sendMessage(input);
      
      const assistantMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        content: responseText,
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error handling message:', error);
      const errorMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error while processing your request.',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-primary-600 text-white py-4 px-6 shadow-md">
        <h1 className="text-xl font-semibold">NILM Chat Agent</h1>
        <p className="text-sm text-primary-100">Non-Intrusive Load Monitoring Assistant</p>
      </header>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex items-center gap-2">
          <button 
            className="p-2 rounded-full text-gray-500 hover:bg-gray-100"
            aria-label="Add attachment"
          >
            <FiPlusCircle size={20} />
          </button>
          
          <div className="flex-1 flex items-center bg-gray-100 rounded-full px-4 py-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask about your electrical usage..."
              className="flex-1 bg-transparent focus:outline-none"
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !input.trim()}
              className={`ml-2 p-1 rounded-full ${
                loading || !input.trim() 
                  ? 'text-gray-400' 
                  : 'text-primary-500 hover:bg-primary-50'
              }`}
              aria-label="Send message"
            >
              <FiSend size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;