// src/components/Message.tsx
import { format } from 'date-fns';
import ReactMarkdown from 'react-markdown';
import { MessageType } from './ChatInterface';

interface MessageProps {
  message: MessageType;
}

const Message = ({ message }: MessageProps) => {
  const { content, role, timestamp } = message;
  
  const isUser = role === 'user';
  
  return (
    <div 
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div 
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser 
            ? 'bg-primary-500 text-white rounded-br-none' 
            : 'bg-white shadow-sm border border-gray-200 rounded-bl-none'
        }`}
      >
        <div className="prose prose-sm">
          {isUser ? (
            <p className="m-0">{content}</p>
          ) : (
            <ReactMarkdown>{content}</ReactMarkdown>
          )}
        </div>
        <div 
          className={`text-xs mt-1 ${
            isUser ? 'text-primary-100' : 'text-gray-400'
          }`}
        >
          {format(timestamp, 'h:mm a')}
        </div>
      </div>
    </div>
  );
};

export default Message;