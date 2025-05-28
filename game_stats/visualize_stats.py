"""
Script to visualize game statistics from CSV files.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import glob

def calculate_scores(df):
    """Calculate scores for each player based on the scoring system."""
    # Calculate points for each category
    df['survival_points'] = (df['seconds_survived'])//3 * 1  # +1 point per 3 seconds
    df['laser_hit_points'] = df['laser_hits'] * 5  # +5 points per laser hit
    df['life_lost_penalty'] = df['lives_lost'] * -5  # -5 points per life lost
    df['last_survivor_bonus'] = df['is_last_surviving'].astype(int) * 25  # +25 points if last surviving
    
    # Calculate total score
    df['total_score'] = (df['survival_points'] + 
                        df['laser_hit_points'] + 
                        df['life_lost_penalty'] + 
                        df['last_survivor_bonus'])
    
    return df

def create_visualization(df, timestamp):
    """Create and save the visualization."""
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Game Statistics Analysis', fontsize=16, y=0.95)
    
    # Sort players by total score
    player_scores = df.groupby('player_id')['total_score'].sum().sort_values(ascending=True)
    winner = player_scores.index[-1]
    
    # Plot 1: Total Scores (Horizontal Bar Chart)
    ax1.barh(player_scores.index, player_scores.values)
    ax1.set_title(f'Overall Winner: {winner}\nTotal Scores per Player')
    ax1.set_xlabel('Total Score')
    ax1.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Plot 2: Score Breakdown (Grouped Bar Chart)
    categories = ['survival_points', 'laser_hit_points', 'life_lost_penalty', 'last_survivor_bonus']
    category_labels = ['Survival', 'Laser Hits', 'Life Lost', 'Last Survivor']
    
    # Calculate category totals for each player
    category_totals = df.groupby('player_id')[categories].sum()
    
    # Set up the grouped bar chart
    x = range(len(player_scores.index))
    width = 0.2
    
    for i, (category, label) in enumerate(zip(categories, category_labels)):
        offset = (i - 1.5) * width
        ax2.bar([xi + offset for xi in x], 
                category_totals[category].reindex(player_scores.index),
                width, label=label)
    
    ax2.set_title('Score Breakdown by Category')
    ax2.set_xticks(x)
    ax2.set_xticklabels(player_scores.index, rotation=45)
    ax2.set_ylabel('Points')
    ax2.legend()
    ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout and save
    plt.tight_layout()
    output_filename = os.path.join('game_stats', f"{timestamp}_stats.png")
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Visualization saved as: {output_filename}")

def main():
    # Find the most recent CSV file in the game_stats directory
    csv_files = glob.glob('game_stats/*_gamestats.csv')
    if not csv_files:
        print("No game statistics files found in the game_stats directory!")
        return
        
    # Get the most recent file
    latest_file = max(csv_files, key=os.path.getctime)
    print(f"Processing file: {latest_file}")
    
    # Extract timestamp from filename
    timestamp = os.path.basename(latest_file).split('_gamestats.csv')[0]
    
    # Read and process the data
    df = pd.read_csv(latest_file)
    df = calculate_scores(df)
    
    # Create and save visualization
    create_visualization(df, timestamp)

if __name__ == "__main__":
    main() 