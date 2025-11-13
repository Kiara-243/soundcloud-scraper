from typing import Any, Dict
from urllib.parse import parse_qs, urlparse

def classify_url(url: str) -> Dict[str, Any]:
    """
    Validate and classify a SoundCloud URL into one of:
    - track
    - playlist
    - album
    - user
    - search
    - unknown
    """
    parsed = urlparse(url)

    result: Dict[str, Any] = {
        "is_valid": False,
        "resource_type": "unknown",
        "normalized_url": url,
        "search_term": None,
    }

    if not parsed.scheme.startswith("http"):
        return result

    host = (parsed.netloc or "").lower()
    if "soundcloud.com" not in host:
        return result

    path_parts = [p for p in (parsed.path or "").split("/") if p]
    query_params = parse_qs(parsed.query or "")

    # Detect search URLs
    if "search" in path_parts or "q" in query_params:
        q_vals = query_params.get("q") or []
        search_term = q_vals[0] if q_vals else None
        result.update(
            {
                "is_valid": True,
                "resource_type": "search",
                "search_term": search_term,
            }
        )
        return result

    # Patterns:
    # /{user_slug}/{track_slug}
    # /{user_slug}/sets/{playlist_slug}
    # /{user_slug}/albums/{album_slug}
    # /{user_slug}
    resource_type = "unknown"

    if len(path_parts) >= 3 and path_parts[1] in {"sets", "albums"}:
        resource_type = "playlist" if path_parts[1] == "sets" else "album"
    elif len(path_parts) >= 2:
        resource_type = "track"
    elif len(path_parts) == 1:
        resource_type = "user"

    result.update(
        {
            "is_valid": True,
            "resource_type": resource_type,
        }
    )
    return result