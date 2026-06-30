from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Boolean
from app.core.database import Base

class DeliveryModel(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    innings_id: Mapped[int] = mapped_column(ForeignKey("innings.id"))
    
    over_number: Mapped[int] = mapped_column(Integer)
    delivery_number: Mapped[int] = mapped_column(Integer)
    ball: Mapped[str] = mapped_column(String) # e.g. '0.1'

    batter_id: Mapped[str] = mapped_column(ForeignKey("players.id"))
    bowler_id: Mapped[str] = mapped_column(ForeignKey("players.id"))
    non_striker_id: Mapped[str] = mapped_column(ForeignKey("players.id"))

    batter_runs: Mapped[int] = mapped_column(Integer)
    extras: Mapped[int] = mapped_column(Integer)
    total_runs: Mapped[int] = mapped_column(Integer)

    is_wicket: Mapped[bool] = mapped_column(Boolean, default=False)
    player_out_id: Mapped[str | None] = mapped_column(ForeignKey("players.id"), nullable=True)
    wicket_kind: Mapped[str | None] = mapped_column(String, nullable=True)
