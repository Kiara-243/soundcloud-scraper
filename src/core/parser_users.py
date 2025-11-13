from typing import Any, Dict

def parse_user(user_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a raw SoundCloud user JSON into a structured summary.
    """
    return {
        "id": user_json.get("id"),
        "username": user_json.get("username") or user_json.get("permalink"),
        "full_name": user_json.get("full_name") or user_json.get("name"),
        "city": user_json.get("city"),
        "country_code": user_json.get("country_code"),
        "followers_count": user_json.get("followers_count"),
        "followings_count": user_json.get("followings_count"),
        "track_count": user_json.get("track_count"),
        "verified": user_json.get("verified", False),
        "avatar_url": user_json.get("avatar_url") or user_json.get("avatar_url_template"),
        "permalink_url": user_json.get("permalink_url"),
        "uri": user_json.get("uri"),
    }