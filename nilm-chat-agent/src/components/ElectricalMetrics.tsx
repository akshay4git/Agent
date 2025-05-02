// src/components/ElectricalMetrics.tsx
import { useState } from 'react';

interface MetricsProps {
  data: {
    loadType: string;
    voltage: number;
    current: number;
    power: number;
    thd: number;
    timestamp: string;
  };
}

const ElectricalMetrics = ({ data }: MetricsProps) => {
  const [expanded, setExpanded] = useState(false);
  
  // Define color for THD based on value
  const getThdColor = (thd: number) => {
    if (thd < 5) return 'text-green-500';
    if (thd < 10) return 'text-yellow-500';
    return 'text-red-500';
  };
  
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 my-3">
      <div className="flex justify-between items-center">
        <h3 className="font-medium text-gray-800">
          {data.loadType} 
          <span className="ml-2 text-sm text-gray-500">
            ({new Date(data.timestamp).toLocaleTimeString()})
          </span>
        </h3>
        <button 
          onClick={() => setExpanded(!expanded)}
          className="text-primary-500 text-sm"
        >
          {expanded ? 'Show less' : 'Show more'}
        </button>
      </div>
      
      <div className="grid grid-cols-2 gap-2 mt-2">
        <div className="flex flex-col">
          <span className="text-sm text-gray-500">Power</span>
          <span className="font-medium">{data.power} W</span>
        </div>
        <div className="flex flex-col">
          <span className="text-sm text-gray-500">THD</span>
          <span className={`font-medium ${getThdColor(data.thd)}`}>
            {data.thd}%
          </span>
        </div>
      </div>
      
      {expanded && (
        <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-gray-100">
          <div className="flex flex-col">
            <span className="text-sm text-gray-500">Voltage</span>
            <span className="font-medium">{data.voltage} V</span>
          </div>
          <div className="flex flex-col">
            <span className="text-sm text-gray-500">Current</span>
            <span className="font-medium">{data.current} A</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ElectricalMetrics;