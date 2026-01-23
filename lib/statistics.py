"""Statistics calculation for PR data."""

from typing import List
from dataclasses import dataclass, asdict
from collections import defaultdict
from .github_client import PRData


@dataclass
class UserStats:
    """Statistics for a single user."""
    user: str
    total_prs: int
    avg_lines_per_pr: float
    total_lines: int


def calculate_statistics(pr_data_list: List[PRData]) -> List[UserStats]:
    """Calculate statistics per user."""
    user_prs = defaultdict(list)

    for pr in pr_data_list:
        user_prs[pr.author].append(pr)

    stats = []
    for user, prs in user_prs.items():
        total_prs = len(prs)
        total_lines = sum(pr.total_lines for pr in prs)
        avg_lines = total_lines / total_prs if total_prs > 0 else 0

        stats.append(UserStats(
            user=user,
            total_prs=total_prs,
            avg_lines_per_pr=round(avg_lines, 1),
            total_lines=total_lines
        ))

    stats.sort(key=lambda x: x.total_prs, reverse=True)
    return stats
