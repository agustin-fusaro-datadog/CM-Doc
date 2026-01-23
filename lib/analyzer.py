"""Main analyzer module that orchestrates PR analysis."""

from typing import List, Optional, Dict
from dataclasses import asdict
from .github_client import GitHubClient, PRData, GitHubAPIError
from .statistics import calculate_statistics, UserStats


class PRAnalyzer:
    """Orchestrates PR analysis for multiple users."""

    def __init__(self, token: str):
        self.client = GitHubClient(token)

    def analyze(
        self,
        users: List[str],
        repository: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        verbose: bool = False
    ) -> Dict:
        """
        Analyze PRs for multiple users and return statistics.

        Returns:
            Dict with 'summary' (list of UserStats) and 'prs' (list of PRData)
        """
        all_pr_data = []

        for user in users:
            pr_data = self.client.fetch_merged_prs(
                user=user,
                repository=repository,
                start_date=start_date,
                end_date=end_date,
                verbose=verbose
            )
            all_pr_data.extend(pr_data)

        if not all_pr_data:
            return {
                'summary': [],
                'prs': [],
                'total_prs': 0
            }

        stats = calculate_statistics(all_pr_data)

        return {
            'summary': [asdict(s) for s in stats],
            'prs': [asdict(pr) for pr in all_pr_data],
            'total_prs': len(all_pr_data)
        }
