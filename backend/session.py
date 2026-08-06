from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai import ChatBot

_sessions : dict[str, ChatBot] = {}

def get_chatbot(user_id: str) -> ChatBot:
    """
    Returns or creates a ChatBot instance for the given user ID.
    """
    from ai import ChatBot

    if user_id not in _sessions:
        _sessions[user_id] = ChatBot(user_id)
    return _sessions[user_id]

def clear_chatbot(user_id: str) -> bool:
    """
    Clears the ChatBot for the given user ID.
    """
    if user_id in _sessions:
        _sessions[user_id].clear_user_data()
        del _sessions[user_id]
        return True
    return False
