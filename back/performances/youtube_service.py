import os
import requests
from django.conf import settings
from django.core.cache import cache
from .models import YouTubeVideoCache, Performance
from django.utils import timezone

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE_PLAYLIST_ID = os.environ.get('YOUTUBE_PLAYLIST_ID_MAIN')
YOUTUBE_API_BASE = 'https://www.googleapis.com/youtube/v3'


def get_playlist_videos(max_results=6):
    """
    Fetch videos from YouTube playlist
    Returns: list of video dicts or empty list on error
    """
    if not YOUTUBE_API_KEY or not YOUTUBE_PLAYLIST_ID:
        return []

    # Check model-based cache first (1 hour)
    cache_obj, created = YouTubeVideoCache.objects.get_or_create(
        cache_key='playlist:main',
        defaults={
            'status': 'NONE',
            'video_data': {'videos': []}
        }
    )

    if not created and cache_obj.is_fresh(max_age_hours=1):
        return cache_obj.video_data.get('videos', [])

    # Call YouTube API
    try:
        url = f"{YOUTUBE_API_BASE}/playlistItems"
        params = {
            'part': 'snippet',
            'playlistId': YOUTUBE_PLAYLIST_ID,
            'maxResults': max_results,
            'key': YOUTUBE_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get('items', []):
            snippet = item.get('snippet', {})
            video_id = snippet.get('resourceId', {}).get('videoId')

            if video_id:
                videos.append({
                    'videoId': video_id,
                    'title': snippet.get('title', ''),
                    'channelTitle': snippet.get('channelTitle', ''),
                    'publishedAt': snippet.get('publishedAt', ''),
                    'thumbnailUrl': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    'youtubeUrl': f'https://www.youtube.com/watch?v={video_id}'
                })

        # Update cache
        cache_obj.status = 'FOUND' if videos else 'NONE'
        cache_obj.video_data = {'videos': videos}
        cache_obj.save()

        return videos

    except Exception as e:
        print(f"YouTube API error: {e}")
        return cache_obj.video_data.get('videos', [])


def search_performance_video(performance_name):
    """
    Search for a single performance video
    Returns: dict with video info or None
    """
    if not YOUTUBE_API_KEY or not performance_name:
        return None

    # Try multiple search queries
    queries = [
        f"{performance_name} 예고편",
        f"{performance_name} 하이라이트",
        f"{performance_name} 공연"
    ]

    for query in queries:
        try:
            url = f"{YOUTUBE_API_BASE}/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'videoEmbeddable': 'true',
                'safeSearch': 'strict',
                'maxResults': 3,
                'key': YOUTUBE_API_KEY
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            items = data.get('items', [])
            if items:
                item = items[0]
                snippet = item.get('snippet', {})
                video_id = item.get('id', {}).get('videoId')

                if video_id:
                    return {
                        'videoId': video_id,
                        'title': snippet.get('title', ''),
                        'channelTitle': snippet.get('channelTitle', ''),
                        'thumbnailUrl': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                        'youtubeUrl': f'https://www.youtube.com/watch?v={video_id}'
                    }
        except Exception as e:
            print(f"Search error for '{query}': {e}")
            continue

    return None


def get_performance_video(performance_id):
    """
    Get or cache performance video
    Returns: dict with status=FOUND/NONE
    """
    try:
        performance = Performance.objects.get(pk=performance_id)
    except Performance.DoesNotExist:
        return {
            'status': 'NONE',
            'youtubeSearchUrl': 'https://www.youtube.com/results?search_query=%EA%B3%B5%EC%97%B0',
            'fallbackPlaylistUrl': f'https://www.youtube.com/playlist?list={YOUTUBE_PLAYLIST_ID}'
        }

    # Check cache (24 hours)
    cache_obj, created = YouTubeVideoCache.objects.get_or_create(
        performance=performance,
        defaults={
            'status': 'NONE',
            'video_data': {},
            'fallback_data': {}
        }
    )

    if not created and cache_obj.is_fresh(max_age_hours=24):
        # Return cached result
        if cache_obj.status == 'FOUND':
            return {
                'status': 'FOUND',
                **cache_obj.video_data
            }
        else:
            return {
                'status': 'NONE',
                **cache_obj.fallback_data
            }

    # Search for video
    video = search_performance_video(performance.prfnm)

    if video:
        # Found video
        cache_obj.status = 'FOUND'
        cache_obj.video_data = video
        cache_obj.fallback_data = None
        cache_obj.save()

        return {
            'status': 'FOUND',
            **video
        }
    else:
        # No video found - create fallback
        import urllib.parse
        search_query = urllib.parse.quote(performance.prfnm)

        fallback = {
            'youtubeSearchUrl': f'https://www.youtube.com/results?search_query={search_query}',
            'fallbackPlaylistUrl': f'https://www.youtube.com/playlist?list={YOUTUBE_PLAYLIST_ID}'
        }

        cache_obj.status = 'NONE'
        cache_obj.video_data = {}
        cache_obj.fallback_data = fallback
        cache_obj.save()

        return {
            'status': 'NONE',
            **fallback
        }
