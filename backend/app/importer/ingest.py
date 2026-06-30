import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from tqdm import tqdm

from app.core.database import SessionLocal
from app.parser.match_parser import MatchParser
from app.models.team import TeamModel
from app.models.player import PlayerModel
from app.models.match import MatchModel
from app.models.innings import InningsModel
from app.models.delivery import DeliveryModel

def load_caches(session: Session):
    teams = session.scalars(select(TeamModel)).all()
    team_cache = {t.name: t for t in teams}
    
    players = session.scalars(select(PlayerModel)).all()
    player_cache = {p.id: p for p in players}
    
    existing_matches = session.execute(
        select(MatchModel.match_date, MatchModel.venue_name)
    ).all()
    match_cache = set((m.match_date, m.venue_name) for m in existing_matches)
    
    return team_cache, player_cache, match_cache

def get_or_create_team_cached(session: Session, team_name: str, cache: dict) -> TeamModel:
    if not team_name:
        return None
    if team_name in cache:
        return cache[team_name]
    team = TeamModel(name=team_name)
    session.add(team)
    session.flush()
    cache[team_name] = team
    return team

def get_or_create_player_cached(session: Session, player_id: str, player_name: str, cache: dict) -> PlayerModel:
    if not player_id:
        return None
    if player_id in cache:
        return cache[player_id]
    player = PlayerModel(id=player_id, name=player_name)
    session.add(player)
    session.flush()
    cache[player_id] = player
    return player

def ingest_data(data_dir: Path):
    parser = MatchParser()
    json_files = list(data_dir.glob("*.json"))
    
    print(f"Found {len(json_files)} JSON files to ingest.")
    
    with SessionLocal() as session:
        session.expire_on_commit = False
        team_cache, player_cache, match_cache = load_caches(session)
        print("Caches loaded.")
        
        for i, file_path in enumerate(tqdm(json_files, desc="Ingesting IPL Matches")):
            try:
                domain_match = parser.parse(file_path)
            except Exception as e:
                continue
            
            match_key = (domain_match.match_date, domain_match.venue.name)
            if match_key in match_cache:
                continue
            
            team1 = get_or_create_team_cached(session, domain_match.teams[0].name, team_cache)
            team2 = get_or_create_team_cached(session, domain_match.teams[1].name, team_cache)
            toss_winner = get_or_create_team_cached(session, domain_match.toss.winner.name, team_cache)
            
            outcome_winner_name = domain_match.outcome.winner.name if domain_match.outcome.winner else None
            outcome_winner = get_or_create_team_cached(session, outcome_winner_name, team_cache) if outcome_winner_name else None
            
            db_match = MatchModel(
                season=domain_match.season,
                match_date=domain_match.match_date,
                venue_name=domain_match.venue.name,
                venue_city=domain_match.venue.city,
                team1_id=team1.id,
                team2_id=team2.id,
                toss_winner_id=toss_winner.id,
                toss_decision=domain_match.toss.decision,
                outcome_winner_id=outcome_winner.id if outcome_winner else None,
                outcome_by_runs=domain_match.outcome.by_runs,
                outcome_by_wickets=domain_match.outcome.by_wickets,
                outcome_result=domain_match.outcome.result
            )
            session.add(db_match)
            session.flush() 
            match_cache.add(match_key)
            
            deliveries_to_insert = []
            
            for inn_idx, domain_inning in enumerate(domain_match.innings):
                bat_team = get_or_create_team_cached(session, domain_inning.batting_team.name, team_cache)
                bowl_team_name = team2.name if bat_team.name == team1.name else team1.name
                bowl_team = get_or_create_team_cached(session, bowl_team_name, team_cache)
                
                db_inning = InningsModel(
                    match_id=db_match.id,
                    innings_number=inn_idx + 1,
                    batting_team_id=bat_team.id,
                    bowling_team_id=bowl_team.id
                )
                session.add(db_inning)
                session.flush()
                
                for over in domain_inning.overs:
                    for delivery in over.deliveries:
                        batter = get_or_create_player_cached(session, delivery.batter.registry_id, delivery.batter.name, player_cache)
                        bowler = get_or_create_player_cached(session, delivery.bowler.registry_id, delivery.bowler.name, player_cache)
                        non_striker = get_or_create_player_cached(session, delivery.non_striker.registry_id, delivery.non_striker.name, player_cache)
                        
                        player_out_id = None
                        if delivery.wicket:
                            player_out = get_or_create_player_cached(session, delivery.wicket.player_out.registry_id, delivery.wicket.player_out.name, player_cache)
                            player_out_id = player_out.id
                            
                        del_num = int(float(delivery.ball) * 10) % 10
                            
                        batter_id = delivery.batter.registry_id
                        bowler_id = delivery.bowler.registry_id
                        non_striker_id = delivery.non_striker.registry_id
                        
                        db_delivery = DeliveryModel(
                            innings_id=db_inning.id,
                            over_number=over.number,
                            delivery_number=del_num,
                            ball=delivery.ball,
                            batter_id=batter_id,
                            bowler_id=bowler_id,
                            non_striker_id=non_striker_id,
                            batter_runs=delivery.batter_runs,
                            extras=delivery.extras,
                            total_runs=delivery.total_runs,
                            is_wicket=True if delivery.wicket else False,
                            player_out_id=player_out_id,
                            wicket_kind=delivery.wicket.kind if delivery.wicket else None
                        )
                        deliveries_to_insert.append(db_delivery)
            
            if deliveries_to_insert:
                session.bulk_save_objects(deliveries_to_insert)
            
            # Commit every 10 matches to save memory and avoid huge transactions
            if i % 10 == 0:
                session.commit()
                
        # Final commit
        session.commit()

if __name__ == "__main__":
    data_dir = Path(r"D:\ML_Project\CricketSim\backend\data\raw\ipl")
    print(f"Starting ingestion from {data_dir}")
    ingest_data(data_dir)
