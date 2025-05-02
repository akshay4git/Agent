// src/App.tsx
import { useState } from 'react';
import Layout from './components/Layout';
import ChatInterface from './components/ChatInterface';
import Dashboard from './components/Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'dashboard'>('chat');
  
  return (
    <Layout>
      <div className="flex h-16 border-b items-center px-4">
        <div className="flex space-x-4">
          <button
            className={`pb-4 px-1 border-b-2 ${
              activeTab === 'chat' 
                ? 'border-primary-500 text-primary-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
          <button
            className={`pb-4 px-1 border-b-2 ${
              activeTab === 'dashboard' 
                ? 'border-primary-500 text-primary-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
        </div>
      </div>
      
      <div className="h-[calc(100%-4rem)]">
        {activeTab === 'chat' ? <ChatInterface /> : <Dashboard />}
      </div>
    </Layout>
  );
}

export default App;