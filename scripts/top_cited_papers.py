# top_cited_papers.py
import datetime
from typing import Any, Dict, List

from paper_utils import filter_excluded_terms

from semantic_scholar_client import SemanticScholarAPIClient


def get_top_cited_papers_by_date_range(
    client: SemanticScholarAPIClient,
    start_date: datetime.date,
    end_date: datetime.date,
    query: str,
    top_n: int = 5,
    fields: str = None,
    max_fetch: int = 1000,
    exclude_terms: List[str] = None,
) -> List[Dict[str, Any]]:
    """Get the top N most cited papers for a query within a date range."""
    print(
        f"Fetching papers for '{query}' from {start_date} to {end_date} to find top {top_n} most cited..."
    )

    all_papers = client.get_all_papers_by_date_range(
        start_date=start_date,
        end_date=end_date,
        query=query,
        fields=fields,
        max_results=max_fetch,
    )

    if exclude_terms:
        all_papers = filter_excluded_terms(all_papers, exclude_terms)

    if not all_papers:
        print(f"No papers found for query '{query}' in the specified date range.")
        return []

    sorted_papers = sorted(
        all_papers, key=lambda x: x.get("citationCount", 0), reverse=True
    )
    top_papers = sorted_papers[:top_n]

    print(
        f"Selected top {len(top_papers)} most cited papers from {len(all_papers)} total papers."
    )
    return top_papers


if __name__ == "__main__":
    import os

    from paper_utils import format_paper_details

    SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if not SEMANTIC_SCHOLAR_API_KEY:
        print("ERROR: Please set the SEMANTIC_SCHOLAR_API_KEY environment variable.")
        exit(1)

    client = SemanticScholarAPIClient(api_key=SEMANTIC_SCHOLAR_API_KEY)
    EXCLUDE_TERMS = ["microbiome", "prebiotics", "probiotics"]

    today = datetime.date.today()
    twelve_months_ago = today - datetime.timedelta(days=365)

    top_ibd_papers = get_top_cited_papers_by_date_range(
        client=client,
        start_date=twelve_months_ago,
        end_date=today,
        query="IBD",
        top_n=5,
        fields="title,authors,citationCount,publicationDate,venue,externalIds,abstract,tldr",
        exclude_terms=EXCLUDE_TERMS,
    )

    print(
        "--- Top 5 Most Cited IBD Papers (Last 12 Months, Excluding Microbiome/Prebiotics/Probiotics) ---"
    )
    for i, paper in enumerate(top_ibd_papers, 1):
        print(f"\n{i}. {format_paper_details(paper)}")
        print("-" * 80)
