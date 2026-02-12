from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db
from src.models import Connection, User
from src.schemas import ConnectionCreate, ConnectionResponse, UserResponse
from src.auth.jwt import get_current_user

router = APIRouter()


@router.post("/", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
async def create_connection(
    connection_data: ConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if str(connection_data.user_id) == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create connection with yourself"
        )
    
    target_user = db.query(User).filter(User.id == connection_data.user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    existing = db.query(Connection).filter(
        Connection.follower_id == current_user.id,
        Connection.followed_id == connection_data.user_id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Connection already exists"
        )
    
    connection = Connection(
        follower_id=current_user.id,
        followed_id=connection_data.user_id,
        connection_type=connection_data.connection_type,
        status="pending" if connection_data.connection_type == "friend" else "accepted",
    )
    
    if connection_data.connection_type == "follow":
        connection.accepted_at = datetime.utcnow()
    
    db.add(connection)
    db.commit()
    db.refresh(connection)
    
    return ConnectionResponse(
        id=connection.id,
        follower=UserResponse.model_validate(connection.follower),
        followed=UserResponse.model_validate(connection.followed),
        status=connection.status,
        connection_type=connection.connection_type,
        created_at=connection.created_at,
        accepted_at=connection.accepted_at,
    )


@router.post("/{connection_id}/accept", response_model=ConnectionResponse)
async def accept_connection(
    connection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    connection = db.query(Connection).filter(Connection.id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection request not found")
    
    if str(connection.followed_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to accept this connection"
        )
    
    connection.status = "accepted"
    connection.accepted_at = datetime.utcnow()
    db.commit()
    db.refresh(connection)
    
    return ConnectionResponse(
        id=connection.id,
        follower=UserResponse.model_validate(connection.follower),
        followed=UserResponse.model_validate(connection.followed),
        status=connection.status,
        connection_type=connection.connection_type,
        created_at=connection.created_at,
        accepted_at=connection.accepted_at,
    )


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(
    connection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    connection = db.query(Connection).filter(Connection.id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")
    
    if str(connection.follower_id) != str(current_user.id) and str(connection.followed_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this connection"
        )
    
    db.delete(connection)
    db.commit()
