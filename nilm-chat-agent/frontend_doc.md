# NILM Chat Backend Documentation (with Flan-T5 Integration)

This documentation outlines the backend architecture and implementation of the NILM Chat system, supporting both traditional LLM APIs (OpenAI, Anthropic) and HuggingFace's Flan-T5 models. It provides database models, endpoints, core services, frontend integration, and configuration strategies.

---

## 📁 Project Structure

```
nilm-chat-backend/
├── app/
│   ├── main.py               # Entry point for FastAPI
│   ├── config.py             # App and environment configuration
│   ├── database.py           # SQLAlchemy database setup
│   ├── models/               # SQLAlchemy ORM models
│   ├── api/                  # API route definitions
│   ├── services/             # Business logic (LLM, data summary, etc.)
│   └── utils/                # Prompt templates and utilities
├── scripts/                  # Data seeding and CSV import scripts
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (local)
├── .env.example              # Example environment file
└── tests/                    # Integration and unit tests
```

---

## ⚙️ Environment Setup

### Python Dependencies

Install core and Flan-T5-related packages:

```bash
pip install -r requirements.txt
```

**Key Dependencies:**

- FastAPI, Uvicorn (API)
- SQLAlchemy, Pydantic (ORM, validation)
- Transformers, Torch, Accelerate (Flan-T5)
- httpx, dotenv, pandas

### `.env` Configuration

```env
DATABASE_URL=sqlite:///./nilm_chat.db
LLM_PROVIDER=flan-t5
MODEL_NAME=google/flan-t5-large
DEVICE=cpu
MAX_NEW_TOKENS=512
TEMPERATURE=0.7
```

---

## 🗃️ Database Models

### `ElectricalData`

```python
class ElectricalData(Base):
    __tablename__ = "electrical_data"
    ...
```

### `ChatSession` & `ChatMessage`

```python
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    ...

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    ...
```

---

## 🧠 LLM Integration

### Initialization in `main.py`

```python
@app.on_event("startup")
async def startup_event():
    if settings.LLM_PROVIDER == "flan-t5":
        await initialize_model()
```

### `get_llm_response()`

```python
async def get_llm_response(user_message, conversation_history, max_history=5):
    ...
```

### `get_flan_t5_response()`

```python
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
outputs = model.generate(...)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

---

## 🔌 API Endpoints

### Chat Endpoints

```python
@router.post("/", response_model=ChatResponse)
async def chat_with_assistant(...):
    ...
```

### Metrics Endpoints

```python
@router.get("/summary", response_model=MetricsSummary)
async def get_metrics_summary(...):
    ...
```

### Devices Endpoints

```python
@router.get("/", response_model=List[DeviceInfo])
async def get_all_devices(...):
    ...
```

---

## 🌐 Frontend Integration Guide

The frontend (React + TypeScript) communicates with the backend via RESTful endpoints defined above.

### Chat Integration

- `POST /api/chat/` is called by `useLLM.ts` hook in the frontend.
- Responses are rendered via `ChatInterface.tsx` and `Message.tsx`.

```tsx
const { sendMessage } = useLLM();
await sendMessage("What's my power usage?");
```

### Dashboard Integration

- `GET /api/metrics/summary` and `GET /api/devices/` are polled by `Dashboard.tsx`.
- `ElectricalMetrics.tsx` handles display per device.

```tsx
useEffect(() => {
  fetch(`${API_URL}/metrics/summary`).then(...);
  fetch(`${API_URL}/devices/`).then(...);
}, []);
```

### Environment Setup

Frontend expects the following environment vars:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK_DATA=false
```

To use mock data, set `VITE_USE_MOCK_DATA=true`.

### Cross-Origin

CORS settings in backend `.env`:

```python
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]
```

Ensure these match frontend dev ports.

---

## 📈 Metrics Summary Service

### `get_recent_metrics_summary()`

Returns structured JSON for:

- device list
- average power
- THD
- power factor
- last update timestamp

---

## 🧪 Testing

### Sample Test

```python
def test_chat_endpoint():
    ...
```

Run tests:

```bash
pytest tests/
```

---

## 📥 Data Seeding and Import

```python
def generate_sample_data():
    ...
```

```python
for _, row in df.iterrows():
    ...
```

---

## 🚀 Running the Backend

```bash
uvicorn app.main:app --reload
```

Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Prompt Engineering

```python
SYSTEM_PROMPT = """You are an assistant... Devices: {metrics_context}"""
```

---

## 🧠 Model Performance Notes

| Model           | RAM Needed | Device Recommended |
| --------------- | ---------- | ------------------ |
| `flan-t5-base`  | 2–4 GB     | CPU                |
| `flan-t5-large` | 4–8 GB     | CPU / GPU (CUDA)   |
| `flan-t5-xl`    | 8–16 GB    | GPU preferred      |
| `flan-t5-xxl`   | 16–32 GB   | High-end GPU only  |

---

## ✅ Future Enhancements

- WebSocket support for real-time updates
- User authentication and RBAC
- Time-series trend analysis and anomaly detection
- Fine-tuned LLM integration with NILM-specific dataset

