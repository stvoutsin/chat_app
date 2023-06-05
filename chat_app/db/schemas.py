from typing import List
from pydantic import BaseModel

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class UserID(OurBaseModel):
    id: int

class UserBase(OurBaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class RegisterValidator(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class FriendBase(OurBaseModel):
    user_id: int
    friend_id: int

class FriendCreate(FriendBase):
    pass

class Friend(FriendBase):
    friend_id: int

    class Config:
        orm_mode = True

class Friendship(OurBaseModel):
    user_id: int
    friend_id: int

class ResponseMessage(OurBaseModel):
    success: bool
    message: str
    def __repr__(self):
        return {"success": self.success,
                "message": self.message}

    def __str__(self):
        return {"success": self.success,
                "message": self.message}



class ChatBase(OurBaseModel):
    user_id: int
    friend_id: int


class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int

class ChatMessage(OurBaseModel):
    sender_id: int
    message: str
    chat_id: int
    created_at: str

class MessageCreate(ChatMessage):
    pass


class MessageUpdate(ChatMessage):
    pass

class ChatHistoryResponse(OurBaseModel):
    messages: List[ChatMessage]
