from typing import Any, Dict, List

def parse_comments(comments_json: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize raw SoundCloud comment objects into the simple structure used by the scraper.
    """
    parsed: List[Dict[str, Any]] = []

    for raw in comments_json:
        user = raw.get("user") or {}
        parsed.append(
            {
                "body": raw.get("body") or raw.get("comment") or "",
                "timestamp": raw.get("timestamp") or raw.get("created_at"),
                "user": {
                    "username": user.get("username") or user.get("permalink") or user.get("name"),
                },
            }
        )

    return parsed