# recent_papers_search.py
import datetime
from typing import Any, Dict, List

from journal_impact import JournalImpactAnalyzer, sort_papers_by_impact
from paper_utils import filter_excluded_terms
from semantic_scholar_client import SemanticScholarAPIClient


def get_recent_papers_by_keywords(
    client: SemanticScholarAPIClient,
    keywords: List[str],
    days_back: int = 7,
    fields: str = None,
    max_results_per_keyword: int = 200,
    exclude_terms: List[str] = None,
    sort_by_impact: bool = True,
) -> Dict[str, List[Dict[str, Any]]]:
    """Get recent papers with optional impact factor sorting."""
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days_back)

    analyzer = JournalImpactAnalyzer() if sort_by_impact else None
    results = {}

    for keyword in keywords:
        print(f"\n--- Searching for '{keyword}' in last {days_back} days ---")
        try:
            papers = client.get_all_papers_by_date_range(
                start_date=start_date,
                end_date=today,
                query=keyword,
                fields=fields,
                max_results=max_results_per_keyword,
            )

            if exclude_terms:
                papers = filter_excluded_terms(papers, exclude_terms)

            if sort_by_impact and analyzer:
                papers = sort_papers_by_impact(papers, analyzer)
                print(f"Found {len(papers)} papers for '{keyword}' (sorted by impact)")
            else:
                print(f"Found {len(papers)} papers for '{keyword}'")

            results[keyword] = papers

        except Exception as e:
            print(f"Error searching for '{keyword}': {e}")
            results[keyword] = []

    return results
