import json
from typing import List, Tuple, Optional
import httpx
import asyncio
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from app.config import settings
from app.utils.prompt_templates import SYSTEM_PROMPT
from app.services.data_service import get_recent_metrics_summary

# Global variables to hold the model and tokenizer
model = None
tokenizer = None

async def initialize_model():
    """Initialize the Flan-T5 model and tokenizer"""
    global model, tokenizer
    
    if model is None or tokenizer is None:
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(settings.MODEL_NAME)
        
        # Move model to the specified device
        device = torch.device(settings.DEVICE)
        model = model.to(device)
    
    return model, tokenizer

async def get_llm_response(
    user_message: str,
    conversation_history: List[Tuple[str, str]],
    max_history: int = 5
) -> str:
    """Get a response from the LLM based on the user message and conversation history"""
    # Get electrical metrics data for context
    metrics_data = await get_recent_metrics_summary()
    metrics_context = json.dumps(metrics_data)
    
    # Prepare the prompt with system message, metrics, and history
    if settings.LLM_PROVIDER == "flan-t5":
        response = await get_flan_t5_response(user_message, conversation_history, metrics_context, max_history)
    elif settings.LLM_PROVIDER == "openai":
        response = await get_openai_response(user_message, conversation_history, metrics_context, max_history)
    elif settings.LLM_PROVIDER == "anthropic":
        response = await get_anthropic_response(user_message, conversation_history, metrics_context, max_history)
    else:
        # Fallback to a simple response if no provider is configured
        response = "I'm sorry, but I don't have enough information to answer your question about electrical usage at this time."
    
    return response

async def get_flan_t5_response(
    user_message: str,
    conversation_history: List[Tuple[str, str]],
    metrics_context: str,
    max_history: int = 5
) -> str:
    """Get response from Flan-T5 model"""
    try:
        # Initialize the model and tokenizer
        model, tokenizer = await initialize_model()
        
        # Format the system prompt with metrics context
        system_prompt = SYSTEM_PROMPT.format(metrics_context=metrics_context)
        
        # Construct input prompt
        prompt = f"System: {system_prompt}\n\n"
        
        # Add the most recent conversation history
        limited_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history
        
        for role, content in limited_history:
            if role == "user":
                prompt += f"User: {content}\n"
            else:
                prompt += f"Assistant: {content}\n"
        
        # Add the current user message if it's not already included in the history
        if not conversation_history or conversation_history[-1][0] != "user" or conversation_history[-1][1] != user_message:
            prompt += f"User: {user_message}\n"
        
        prompt += "Assistant:"
        
        # Encode the input
        device = torch.device(settings.DEVICE)
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
        
        # Generate response
        outputs = model.generate(
            input_ids=input_ids,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            temperature=settings.TEMPERATURE,
            do_sample=True,
            top_p=0.95,
            num_return_sequences=1
        )
        
        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove any remaining prompt text
        assistant_prefix = "Assistant:"
        if response.startswith(assistant_prefix):
            response = response[len(assistant_prefix):].strip()
        
        return response
    
    except Exception as e:
        print(f"Error using Flan-T5 model: {str(e)}")
        return f"I'm sorry, I encountered an error processing your request. Please try again later."

async def get_openai_response(
    user_message: str,
    conversation_history: List[Tuple[str, str]],
    metrics_context: str,
    max_history: int = 5
) -> str:
    """Get response from OpenAI API"""
    import openai
    
    # Set API key
    openai.api_key = settings.OPENAI_API_KEY
    
    # Prepare the messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(metrics_context=metrics_context)}
    ]
    
    # Add the most recent conversation history
    limited_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history
    
    for role, content in limited_history:
        messages.append({"role": role, "content": content})
    
    # Add the current user message if it's not already included in the history
    if not conversation_history or conversation_history[-1][0] != "user" or conversation_history[-1][1] != user_message:
        messages.append({"role": "user", "content": user_message})
    
    try:
        # Make request to OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=settings.MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return f"I'm sorry, I encountered an error processing your request. Please try again later."

async def get_anthropic_response(
    user_message: str,
    conversation_history: List[Tuple[str, str]],
    metrics_context: str,
    max_history: int = 5
) -> str:
    """Get response from Anthropic Claude API"""
    # Construct the prompt for Claude
    system_prompt = SYSTEM_PROMPT.format(metrics_context=metrics_context)
    
    # Create a conversation string for Claude
    conversation = f"<system>\n{system_prompt}\n</system>\n\n"
    
    # Add the most recent conversation history
    limited_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history
    
    for role, content in limited_history:
        if role == "user":
            conversation += f"\n\nHuman: {content}"
        else:
            conversation += f"\n\nAssistant: {content}"
    
    # Add the current user message if it's not already included in the history
    if not conversation_history or conversation_history[-1][0] != "user" or conversation_history[-1][1] != user_message:
        conversation += f"\n\nHuman: {user_message}"
    
    conversation += "\n\nAssistant:"
    
    try:
        # Make request to Anthropic API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": settings.MODEL_NAME,
                    "messages": [
                        {"role": "user", "content": conversation}
                    ],
                    "max_tokens": 800
                }
            )
            
            response_data = response.json()
            return response_data["content"][0]["text"]
    except Exception as e:
        print(f"Error calling Anthropic API: {str(e)}")
        return f"I'm sorry, I encountered an error processing your request. Please try again later."