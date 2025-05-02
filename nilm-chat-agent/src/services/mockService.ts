// src/services/mockService.ts

interface ElectricalData {
    id: string;
    loadType: string;
    voltage: number;
    current: number;
    power: number;
    thd: number;
    timestamp: string;
  }
  
  // Mock electrical device data
  export const getMockElectricalData = (): ElectricalData[] => {
    return [
      {
        id: '1',
        loadType: 'Incandescent Bulb',
        voltage: 120,
        current: 0.5,
        power: 60,
        thd: 2.1,
        timestamp: new Date().toISOString()
      },
      {
        id: '2',
        loadType: 'LED Driver',
        voltage: 120,
        current: 0.12,
        power: 12,
        thd: 18.4,
        timestamp: new Date().toISOString()
      },
      {
        id: '3',
        loadType: 'CFL Bulb',
        voltage: 120,
        current: 0.18,
        power: 20,
        thd: 12.7,
        timestamp: new Date().toISOString()
      }
    ];
  };
  
  // Generate responses based on user input patterns
  export const getMockChatResponse = (message: string): Promise<string> => {
    return new Promise((resolve) => {
      // Simulate network delay
      setTimeout(() => {
        const lowerMessage = message.toLowerCase();
        
        // Match common NILM-related queries
        if (lowerMessage.includes('thd') || lowerMessage.includes('harmonic distortion')) {
          resolve(
            "I've analyzed your electrical data and found varying THD values:\n\n" +
            "- LED Driver: 18.4% (High) - This non-linear load is causing power quality issues\n" +
            "- CFL Bulb: 12.7% (Moderate) - Common for compact fluorescent lights\n" +
            "- Incandescent Bulb: 2.1% (Low) - Linear resistive loads typically have low THD\n\n" +
            "High THD can lead to overheating in neutral conductors and reduced efficiency. Would you like recommendations for reducing THD?"
          );
        } 
        else if (lowerMessage.includes('device') || lowerMessage.includes('running') || lowerMessage.includes('active')) {
          resolve(
            "Currently active devices:\n\n" +
            "1. **Incandescent Bulb**: 60W (50% of total consumption)\n" +
            "2. **LED Driver**: 12W (10% of total consumption)\n" +
            "3. **CFL Bulb**: 20W (17% of total consumption)\n\n" +
            "Total power consumption: 92W"
          );
        }
        else if (lowerMessage.includes('power') || lowerMessage.includes('consumption') || lowerMessage.includes('usage')) {
          resolve(
            "Power consumption breakdown:\n\n" +
            "- Current total: 92W\n" +
            "- Daily average: 1.2kWh\n" +
            "- Weekly trend: 8% decrease\n\n" +
            "Your most energy-intensive device is the incandescent bulb (60W). Replacing it with an LED equivalent (9W) could reduce your consumption by approximately 51W."
          );
        }
        else if (lowerMessage.includes('cfl') || lowerMessage.includes('fluorescent')) {
          resolve(
            "I've detected a CFL bulb in your circuit:\n\n" +
            "- Power: 20W\n" +
            "- Current: 0.18A\n" +
            "- THD: 12.7%\n\n" +
            "Compact Fluorescent Lamps typically have a moderate THD due to their electronic ballasts. This is within normal range, though slightly higher than ideal. CFLs consume about 75% less energy than incandescent bulbs but contain small amounts of mercury, so proper disposal is important."
          );
        }
        else if (lowerMessage.includes('led')) {
          resolve(
            "LED driver analysis:\n\n" +
            "- Power: 12W\n" +
            "- Current: 0.12A\n" +
            "- THD: 18.4% (Higher than ideal)\n\n" +
            "The high THD indicates this is likely a lower-quality LED driver. Premium LED drivers typically maintain THD below 10%. High THD can cause power quality issues in your electrical system. Consider using LED drivers with power factor correction for better performance."
          );
        }
        else if (lowerMessage.includes('help') || lowerMessage.includes('capabilities') || lowerMessage.includes('what can you do')) {
          resolve(
            "I can help you understand your electrical usage by analyzing NILM (Non-Intrusive Load Monitoring) data. Here's what you can ask me about:\n\n" +
            "- **Device identification**: What devices are currently running?\n" +
            "- **Power consumption**: How much power am I using right now?\n" +
            "- **Specific devices**: Tell me about my LED lights or CFL bulbs\n" +
            "- **Power quality**: What's my THD (Total Harmonic Distortion)?\n" +
            "- **Recommendations**: How can I reduce my energy consumption?\n\n" +
            "Feel free to ask me anything about your electrical usage!"
          );
        }
        else {
          resolve(
            "I'm your NILM Chat Agent, analyzing your electrical load data. I notice you have three active devices: an incandescent bulb (60W), a CFL bulb (20W), and an LED driver (12W). How can I help you understand your electrical usage better today?"
          );
        }
      }, 800); // Simulate 800ms response time
    });
  };