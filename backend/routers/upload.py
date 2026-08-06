import os
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from models.schemas import ErrorResponse, Response, UploadResponse

from session import clear_chatbot, get_chatbot

router = APIRouter(tags=["Upload"])


@router.post("/upload", response_model=UploadResponse, responses={500: {"model": ErrorResponse}})
async def upload_file(user_id: str = Form(...), file: UploadFile = File(...)):
    tmp_path = None

    try:

        if not user_id or not user_id.strip():
            raise HTTPException(status_code=400, detail="user_id is required.")

        if not file:
            raise HTTPException(status_code=400, detail="File is required.")

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="File must be a PDF.")

        chatbot = get_chatbot(user_id)
        content = await file.read()

        if not content:
            raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        chatbot.load_document(tmp_path)
        chunks = chatbot.split_document()
        chatbot.embed_and_store()

        return UploadResponse(filename=file.filename, indexed=True, chunks=len(chunks))

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


@router.post("/upload/clear", response_model=Response, responses={500: {"model": ErrorResponse}})
def clear_file(user_id: str = Form(...)):
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(status_code=400, detail="user_id is required.")

        cleared = clear_chatbot(user_id)

        if not cleared:
            return Response(message="No active uploaded document found to clear.")

        return Response(message="Uploaded document data cleared.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
