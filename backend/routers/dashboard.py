from fastapi import APIRouter, HTTPException

from models.schemas import ErrorResponse


router = APIRouter(tags=["Chat"])


@router.get("/{user_id}", responses={500: {"model": ErrorResponse}})
def get_dashboard(user_id: str):
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(status_code=400, detail="user_id is required.")



        dashboard_data = {
            "user_id": user_id,
            "message": "Dashboard data retrieved successfully."
            # Add more fields as needed
        }

        return dashboard_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))