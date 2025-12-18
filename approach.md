# Assessment Recommendation Engine - Approach Document
**Submitted by:** Antigravity Agent
**Date:** December 18, 2025

## 1. Problem Statement
The objective was to build a Career Path Recommendation Engine that suggests personalized learning paths or courses to users based on their skills, experience, and interests. The solution needed to be deployed as a web application (Streamlit), exposing an API for search functionality, and providing recommendations from a defined product catalog (`catalog.json`).

## 2. Methodology

### 2.1 Data Ingestion & Analysis
The core dataset (`data/catalog.json`) consists of course metadata including Title, Category (e.g., Frontend, Data Science), Difficulty, Provider, and Tags.
- **Analysis:** The data is structured but sparse. A content-based filtering approach was chosen as the most effective method given the lack of historical user interaction data (which would be required for collaborative filtering).

### 2.2 Recommendation Logic
A **Weighted Hybrid Logic** was implemented to score content relevance against a user's profile:
1.  **Category Alignment (Weight: 50)**: Primary filter. If a user's expertise matches the course category, a high base score is assigned.
2.  **Skill overlap (Weight: 15 per tag)**: Secondary filter. Intersection of user's known languages/tools with course tags.
3.  **Heuristic Adjustment**: Minimal randomization (0-10 points) is added to break ties among equally relevant items, providing list variety.

This scoring mechanism ensures that users receive recommendations that are fundamentally aligned with their career goals while favoring specific technologies they already know or want to learn.

### 2.3 System Architecture
The solution is built using a modern Python stack:
- **Frontend**: `Streamlit` for rapid UI development, offering an interactive form for user assessment and immediate visualization of results.
- **Backend API**: `FastAPI` to expose the core logic programmatically.
  - **Endpoint**: `POST /api/v1/recommendations/search` allows external systems to query the video/course database.
  - **Service Layer**: Decoupled `YouTubeService` and `RecommendationService` to separate business logic from HTTP handling.

## 3. Implementation Details

### 3.1 Key Components
- **`app.py`**: The Streamlit entry point. Manages session state for the assessment wizard and renders the recommendation cards.
- **`app/services/youtube_service.py`**: robust service handling external API calls to YouTube (with mock fallback for offline development), integrated into the search feature.
- **`app/routes/recommendations.py`**: RESTful route handler ensuring standard JSON responses for search queries.

### 3.2 Testing & Verification
- **Automated Testing**: A `test_api.py` script verifies the API endpoints using `TestClient`.
- **Manual Verification**: The Streamlit UI was manually verified to ensure the question flow correctly updates the session state and filters the catalog.
- **Prediction set**: A test script `generate_predictions.py` was created to validate the logic against a set of mock candidates (`test_candidates.csv`), producing the `antigravity_agent.csv` results.

## 4. Future Improvements
- **ML Integration**: Replace the weighted logic with a semantic search model (e.g., using embeddings from a transformer model like all-MiniLM-L6-v2) to match user descriptions to course descriptions.
- **User History**: Implement a database table to track user clicks and completions, enabling collaborative filtering (users who liked X also liked Y).
- **Video Previews**: Enhance the UI to show dynamic YouTube video previews for each course using the search API.
