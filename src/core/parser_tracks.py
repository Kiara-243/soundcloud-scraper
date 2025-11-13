from typing import Any, Dict, List, Optional

def _extract_user(user_json: Dict[str, Any]) -> Dict[str, Any]:
    if not user_json:
        return {}

    return {
        "username": user_json.get("username") or user_json.get("permalink"),
        "full_name": user_json.get("full_name") or user_json.get("name"),
        "followers_count": user_json.get("followers_count"),
        "verified": user_json.get("verified", False),
        "avatar_url": user_json.get("avatar_url") or user_json.get("avatar_url_template"),
        "id": user_json.get("id"),
        "uri": user_json.get("uri"),
    }

def parse_track(
    track_json: Dict[str, Any],
    comments: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Convert a raw SoundCloud track JSON into the structured form documented in the README.
    """
    comments = comments or []

    user_json = track_json.get("user") or {}
    user = _extract_user(user_json)

    media = track_json.get("media") or {}
    artwork_url = track_json.get("artwork_url") or track_json.get("artwork_url_template")

    comment_count = track_json.get("comment_count")
    if comment_count is None and comments:
        comment_count = len(comments)

    result: Dict[str, Any] = {
        "artwork_url": artwork_url,
        "caption": track_json.get("caption") or "",
        "comment_count": comment_count,
        "created_at": track_json.get("created_at"),
        "description": track_json.get("description") or "",
        "duration": track_json.get("duration"),
        "genre": track_json.get("genre"),
        "id": track_json.get("id"),
        "likes_count": track_json.get("likes_count"),
        "permalink_url": track_json.get("permalink_url"),
        "playback_count": track_json.get("playback_count"),
        "purchase_url": track_json.get("purchase_url") or track_json.get("purchase_title"),
        "reposts_count": track_json.get("reposts_count"),
        "title": track_json.get("title"),
        "uri": track_json.get("uri"),
        "user": {
            "username": user.get("username"),
            "followers_count": user.get("followers_count"),
            "verified": user.get("verified"),
        },
        "comments": comments,
        "media": media,
    }

    return result