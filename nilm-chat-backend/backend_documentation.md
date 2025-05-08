# Backend Documentation

## Overview

This backend is designed for a system that processes and manages electrical data from multiple devices in real-time. The backend handles data import, database management, and AI-driven responses based on real-time device data. The system utilizes FastAPI for the API layer and SQLAlchemy for database operations, with a machine learning model to provide insights and respond to user queries regarding electrical consumption.

## Architecture

### Components

- **FastAPI**: Framework used for the backend API.
- **SQLAlchemy**: ORM used to manage the database.
- **PyTorch**: Used for machine learning, specifically with the FLAN-T5 model.
- **PostgreSQL** (or another database like SQLite): Used for data storage.

### Modules Overview

#### 1. `app/api/models/chat.py`
Defines two database models for the chat system:

- **ChatSession**: Manages chat session details (e.g., session ID, creation time, last active time).
- **ChatMessage**: Stores messages for each chat session, including content and sender (user or assistant).

#### 2. `app/models/electrical_data.py`
Defines the `ElectricalData` model that stores all the electrical measurements from the devices. It includes various columns for power, voltage, current, frequency, etc., as well as new fields like device state and cluster ID.

#### 3. `app/services/data_service.py`
Handles the processing and extraction of real devices from the dataset.

The function `get_actual_devices` filters the data for devices that are active within the last 24 hours and calculates the average power and THD for each device.

#### 4. `app/services/device_services.py`
Provides a service for getting the most common device state per cluster and for calculating power and THD averages per cluster.

Includes the `get_cluster_summaries` function that generates a summary of the devices in each cluster, including power and THD information.

#### 5. `app/services/llm_service.py`
This service handles the AI model used for generating responses to user queries based on real-time electrical data.

- The `LLMService` class loads the FLAN-T5 model, initializes the tokenizer, and generates responses.
- The AI system generates responses based on real-time device information, such as power and THD data.
- The system maintains a conversation history to provide context for the responses.

#### 6. `/scripts/import_csv_data.py`
This script is responsible for importing electrical data from a CSV file into the database. It handles:

- Data reading, cleaning, and preprocessing.
- Batch importing data to avoid overloading the database.
- Data validation and logging for successful and failed imports.

#### 7. `/scripts/create_tables.py`
This script initializes the database by creating the necessary tables (like `chat_sessions`, `chat_messages`, and `electrical_data`) based on the models defined in SQLAlchemy.

#### 8. `/scripts/reset_db.py`
This script resets the database, which can be useful during development or for clearing old data. It deletes all records from the relevant tables, ensuring the database is clean.

## Endpoints Overview

### 1. `/api/chat/`
**POST**: Send a user message and receive a response from the assistant.

**Request Body**:
- `user_message`: The message from the user.
- `conversation_history`: The history of the conversation to provide context.

**Response**:
- The generated response from the assistant.
- A list of devices mentioned in the response.
- Confidence score (0-1) indicating how well the response aligns with the available data.

### 2. `/api/devices/`
**GET**: Retrieve a list of active devices in the system.

**Response**:
- A list of active devices, including:
  - Device name
  - Average power usage
  - Average Total Harmonic Distortion (THD)
  - Last seen timestamp

### 3. `/api/devices/summary/`
**GET**: Retrieve a summary of devices by cluster.

**Response**:
- A list of clusters with device names, average power, and THD.

## Configuration

### Environment Variables
- `DEVICE`: Specifies the device used for running the model (e.g., cuda or cpu).
- `MODEL_NAME`: The name of the model (FLAN-T5).
- `MODEL_CACHE_TIMEOUT`: The timeout duration for the cached model.
- `MAX_CONVERSATION_HISTORY`: The number of conversation history entries to keep for context.
- `MAX_NEW_TOKENS`: The maximum number of tokens to generate in a response.

### Dependencies
- `fastapi`: Web framework for building APIs.
- `sqlalchemy`: ORM for managing database interactions.
- `torch`: PyTorch framework for running machine learning models.
- `transformers`: Library to load and run the FLAN-T5 model.

## Database Schema

### `chat_sessions`
- `id`: Primary key.
- `session_id`: Unique session ID.
- `created_at`: Timestamp when the session was created.
- `last_active`: Timestamp when the session was last active.

### `chat_messages`
- `id`: Primary key.
- `session_id`: Foreign key to the `chat_sessions` table.
- `role`: Role of the sender (user or assistant).
- `content`: The content of the message.
- `timestamp`: Timestamp when the message was sent.

### `electrical_data`
- `id`: Primary key.
- `timestamp`: Timestamp of the data entry.
- `voltage`, `current`, `real_power`, `reactive_power`, `apparent_power`, `power_factor`, `frequency`, `thd`: Measurement fields.
- `real_power_watt`: Real power in watts.
- `cluster`: The cluster ID to group similar devices.
- `device_state`: The state of the device (e.g., "on", "off", etc.).

## Setup and Installation

### 1. Install Dependencies
Run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Create the Database Tables
To create the necessary database tables, run the following script:

```bash
python scripts/create_tables.py
```

### 3. Import Data
To import data from a CSV file, use the following script:

```bash
python scripts/import_csv_data.py <file_path>
```

### 4. Reset the Database
To reset the database (clear all data), run the following script:

```bash
python scripts/reset_db.py
```

## Conclusion

This backend system efficiently manages real-time electrical data, processes it for meaningful insights, and responds to user queries with the help of an AI model. With batch data imports, database management, and machine learning, the system is designed for performance and scalability.