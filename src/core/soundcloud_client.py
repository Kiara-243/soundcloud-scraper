import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

class SoundCloudClientError(Exception):
    """Base exception for SoundCloud client failures."""

@dataclass
class SoundCloudClient:
    """
    Thin wrapper around the public SoundCloud API.

    A valid client_id is required for most endpoints. Provide it via:
    - ctor argument client_id, or
    - environment variable SOUNDCLOUD_CLIENT_ID (resolved by caller).
    """

    client_id: Optional[str] = None
    base_url: str = "https://api-v2.soundcloud.com"
    timeout: int = 10
    user_agent: str = "SoundCloudScraper/1.0"

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.user_agent,
                "Accept": "application/json, text/plain, */*",
            }
        )
        if not self.client_id:
            logger.warning(
                "No SoundCloud client_id configured. Network calls will fail against "
                "endpoints that require authentication."
            )

    # -----------------------
    # Low-level HTTP helpers
    # -----------------------
    def _ensure_client_id(self) -> str:
        if not self.client_id:
            raise SoundCloudClientError(
                "SOUNDCLOUD_CLIENT_ID is not set. Set it via environment variable "
                "or pass client_id to SoundCloudClient()."
            )
        return self.client_id

    def _request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            logger.debug("Requesting %s %s params=%s", method, url, params)
            response = self.session.request(method, url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise SoundCloudClientError(f"HTTP error calling SoundCloud API: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise SoundCloudClientError(f"Failed to parse JSON from SoundCloud API: {exc}") from exc

    def _get(self, path_or_url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            url = path_or_url
        else:
            url = f"{self.base_url.rstrip('/')}/{path_or_url.lstrip('/')}"
        return self._request("GET", url, params=params)

    # -----------------------
    # High-level API methods
    # -----------------------
    def resolve_url(self, resource_url: str) -> Dict[str, Any]:
        """
        Resolve any SoundCloud resource URL to a canonical API object.
        """
        client_id = self._ensure_client_id()
        params = {"url": resource_url, "client_id": client_id}
        data = self._get("resolve", params=params)
        logger.debug("Resolved URL %s to kind=%s id=%s", resource_url, data.get("kind"), data.get("id"))
        return data

    def get_track(self, track_id: int) -> Dict[str, Any]:
        client_id = self._ensure_client_id()
        params = {"client_id": client_id}
        return self._get(f"tracks/{track_id}", params=params)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        client_id = self._ensure_client_id()
        params = {"client_id": client_id}
        return self._get(f"users/{user_id}", params=params)

    def get_playlist(self, playlist_id: int) -> Dict[str, Any]:
        client_id = self._ensure_client_id()
        params = {"client_id": client_id}
        return self._get(f"playlists/{playlist_id}", params=params)

    def get_comments_page(
        self,
        track_id: int,
        limit: int = 200,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        Retrieve a single page of comments for a track.
        """
        client_id = self._ensure_client_id()
        params = {
            "client_id": client_id,
            "limit": limit,
            "offset": offset,
        }
        return self._get(f"tracks/{track_id}/comments", params=params)

    def get_all_comments_for_track(
        self,
        track_id: int,
        paginator: "Paginator",
        page_size: int = 200,
    ) -> List[Dict[str, Any]]:
        """
        Fetch comments for a track, honoring paginator.page and paginator.max_items.
        """
        from utils.pagination import Paginator  # Local import to avoid circular at import time

        if not isinstance(paginator, Paginator):
            raise SoundCloudClientError("Paginator instance is required to fetch comments.")

        comments: List[Dict[str, Any]] = []
        offset = 0

        while paginator.can_fetch_next_page():
            paginator.start_new_page()
            logger.debug(
                "Fetching comments page %d for track_id=%s offset=%s",
                paginator.current_page,
                track_id,
                offset,
            )
            chunk = self.get_comments_page(track_id=track_id, limit=page_size, offset=offset)

            items = chunk.get("collection") or chunk.get("comments") or []
            if not items:
                break

            paginator.register_items(len(items))
            comments.extend(items)
            offset += len(items)

            next_href = chunk.get("next_href") or chunk.get("next")
            if not next_href:
                break

            if paginator.reached_max_items():
                break

        logger.info(
            "Fetched %d comments for track_id=%s (pages=%d)",
            len(comments),
            track_id,
            paginator.current_page,
        )
        return comments

    def search_tracks(
        self,
        query: str,
        paginator: "Paginator",
        limit_per_page: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search SoundCloud tracks by a text query, returning raw track JSON objects.
        """
        from utils.pagination import Paginator  # Local import to avoid circular at import time

        if not isinstance(paginator, Paginator):
            raise SoundCloudClientError("Paginator instance is required to search tracks.")

        client_id = self._ensure_client_id()
        results: List[Dict[str, Any]] = []
        offset = 0

        while paginator.can_fetch_next_page():
            paginator.start_new_page()
            params = {
                "q": query,
                "client_id": client_id,
                "limit": limit_per_page,
                "offset": offset,
            }
            logger.debug(
                "Searching tracks page=%d q=%s limit=%d offset=%d",
                paginator.current_page,
                query,
                limit_per_page,
                offset,
            )
            data = self._get("search/tracks", params=params)

            collection = data.get("collection") or []
            if not collection:
                break

            paginator.register_items(len(collection))
            results.extend(collection)
            offset += len(collection)

            next_href = data.get("next_href") or data.get("next")
            if not next_href:
                break

            if paginator.reached_max_items():
                break

        logger.info(
            "Search for %r returned %d tracks (pages=%d)",
            query,
            len(results),
            paginator.current_page,
        )
        return results