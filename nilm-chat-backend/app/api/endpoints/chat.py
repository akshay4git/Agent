from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.api.schemas import ChatRequest, ChatResponse
from app.models.chat import ChatSession, ChatMessage
from app.services.llm_service import get_llm_response
from app.api.schemas import MessageResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # Get or create session
    session_id = request.session_id or str(uuid.uuid4())
    db_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    
    if not db_session:
        db_session = ChatSession(session_id=session_id)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
    
    # Save user message
    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()
    
    # Get chat history for context
    history = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp).all()
    
    conversation_history = [(msg.role, msg.content) for msg in history]
    
    # Get response from LLM service
    assistant_response = await get_llm_response(request.message, conversation_history)
    
    # Save assistant response
    assistant_message = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=assistant_response
    )
    db.add(assistant_message)
    db.commit()
    
    return ChatResponse(message=assistant_response, session_id=session_id)

@router.get("/history/{session_id}", response_model=list[MessageResponse])
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp).all()
    
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No chat history found for session {session_id}"
        )
    
    return messages