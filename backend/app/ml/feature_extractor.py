import pandas as pd
from sqlalchemy import create_engine
from app.core.config import settings

def extract_raw_deliveries():
    engine = create_engine(settings.DATABASE_URL)
    query = """
    SELECT 
        d.id,
        m.season,
        m.match_date,
        i.innings_number,
        d.over_number,
        d.delivery_number,
        d.batter_id,
        d.bowler_id,
        d.non_striker_id,
        d.batter_runs,
        d.extras,
        d.total_runs,
        d.is_wicket,
        d.wicket_kind
    FROM deliveries d
    JOIN innings i ON d.innings_id = i.id
    JOIN matches m ON i.match_id = m.id
    ORDER BY m.match_date ASC, i.innings_number ASC, d.over_number ASC, d.delivery_number ASC
    """
    df = pd.read_sql(query, engine)
    return df

def build_features(df: pd.DataFrame):
    """
    Builds the contextual features for the ML model.
    """
    # Create target variable (0, 1, 2, 3, 4, 6, Wicket=7, Extra=8)
    def categorize_outcome(row):
        if row['is_wicket']:
            return 'wicket'
        elif row['extras'] > 0:
            return 'extra'
        else:
            return str(row['batter_runs'])
            
    df['outcome'] = df.apply(categorize_outcome, axis=1)
    
    # Calculate rolling batter stats (Strike Rate, Avg)
    # Note: For a real simulator, we want season-level aggregates, but for now we'll do simple cumulative stats
    # Group by batter, cumulative sum of runs and balls
    df['is_valid_ball'] = (df['extras'] == 0).astype(int)
    
    batter_stats = df.groupby(['season', 'batter_id']).agg(
        total_runs=('batter_runs', 'sum'),
        total_balls=('is_valid_ball', 'sum'),
        total_dismissals=('is_wicket', 'sum')
    ).reset_index()
    
    batter_stats['strike_rate'] = (batter_stats['total_runs'] / batter_stats['total_balls'].replace(0, 1)) * 100
    batter_stats['average'] = batter_stats['total_runs'] / batter_stats['total_dismissals'].replace(0, 1)
    
    # Merge stats back to main df.
    # CRITICAL: Shift the season back by 1 so we predict based on *past* season performance, not current!
    # For now, we will just use the current season's stats as a proxy if past doesn't exist, but we must be careful with data leakage.
    
    # Let's keep it simple for V1:
    # We will just train a model that looks at match context: over_number, innings, wickets lost, current score
    
    # Cumulative Score and Wickets per innings
    df['innings_runs'] = df.groupby(['match_date', 'innings_number'])['total_runs'].cumsum()
    df['innings_wickets'] = df.groupby(['match_date', 'innings_number'])['is_wicket'].cumsum()
    
    features = [
        'batter_id',
        'bowler_id',
        'innings_number',
        'over_number',
        'delivery_number',
        'innings_runs',
        'innings_wickets'
    ]
    
    X = df[features]
    y = df['outcome']
    
    return X, y

if __name__ == "__main__":
    print("Extracting raw deliveries from DB...")
    df = extract_raw_deliveries()
    print(f"Extracted {len(df)} deliveries.")
    X, y = build_features(df)
    print("Features built successfully.")
