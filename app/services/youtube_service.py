import os
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime

class YouTubeService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def search_videos(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if not self.api_key:
            # Return mock data if no API key is present (for testing/dev)
            return self._get_mock_videos(query, max_results)

        try:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video_data = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': datetime.fromisoformat(item['snippet']['publishedAt'].replace('Z', '+00:00')),
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url']
                }
                videos.append(video_data)
                
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return self._get_mock_videos(query, max_results)

    def _get_mock_videos(self, query: str, limit: int) -> List[Dict[str, Any]]:
        # Mock data for when API fails or no key
        return [
            {
                'video_id': f'mock_{i}',
                'title': f'Mock Video Result for {query} {i+1}',
                'description': f'This is a mock video description for result {i+1}',
                'published_at': datetime.now(),
                'channel_id': 'mock_channel',
                'channel_title': 'Mock Channel',
                'thumbnail_url': 'https://via.placeholder.com/320x180'
            }
            for i in range(limit)
        ]
