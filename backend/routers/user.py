from bson import ObjectId
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from models.schemas import ErrorResponse, UserLogin, UserRegister, UserResponse
from passlib.context import CryptContext
from database import users_collection

router = APIRouter(tags=["User"])

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserResponse, responses={500: {"model": ErrorResponse}})
async def register(request: UserRegister):
    try:
        name = request.name.strip()
        email = str(request.email).strip().lower()
        password = request.password

        if not name:
            raise HTTPException(status_code=400, detail="Name is required.")

        existing_user = await users_collection.find_one({"email": email})

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered.")

        hashed_password = password_context.hash(password)

        result = await users_collection.insert_one({
            "name": name,
            "email": email,
            "password_hash": hashed_password,
            "created_at": datetime.now(timezone.utc),
        })

        return UserResponse(
            user_id=str(result.inserted_id),
            name=name,
            email=email,
        )

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/login", response_model=UserResponse, responses={500: {"model": ErrorResponse}})
async def login(request: UserLogin):
    try:
        email = str(request.email).strip().lower()
        password = request.password

        user = await users_collection.find_one({"email": email})

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

        password_valid = password_context.verify(
            password,
            user["password_hash"],
        )

        if not password_valid:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

        return UserResponse(
            user_id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
        )

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/users/{user_id}", response_model=UserResponse, responses={500: {"model": ErrorResponse}})
async def get_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user_id.")

        user = await users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        return UserResponse(
            user_id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
        )

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
