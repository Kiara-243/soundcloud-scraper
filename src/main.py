import argparse
import json
import logging
import os
import pathlib
import sys
from typing import Any, Dict, List

# Ensure local src/ modules are importable even when running as a script
CURRENT_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from core.soundcloud_client import SoundCloudClient, SoundCloudClientError  # type: ignore
from core.parser_tracks import parse_track  # type: ignore
from core.parser_users import parse_user  # type: ignore
from core.parser_playlists import parse_playlist  # type: ignore
from core.parser_comments import parse_comments  # type: ignore
from utils.url_validator import classify_url  # type: ignore
from utils.pagination import Paginator  # type: ignore

def setup_logging(level_str: str) -> None:
    level = getattr(logging, level_str.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

def load_json_file(path: pathlib.Path, description: str) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"{description} file not found at: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_settings(path: pathlib.Path) -> Dict[str, Any]:
    defaults: Dict[str, Any] = {
        "log_level": "INFO",
        "user_agent": "SoundCloudScraper/1.0",
        "request_timeout": 10,
        "include_comments": True,
        "end_page": 0,
        "max_items": 0,
        "client_id": None,
    }
    if not path.exists():
        return defaults

    try:
        settings = load_json_file(path, "Settings")
        defaults.update(settings)
        return defaults
    except Exception as exc:  # pragma: no cover - defensive path
        logging.warning("Failed to load settings from %s: %s", path, exc)
        return defaults

def load_inputs(path: pathlib.Path) -> Dict[str, Any]:
    inputs = load_json_file(path, "Input")
    urls = inputs.get("urls") or inputs.get("url_list")
    if not urls or not isinstance(urls, list):
        raise ValueError("Input JSON must contain a non-empty 'urls' array.")
    return inputs

def process_track_url(
    url: str,
    client: SoundCloudClient,
    include_comments: bool,
    paginator: Paginator,
) -> List[Dict[str, Any]]:
    logging.info("Processing track URL: %s", url)
    resolved = client.resolve_url(url)
    if resolved.get("kind") != "track":
        logging.warning("Resolved resource is not a track: kind=%s", resolved.get("kind"))

    track_id = resolved.get("id")
    if track_id is None:
        raise SoundCloudClientError("Could not determine track ID from resolved data.")

    track_json = client.get_track(track_id)
    comments_raw: List[Dict[str, Any]] = []
    if include_comments:
        comments_raw = client.get_all_comments_for_track(track_id, paginator)

    comments = parse_comments(comments_raw) if comments_raw else []
    record = parse_track(track_json, comments=comments)
    return [record]

def process_playlist_url(
    url: str,
    client: SoundCloudClient,
) -> List[Dict[str, Any]]:
    logging.info("Processing playlist/album URL: %s", url)
    resolved = client.resolve_url(url)
    if resolved.get("kind") not in {"playlist", "album"}:
        logging.warning("Resolved resource is not a playlist/album: kind=%s", resolved.get("kind"))

    playlist_id = resolved.get("id")
    if playlist_id is None:
        raise SoundCloudClientError("Could not determine playlist ID from resolved data.")

    playlist_json = client.get_playlist(playlist_id)
    playlist_record = parse_playlist(playlist_json)
    return [playlist_record]

def process_user_url(
    url: str,
    client: SoundCloudClient,
) -> List[Dict[str, Any]]:
    logging.info("Processing user URL: %s", url)
    resolved = client.resolve_url(url)
    if resolved.get("kind") != "user":
        logging.warning("Resolved resource is not a user: kind=%s", resolved.get("kind"))

    user_id = resolved.get("id")
    if user_id is None:
        raise SoundCloudClientError("Could not determine user ID from resolved data.")

    user_json = client.get_user(user_id)
    user_record = parse_user(user_json)
    return [user_record]

def process_search_url(
    url: str,
    client: SoundCloudClient,
    paginator: Paginator,
) -> List[Dict[str, Any]]:
    logging.info("Processing search URL: %s", url)
    classification = classify_url(url)
    search_term = classification.get("search_term")
    if not search_term:
        logging.warning("No search term could be derived from URL: %s", url)
        return []

    tracks = client.search_tracks(search_term, paginator)
    return [parse_track(track) for track in tracks]

def main() -> None:
    default_input = ROOT_DIR / "data" / "inputs.sample.json"
    default_settings = CURRENT_DIR / "config" / "settings.example.json"
    default_output = ROOT_DIR / "data" / "sample_output.json"

    parser = argparse.ArgumentParser(
        description="SoundCloud Scraper - Fetch structured data for SoundCloud URLs."
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(default_input),
        help="Path to input JSON file containing URLs (default: data/inputs.sample.json)",
    )
    parser.add_argument(
        "--settings",
        type=str,
        default=str(default_settings),
        help="Path to settings JSON file (default: src/config/settings.example.json)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(default_output),
        help="Path to output JSON file (default: data/sample_output.json)",
    )
    args = parser.parse_args()

    settings = load_settings(pathlib.Path(args.settings))
    setup_logging(settings.get("log_level", "INFO"))

    inputs = load_inputs(pathlib.Path(args.input))

    include_comments = bool(
        inputs.get("includeComments", settings.get("include_comments", True))
    )
    end_page_raw = inputs.get("endPage", settings.get("end_page", 0))
    max_items_raw = inputs.get("maxItems", settings.get("max_items", 0))

    end_page = int(end_page_raw) if isinstance(end_page_raw, int) else 0
    max_items = int(max_items_raw) if isinstance(max_items_raw, int) and max_items_raw > 0 else None

    paginator = Paginator(end_page=end_page, max_items=max_items)

    client_id = os.getenv("SOUNDCLOUD_CLIENT_ID") or settings.get("client_id")
    timeout = int(settings.get("request_timeout", 10))
    user_agent = str(settings.get("user_agent", "SoundCloudScraper/1.0"))

    client = SoundCloudClient(
        client_id=client_id,
        timeout=timeout,
        user_agent=user_agent,
    )

    results: List[Dict[str, Any]] = []
    urls: List[str] = inputs["urls"]

    for url in urls:
        try:
            classification = classify_url(url)
            if not classification.get("is_valid"):
                logging.warning("Skipping invalid SoundCloud URL: %s", url)
                continue

            resource_type = classification.get("resource_type")
            if resource_type == "track":
                results.extend(process_track_url(url, client, include_comments, paginator))
            elif resource_type in {"playlist", "album"}:
                results.extend(process_playlist_url(url, client))
            elif resource_type == "user":
                results.extend(process_user_url(url, client))
            elif resource_type == "search":
                results.extend(process_search_url(url, client, paginator))
            else:
                logging.warning("Unknown resource type '%s' for URL: %s", resource_type, url)

        except SoundCloudClientError as exc:
            logging.error("SoundCloud client error for URL %s: %s", url, exc)
        except Exception as exc:  # pragma: no cover - defensive
            logging.exception("Unexpected error while processing URL %s: %s", url, exc)

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logging.info("Scraping completed. Wrote %d items to %s", len(results), output_path)

if __name__ == "__main__":
    main()