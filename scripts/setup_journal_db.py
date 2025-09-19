# setup_journal_db.py
import time

import requests

from journal_impact import JournalImpactAnalyzer


def populate_journal_database(max_journals: int = 1000):
    """Populate database with OpenAlex journal data."""
    analyzer = JournalImpactAnalyzer()

    # OpenAlex API endpoint for medical/biology journals
    url = "https://api.openalex.org/sources"
    params = {"filter": "type:journal,works_count:>100", "per-page": 200, "cursor": "*"}

    headers = {"User-Agent": "JournalImpactTool/1.0", "Accept": "application/json"}

    processed = 0

    while processed < max_journals:
        try:
            response = requests.get(url, headers=headers, params=params)
            time.sleep(0.1)  # Rate limiting

            if response.status_code != 200:
                print(f"API error: {response.status_code}")
                break

            data = response.json()
            journals = data.get("results", [])

            if not journals:
                break

            for journal in journals:
                if processed >= max_journals:
                    break

                # Extract ISSN data safely
                issn_l = journal.get("issn_l")
                issn_list = journal.get("issn", []) or []  # Handle None case

                journal_data = {
                    "issn_l": issn_l,
                    "display_name": journal.get("display_name"),
                    "issn_print": issn_list[0] if len(issn_list) > 0 else None,
                    "issn_online": issn_list[1] if len(issn_list) > 1 else None,
                    "works_count": journal.get("works_count", 0),
                    "cited_by_count": journal.get("cited_by_count", 0),
                    "h_index": journal.get("summary_stats", {}).get("h_index", 0)
                    if journal.get("summary_stats")
                    else 0,
                }

                if issn_l:  # Only add if we have ISSN
                    analyzer.add_journal(journal_data)
                    processed += 1

                    if processed % 100 == 0:
                        print(f"Processed {processed} journals...")

            # Get next page
            meta = data.get("meta", {})
            next_cursor = meta.get("next_cursor")
            if next_cursor:
                params["cursor"] = next_cursor
            else:
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"Database populated with {processed} journals")


if __name__ == "__main__":
    populate_journal_database()
