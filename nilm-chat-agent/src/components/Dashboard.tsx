// src/components/Dashboard.tsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import ElectricalMetrics from './ElectricalMetrics';
import { FiRefreshCw } from 'react-icons/fi';
import { getMockElectricalData } from '../services/mockService';

interface ElectricalData {
  id: string;
  loadType: string;
  voltage: number;
  current: number;
  power: number;
  thd: number;
  timestamp: string;
}

// Check if we should use mock data
const USE_MOCK_DATA = true; // Set to false when your backend is ready

const Dashboard = () => {
  const [data, setData] = useState<ElectricalData[]>([]);
  const [loading, setLoading] = useState(false);
  
  const fetchData = async () => {
    setLoading(true);
    try {
      if (USE_MOCK_DATA) {
        // Use mock data
        const mockData = getMockElectricalData();
        setData(mockData);
      } else {
        // Use actual backend
        const response = await axios.get('http://localhost:8000/current-data');
        setData(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch electrical data', error);
      
      // Fallback to mock data
      if (!USE_MOCK_DATA) {
        const mockData = getMockElectricalData();
        setData(mockData);
      }
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-800">Current Devices</h2>
        <button 
          onClick={fetchData}
          disabled={loading}
          className={`flex items-center gap-1 px-3 py-1 rounded-md 
            ${loading ? 'bg-gray-100 text-gray-400' : 'bg-primary-50 text-primary-600 hover:bg-primary-100'}`}
        >
          <FiRefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          <span>Refresh</span>
        </button>
      </div>
      
      {loading && data.length === 0 ? (
        <div className="text-center py-8 text-gray-500">Loading electrical data...</div>
      ) : data.length === 0 ? (
        <div className="text-center py-8 text-gray-500">No active devices detected</div>
      ) : (
        <div className="space-y-3">
          {data.map((item) => (
            <ElectricalMetrics key={item.id} data={item} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;