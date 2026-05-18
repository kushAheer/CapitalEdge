from fastapi import APIRouter, HTTPException

from models.schemas import ChatRequest, ChatResponse, ErrorResponse

from session import get_chatbot

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
def chat(request: ChatRequest):
    try:

        if not request.user_id or not request.user_id.strip():
            raise HTTPException(status_code=400, detail="user_id is required.")

        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query is required.")

        chatbot = get_chatbot(request.user_id)

        response = chatbot.chat(request.query)

        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate response.")

        return ChatResponse(answer=response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
