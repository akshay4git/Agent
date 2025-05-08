# Frontend Documentation for NILM Chat Application

## 1. Overview:
This project is a Non-Intrusive Load Monitoring (NILM) Chat Assistant built using ReactJS. The app is designed to provide insights into electrical usage, devices, and power metrics through a conversational interface. The user interacts with the system via a chat interface where they can ask questions about power consumption, device status, and related metrics.

## 2. Key Features:
- **Real-time Interaction**: The app allows users to interact with an AI-powered chat agent.
- **Dynamic Device Metrics**: Users can monitor and query device metrics like voltage, current, power, and Total Harmonic Distortion (THD) in real-time.
- **Sidebar Navigation**: Provides access to different sections like Chat, Dashboard, and Settings.
- **Message Formatting**: Uses React Markdown to render chat content in markdown format, allowing for rich text responses from the server.
- **Automatic Refresh**: Electrical data on the Dashboard refreshes every 30 seconds to provide real-time updates.

## 3. Folder Structure:
- **/src**: Contains all the source code for the application.
- **/components**: Contains all UI components such as the Chat Interface, Electrical Metrics display, and Dashboard.
- **/hooks**: Contains custom hooks like useLLM to handle communication with the backend.
- **/styles**: CSS or Tailwind configurations for the frontend styling.
- **/assets**: Static assets like images, icons, etc.

## 4. Components:

### 4.1. ChatInterface.tsx
**Purpose**: Displays the chat interface, allowing users to send and receive messages.

**State Variables**:
- `messages`: An array to store chat messages.
- `input`: The current input message from the user.
- `messagesEndRef`: Used to scroll to the bottom of the chat when new messages are added.

**Functions**:
- `handleSendMessage`: Sends a message to the backend and appends the assistant's response.

### 4.2. Message.tsx
**Purpose**: Renders individual chat messages, formatting them based on whether the message is from the user or assistant.

**Features**:
- Renders the message in markdown format if the sender is the assistant.
- Displays a timestamp with each message.

### 4.3. ElectricalMetrics.tsx
**Purpose**: Displays real-time electrical data like power, voltage, current, and THD for each device.

**State Variables**:
- `expanded`: Toggles between showing less or more detailed metrics.

**Features**:
- Dynamic styling for THD based on its value (green, yellow, red).

### 4.4. Dashboard.tsx
**Purpose**: Displays a list of active devices and their electrical metrics.

**State Variables**:
- `data`: Stores the list of active devices.
- `loading`: Indicates whether data is being fetched.

**Functions**:
- `fetchData`: Fetches current device data from the backend and updates the data state.

### 4.5. Layout.tsx
**Purpose**: Provides the general layout for the application, including the sidebar and main content area.

**State Variables**:
- `showSidebar`: Toggles the visibility of the sidebar on mobile devices.

**Features**:
- Responsive design with mobile menu functionality.

## 5. Hooks:

### 5.1. useLLM.ts
**Purpose**: A custom hook to manage communication with the backend's AI service.

**State Variables**:
- `loading`: Indicates whether the message is being sent to the backend.
- `error`: Stores any error messages that occur during communication.

**Functions**:
- `sendMessage`: Sends a message to the backend and returns the AI's response.
- Handles timeouts and API errors gracefully.

## 6. API Integration:
The app communicates with a backend API at the base URL specified in the environment variable VITE_API_BASE_URL.

**Endpoint**: `/api/chat`

**POST Request**: The sendMessage function sends a message to the backend, and the backend responds with a JSON object containing the assistant's reply.

## 7. Styling:
Tailwind CSS is used for styling, with utility classes for responsive design, spacing, colors, and more.

Components like buttons, grids, and text are styled to be responsive and user-friendly.

## 8. Data Flow and Interaction:

**Chat Flow**:
1. The user types a message in the input field and presses the send button.
2. The message is sent to the backend via the useLLM hook.
3. The backend processes the message and responds with relevant information.
4. The message and response are displayed in the ChatInterface.

**Dashboard Flow**:
1. The app fetches device data every 30 seconds using the fetchData function.
2. The ElectricalMetrics component displays real-time data, and the user can expand to view more detailed metrics.

## 9. Conclusion:
This frontend architecture provides an interactive chat interface for monitoring electrical devices through real-time data. The modular components and hooks ensure flexibility and reusability, allowing for easy integration with the backend services.