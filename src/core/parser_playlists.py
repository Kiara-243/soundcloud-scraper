from typing import Any, Dict, List

def _simplify_track(track_json: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": track_json.get("id"),
        "title": track_json.get("title"),
        "duration": track_json.get("duration"),
        "permalink_url": track_json.get("permalink_url"),
        "playback_count": track_json.get("playback_count"),
        "likes_count": track_json.get("likes_count"),
        "reposts_count": track_json.get("reposts_count"),
    }

def parse_playlist(playlist_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a raw SoundCloud playlist/album JSON into a structured summary.
    """
    user = playlist_json.get("user") or {}
    tracks_raw: List[Dict[str, Any]] = playlist_json.get("tracks") or []

    tracks = [_simplify_track(t) for t in tracks_raw]

    return {
        "id": playlist_json.get("id"),
        "kind": playlist_json.get("kind"),
        "title": playlist_json.get("title"),
        "description": playlist_json.get("description"),
        "genre": playlist_json.get("genre"),
        "track_count": playlist_json.get("track_count") or len(tracks),
        "duration": playlist_json.get("duration"),
        "permalink_url": playlist_json.get("permalink_url"),
        "release_date": playlist_json.get("release_date"),
        "user": {
            "id": user.get("id"),
            "username": user.get("username") or user.get("permalink"),
            "full_name": user.get("full_name") or user.get("name"),
            "followers_count": user.get("followers_count"),
            "verified": user.get("verified", False),
        },
        "tracks": tracks,
    }