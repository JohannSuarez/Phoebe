from sqlalchemy import Column, String
from .database import Base

class State(Base):
    __tablename__ = "pkce_states"

    state = Column(String(100), primary_key=True, index=True)
    code_verifier = Column(String(100), unique=True, index=True)
