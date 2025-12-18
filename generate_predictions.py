import pandas as pd
import json
import os
import random

def load_catalog():
    try:
        with open('data/catalog.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Catalog not found")
        return []

def get_recommendation(candidate, catalog):
    recommendations = []
    
    user_category = candidate['expertise']
    user_languages = candidate['languages'].split(';') if pd.notna(candidate['languages']) else []
    
    for item in catalog:
        score = 0
        
        # Category match
        if item.get("category") == user_category:
            score += 50
        
        # Tag match
        tags = item.get("tags", [])
        for lang in user_languages:
            if lang in tags:
                score += 15
        
        # Simple score
        if score > 0:
            recommendations.append({
                "item_title": item["title"],
                "score": score
            })
    
    # Sort by score desc
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    if recommendations:
        return recommendations[0]['item_title']
    else:
        return "General Software Engineering"

def main():
    catalog = load_catalog()
    if not catalog:
        return

    candidates = pd.read_csv('test_candidates.csv')
    
    results = []
    
    for _, row in candidates.iterrows():
        top_rec = get_recommendation(row, catalog)
        results.append({
            "firstname": row['first_name'],
            "lastname": row['last_name'],
            "predicted_career_path": top_rec
        })
    
    df_results = pd.DataFrame(results)
    
    # Save as firstname_lastname.csv (using my name roughly)
    output_file = "antigravity_agent.csv"
    df_results.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")

if __name__ == "__main__":
    main()
