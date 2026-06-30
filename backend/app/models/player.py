from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.core.database import Base

class PlayerModel(Base):
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(String, primary_key=True) # Cricsheet registry ID is string
    name: Mapped[str] = mapped_column(String, index=True)
