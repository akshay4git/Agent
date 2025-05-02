// src/components/Layout.tsx
import { ReactNode, useState } from 'react';
import { FiMessageSquare, FiGrid, FiSettings, FiMenu, FiX } from 'react-icons/fi';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const [showSidebar, setShowSidebar] = useState(false);
  
  const menuItems = [
    { icon: <FiMessageSquare />, label: 'Chat', active: true },
    { icon: <FiGrid />, label: 'Dashboard', active: false },
    { icon: <FiSettings />, label: 'Settings', active: false },
  ];
  
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Mobile menu button */}
      <button
        className="lg:hidden fixed top-4 left-4 z-20 p-2 rounded-md bg-white shadow-md text-gray-700"
        onClick={() => setShowSidebar(!showSidebar)}
      >
        {showSidebar ? <FiX size={24} /> : <FiMenu size={24} />}
      </button>
      
      {/* Sidebar */}
      <div 
        className={`fixed lg:static inset-y-0 left-0 z-10 w-64 bg-white shadow-md transform transition-transform duration-300 ease-in-out ${
          showSidebar ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-4 border-b">
          <h1 className="text-xl font-bold text-primary-600">NILM Chat</h1>
          <p className="text-sm text-gray-500">Electrical Insights Assistant</p>
        </div>
        
        <nav className="p-4">
          <ul className="space-y-2">
            {menuItems.map((item, index) => (
              <li key={index}>
                <a 
                  href="#" 
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg ${
                    item.active 
                      ? 'bg-primary-50 text-primary-600' 
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
      
      {/* Main content */}
      <div className="flex-1 overflow-auto">
        {children}
      </div>
    </div>
  );
};

export default Layout;