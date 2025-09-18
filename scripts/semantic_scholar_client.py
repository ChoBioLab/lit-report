# semantic_scholar_client.py
import datetime
import time
from typing import Any, Dict, List, Optional

import requests


class SemanticScholarAPIClient:
    """Core client for interacting with the Semantic Scholar Academic Graph API."""

    BASE_URL = "https://api.semanticscholar.org/graph/v1/"
    REQUEST_DELAY = 1.1

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required for authenticated requests.")
        self.api_key = api_key
        self.headers = {"x-api-key": self.api_key}
        self.default_fields = "title,year,abstract,citationCount,publicationDate,venue,externalIds,authors,tldr"
        self.last_request_time = 0

    def _ensure_delay(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_request_time
        if elapsed_time < self.REQUEST_DELAY:
            time_to_wait = self.REQUEST_DELAY - elapsed_time
            print(f"Waiting for {time_to_wait:.2f} seconds to respect rate limit...")
            time.sleep(time_to_wait)
        self.last_request_time = time.time()

    def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
        retries: int = 3,
        delay: int = 5,
    ) -> Dict[str, Any]:
        self._ensure_delay()
        url = f"{self.BASE_URL}{endpoint}"
        current_retries = 0
        current_delay = delay

        while current_retries < retries:
            try:
                response = requests.get(
                    url, params=params, headers=self.headers, timeout=30
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code == 401 or response.status_code == 403:
                    raise ValueError(
                        "Invalid API key or insufficient permissions."
                    ) from e
                elif response.status_code == 429:
                    print(f"Rate limit hit. Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_retries += 1
                    current_delay *= 2
                elif response.status_code == 400:
                    print(
                        "Bad Request (400) - likely pagination limit reached. Stopping pagination."
                    )
                    return {"data": []}
                else:
                    print(
                        f"Request failed with status code {response.status_code}. Retrying..."
                    )
                    time.sleep(current_delay)
                    current_retries += 1
                    current_delay *= 2
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ) as e:
                print(
                    f"Network error occurred: {e}. Retrying in {current_delay} seconds..."
                )
                time.sleep(current_delay)
                current_retries += 1
                current_delay *= 2
            except requests.exceptions.RequestException as e:
                print(
                    f"An unexpected request error occurred: {e}. Retrying in {current_delay} seconds..."
                )
                time.sleep(current_delay)
                current_retries += 1
                current_delay *= 2

        print(f"Request failed after {retries} retries. Returning empty result.")
        return {"data": []}

    def _format_date_range(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> str:
        return f"{start_date.strftime('%Y-%m-%d')}:{end_date.strftime('%Y-%m-%d')}"

    def search_papers(
        self,
        query: str,
        fields: str = None,
        date_range: str = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        endpoint = "paper/search"
        params = {
            "query": query,
            "limit": limit,
            "offset": offset,
            "fields": fields if fields else self.default_fields,
        }
        if date_range:
            params["publicationDateOrYear"] = date_range

        response_data = self._make_request(endpoint, params=params)
        return response_data.get("data", [])

    def get_papers_by_date_range(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        query: str = "research",
        fields: str = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        date_range_str = self._format_date_range(start_date, end_date)
        return self.search_papers(
            query=query,
            fields=fields,
            date_range=date_range_str,
            limit=limit,
            offset=offset,
        )

    def get_all_papers_by_date_range(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        query: str = "research",
        fields: str = None,
        max_results: int = 500,
    ) -> List[Dict[str, Any]]:
        """Retrieves papers published within a specific date range, handling pagination gracefully."""
        all_papers = []
        limit = 100
        offset = 0
        consecutive_failures = 0
        max_consecutive_failures = 2

        print(
            f"Fetching papers from {start_date} to {end_date} with query '{query}'..."
        )

        while len(all_papers) < max_results:
            try:
                papers_page = self.get_papers_by_date_range(
                    start_date,
                    end_date,
                    query=query,
                    fields=fields,
                    limit=limit,
                    offset=offset,
                )

                if not papers_page:
                    print(
                        f"No more papers found. Stopping pagination at {len(all_papers)} papers."
                    )
                    break

                all_papers.extend(papers_page)
                offset += limit
                consecutive_failures = 0
                print(f"Fetched {len(all_papers)} papers so far...")

                if len(papers_page) < limit:
                    print(
                        f"Received fewer papers than requested ({len(papers_page)} < {limit}). End of results."
                    )
                    break

            except requests.exceptions.RequestException as e:
                consecutive_failures += 1
                print(f"Error during pagination (attempt {consecutive_failures}): {e}")

                if consecutive_failures >= max_consecutive_failures:
                    print(
                        f"Too many consecutive failures ({consecutive_failures}). Stopping pagination."
                    )
                    break

                time.sleep(5)

        print(f"Final result: {len(all_papers)} papers fetched.")
        return all_papers

    def get_paper_details(
        self, paper_id: str, fields: str = None
    ) -> Optional[Dict[str, Any]]:
        endpoint = f"paper/{paper_id}"
        params = {"fields": fields if fields else self.default_fields}
        try:
            return self._make_request(endpoint, params=params)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching details for paper {paper_id}: {e}")
            return None
