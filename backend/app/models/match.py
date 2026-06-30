from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date, ForeignKey
from app.core.database import Base

class MatchModel(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season: Mapped[str] = mapped_column(String, index=True)
    match_date: Mapped[date] = mapped_column(Date)
    
    venue_name: Mapped[str] = mapped_column(String)
    venue_city: Mapped[str | None] = mapped_column(String, nullable=True)

    team1_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team2_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    toss_winner_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    toss_decision: Mapped[str] = mapped_column(String)

    outcome_winner_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    outcome_by_runs: Mapped[int | None] = mapped_column(Integer, nullable=True)
    outcome_by_wickets: Mapped[int | None] = mapped_column(Integer, nullable=True)
    outcome_result: Mapped[str | None] = mapped_column(String, nullable=True)
