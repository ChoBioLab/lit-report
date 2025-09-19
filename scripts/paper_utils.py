from typing import Any, Dict, List


def filter_excluded_terms(
    papers: List[Dict[str, Any]], exclude_terms: List[str]
) -> List[Dict[str, Any]]:
    """Filter out papers that contain any of the excluded terms in title or abstract."""
    if not exclude_terms:
        return papers

    filtered_papers = []
    excluded_count = 0
    exclude_terms_lower = [term.lower() for term in exclude_terms]

    for paper in papers:
        title = paper.get("title", "") or ""
        abstract = paper.get("abstract", "") or ""
        title = title.lower()
        abstract = abstract.lower()

        excluded = any(
            term in title or term in abstract for term in exclude_terms_lower
        )

        if not excluded:
            filtered_papers.append(paper)
        else:
            excluded_count += 1

    if excluded_count > 0:
        print(
            f"Excluded {excluded_count} papers containing excluded terms. {len(filtered_papers)} papers remaining."
        )

    return filtered_papers


def format_paper_details(paper: Dict[str, Any]) -> str:
    """Format paper details for display including authors, journal, DOI, and TLDR."""
    title = paper.get("title", "N/A")

    # Format authors with "first 3 ... last 3" pattern for long lists
    authors = paper.get("authors", [])
    if authors:
        author_names = [author.get("name", "Unknown") for author in authors]
        if len(author_names) <= 6:
            authors_str = ", ".join(author_names)
        else:
            first_three = ", ".join(author_names[:3])
            last_three = ", ".join(author_names[-3:])
            authors_str = f"{first_three} ... {last_three}"
    else:
        authors_str = "N/A"

    journal = paper.get("venue", "N/A")
    external_ids = paper.get("externalIds", {}) or {}
    doi = external_ids.get("DOI", "N/A")

    # Construct publication URL
    paper_url = "N/A"
    if doi != "N/A":
        paper_url = f"https://doi.org/{doi}"
    else:
        paper_id = paper.get("paperId")
        if paper_id:
            paper_url = f"https://www.semanticscholar.org/paper/{paper_id}"

    pub_date = paper.get("publicationDate", "N/A")
    citations = paper.get("citationCount", "N/A")

    tldr_obj = paper.get("tldr", {})
    if tldr_obj and isinstance(tldr_obj, dict):
        tldr = tldr_obj.get("text", "N/A")
    else:
        tldr = "N/A"

    return f"""
    Title: {title}
    Authors: {authors_str}
    Journal: {journal}
    Published: {pub_date}
    Citations: {citations}
    URL: {paper_url}
    TLDR: {tldr}
    """.strip()
