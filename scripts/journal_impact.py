# journal_impact.py
import re
import sqlite3
from typing import Any, Dict, List, Optional


class JournalImpactAnalyzer:
    """Lightweight journal impact analyzer using OpenAlex-derived data."""

    def __init__(self, db_path: str = "journal_impact.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for journal impact data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journals (
                issn_l TEXT PRIMARY KEY,
                display_name TEXT,
                issn_print TEXT,
                issn_online TEXT,
                impact_factor REAL,
                works_count INTEGER,
                cited_by_count INTEGER,
                h_index INTEGER
            )
        """)

        conn.commit()
        conn.close()

    def calculate_impact_factor(
        self, cited_by_count: int, works_count: int, years_active: int = 5
    ) -> float:
        """Calculate approximate impact factor from citation data."""
        if works_count == 0 or years_active == 0:
            return 0.0

        avg_citations_per_paper = cited_by_count / works_count
        impact_factor = avg_citations_per_paper / years_active
        return round(impact_factor, 3)

    def add_journal(self, journal_data: Dict[str, Any]):
        """Add journal to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Calculate impact factor
        cited_by_count = journal_data.get("cited_by_count", 0)
        works_count = journal_data.get("works_count", 0)
        impact_factor = self.calculate_impact_factor(cited_by_count, works_count)

        cursor.execute(
            """
            INSERT OR REPLACE INTO journals 
            (issn_l, display_name, issn_print, issn_online, impact_factor, works_count, cited_by_count, h_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                journal_data.get("issn_l"),
                journal_data.get("display_name"),
                journal_data.get("issn_print"),
                journal_data.get("issn_online"),
                impact_factor,
                works_count,
                cited_by_count,
                journal_data.get("h_index", 0),
            ),
        )

        conn.commit()
        conn.close()

    def get_journal_by_issn(self, issn: str) -> Optional[Dict[str, Any]]:
        """Get journal data by any ISSN variant."""
        if not issn:
            return None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Try all ISSN fields
        cursor.execute(
            """
            SELECT issn_l, display_name, impact_factor, h_index, works_count
            FROM journals 
            WHERE issn_l = ? OR issn_print = ? OR issn_online = ?
        """,
            (issn, issn, issn),
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "issn_l": result[0],
                "display_name": result[1],
                "impact_factor": result[2],
                "h_index": result[3],
                "works_count": result[4],
            }
        return None

    def get_journal_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get journal by name with fuzzy matching."""
        if not name:
            return None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Normalize name for matching
        normalized_name = re.sub(r"[^\w\s]", " ", name.lower())
        normalized_name = re.sub(r"\s+", " ", normalized_name.strip())

        # Try exact match first
        cursor.execute(
            """
            SELECT issn_l, display_name, impact_factor, h_index, works_count
            FROM journals 
            WHERE LOWER(display_name) = ?
        """,
            (name.lower(),),
        )

        result = cursor.fetchone()

        # Try partial match if exact fails
        if not result:
            cursor.execute(
                """
                SELECT issn_l, display_name, impact_factor, h_index, works_count
                FROM journals 
                WHERE LOWER(display_name) LIKE ?
                ORDER BY impact_factor DESC
                LIMIT 1
            """,
                (f"%{normalized_name}%",),
            )
            result = cursor.fetchone()

        conn.close()

        if result:
            return {
                "issn_l": result[0],
                "display_name": result[1],
                "impact_factor": result[2],
                "h_index": result[3],
                "works_count": result[4],
            }
        return None

    def get_paper_impact_score(self, paper: Dict[str, Any]) -> float:
        """Calculate impact score for a paper."""
        # Extract ISSN from paper
        external_ids = paper.get("externalIds", {})
        issn = None
        for key in ["ISSN", "issn"]:
            if key in external_ids:
                issn = external_ids[key]
                break

        # Try ISSN lookup first
        journal_data = None
        if issn:
            journal_data = self.get_journal_by_issn(issn)

        # Fallback to venue name
        if not journal_data:
            venue = paper.get("venue", "")
            if venue:
                journal_data = self.get_journal_by_name(venue)

        # Calculate score
        if journal_data:
            impact_factor = journal_data["impact_factor"]
            base_score = min(100, impact_factor * 10)  # Scale to 0-100
        else:
            base_score = 10  # Unknown journal

        # Add citation bonus for recent papers
        citations = paper.get("citationCount", 0)
        citation_bonus = min(20, citations * 2)

        return base_score + citation_bonus


def sort_papers_by_impact(
    papers: List[Dict[str, Any]], analyzer: JournalImpactAnalyzer
) -> List[Dict[str, Any]]:
    """Sort papers by impact score."""
    return sorted(
        papers, key=lambda p: analyzer.get_paper_impact_score(p), reverse=True
    )
