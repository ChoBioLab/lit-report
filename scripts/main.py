# main.py
import argparse
import datetime
import os
from typing import List

from paper_utils import format_paper_details
from recent_papers_search import get_recent_papers_by_keywords
from semantic_scholar_client import SemanticScholarAPIClient
from top_cited_papers import get_top_cited_papers_by_date_range


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Search and analyze academic papers using Semantic Scholar API"
    )

    # Search parameters
    parser.add_argument(
        "--query",
        default="IBD",
        help="Primary search query - supports natural language phrases (default: IBD)",
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=["IBD genetics", "Crohn's disease", "ulcerative colitis"],
        help="Keywords for recent papers search (default: ['IBD genetics', 'Crohn's disease', 'ulcerative colitis'])",
    )
    parser.add_argument(
        "--exclude-terms",
        nargs="+",
        default=["microbiome", "prebiotics", "probiotics"],
        help="Terms to exclude from results (default: ['microbiome', 'prebiotics', 'probiotics'])",
    )

    # Time ranges
    parser.add_argument(
        "--days-back",
        type=int,
        default=7,
        help="Days back for recent papers search (default: 7)",
    )
    parser.add_argument(
        "--months-back",
        type=int,
        default=12,
        help="Months back for top cited papers search (default: 12)",
    )

    # Result limits
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Number of top cited papers to retrieve (default: 5)",
    )
    parser.add_argument(
        "--max-results-per-keyword",
        type=int,
        default=150,
        help="Maximum results per keyword for recent search (default: 150)",
    )
    parser.add_argument(
        "--max-fetch-top-cited",
        type=int,
        default=1000,
        help="Maximum papers to fetch when finding top cited (default: 1000)",
    )
    parser.add_argument(
        "--display-limit",
        type=int,
        default=3,
        help="Number of papers to display per keyword (default: 3)",
    )

    # API fields
    parser.add_argument(
        "--fields",
        default="title,authors,citationCount,publicationDate,venue,externalIds,abstract,tldr",
        help="Comma-separated API fields to retrieve",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if not SEMANTIC_SCHOLAR_API_KEY:
        print("ERROR: Please set the SEMANTIC_SCHOLAR_API_KEY environment variable.")
        print("On Windows: set SEMANTIC_SCHOLAR_API_KEY=your_api_key_here")
        print("On Mac/Linux: export SEMANTIC_SCHOLAR_API_KEY=your_api_key_here")
        exit(1)

    client = SemanticScholarAPIClient(api_key=SEMANTIC_SCHOLAR_API_KEY)

    # Top cited papers
    exclude_str = "/".join(args.exclude_terms) if args.exclude_terms else "None"
    print(
        f"--- Top {args.top_n} Most Cited {args.query} Papers (Last {args.months_back} Months, Excluding {exclude_str}) ---"
    )

    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=args.months_back * 30)

    top_papers = get_top_cited_papers_by_date_range(
        client=client,
        start_date=start_date,
        end_date=today,
        query=args.query,
        top_n=args.top_n,
        fields=args.fields,
        max_fetch=args.max_fetch_top_cited,
        exclude_terms=args.exclude_terms,
    )

    for i, paper in enumerate(top_papers, 1):
        print(f"\n{i}. {format_paper_details(paper)}")
        print("-" * 80)

    # Recent papers search
    print("\n" + "=" * 80)
    recent_papers = get_recent_papers_by_keywords(
        client=client,
        keywords=args.keywords,
        days_back=args.days_back,
        fields=args.fields,
        max_results_per_keyword=args.max_results_per_keyword,
        exclude_terms=args.exclude_terms,
    )

    for keyword, papers in recent_papers.items():
        print(f"\nFound {len(papers)} recent papers for '{keyword}' (after exclusions)")
        for i, paper in enumerate(papers[: args.display_limit]):
            print(f"\n{i + 1}. {format_paper_details(paper)}")
            print("-" * 60)


if __name__ == "__main__":
    main()
