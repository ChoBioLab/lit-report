# recent_papers_search.py
import datetime
from typing import Any, Dict, List

from paper_utils import filter_excluded_terms

from semantic_scholar_client import SemanticScholarAPIClient


def get_recent_papers_by_keywords(
    client: SemanticScholarAPIClient,
    keywords: List[str],
    days_back: int = 7,
    fields: str = None,
    max_results_per_keyword: int = 200,
    exclude_terms: List[str] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """Get recent papers for multiple keyword searches."""
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days_back)

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

            results[keyword] = papers
            print(f"Found {len(papers)} papers for '{keyword}'")
        except Exception as e:
            print(f"Error searching for '{keyword}': {e}")
            results[keyword] = []

    return results


if __name__ == "__main__":
    import os

    from paper_utils import format_paper_details

    SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if not SEMANTIC_SCHOLAR_API_KEY:
        print("ERROR: Please set the SEMANTIC_SCHOLAR_API_KEY environment variable.")
        exit(1)

    client = SemanticScholarAPIClient(api_key=SEMANTIC_SCHOLAR_API_KEY)
    EXCLUDE_TERMS = ["microbiome", "prebiotics", "probiotics"]

    keywords = ["IBD genetics", "Crohn's disease", "ulcerative colitis"]
    recent_papers = get_recent_papers_by_keywords(
        client=client,
        keywords=keywords,
        days_back=7,
        max_results_per_keyword=150,
        exclude_terms=EXCLUDE_TERMS,
    )

    for keyword, papers in recent_papers.items():
        print(f"\nFound {len(papers)} recent papers for '{keyword}' (after exclusions)")
        for i, paper in enumerate(papers[:3]):
            print(f"\n{i + 1}. {format_paper_details(paper)}")
            print("-" * 60)
