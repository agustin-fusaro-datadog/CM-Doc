#!/usr/bin/env python3
"""
GitHub PR Statistics Tool
Analyzes PR activity for specified users within a date range.
"""

import sys
import yaml
import requests
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass


class GitHubAPIError(Exception):
    """Raised when GitHub API request fails."""
    pass


@dataclass
class PRData:
    """Pull request data."""
    number: int
    title: str
    author: str
    merged_at: str
    additions: int
    deletions: int
    total_lines: int
    url: str


class Config:
    """Configuration loader and validator."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.data = self._load()
        self._validate()

    def _load(self) -> Dict:
        """Load YAML configuration file."""
        if not self.config_path.exists():
            raise ConfigError(
                f"Configuration file not found: {self.config_path}\n"
                f"Copy config.example.yaml to config.yaml and configure it."
            )

        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
                if data is None:
                    raise ConfigError("Configuration file is empty")
                return data
        except yaml.YAMLError as e:
            raise ConfigError(f"Invalid YAML syntax: {e}")

    def _validate(self):
        """Validate required fields and format."""
        # Validate GitHub section
        if 'github' not in self.data:
            raise ConfigError("Missing 'github' section in config")

        github = self.data['github']
        if not github.get('token'):
            raise ConfigError(
                "Missing 'github.token' in config\n"
                "Generate a token at: https://github.com/settings/tokens"
            )

        # Validate users
        if 'users' not in self.data or not self.data['users']:
            raise ConfigError("Missing 'users' list in config")

        if not isinstance(self.data['users'], list):
            raise ConfigError("'users' must be a list")

        # Validate date range format
        if 'date_range' in self.data:
            date_range = self.data['date_range']
            for field in ['start', 'end']:
                if date_range.get(field):
                    try:
                        datetime.strptime(date_range[field], '%Y-%m-%d')
                    except ValueError:
                        raise ConfigError(
                            f"Invalid date format for 'date_range.{field}': {date_range[field]}\n"
                            f"Expected format: YYYY-MM-DD"
                        )

        # Validate output format
        if 'output' in self.data:
            output_format = self.data['output'].get('format', 'table')
            valid_formats = ['table', 'json', 'csv']
            if output_format not in valid_formats:
                raise ConfigError(
                    f"Invalid output format: {output_format}\n"
                    f"Valid formats: {', '.join(valid_formats)}"
                )

    @property
    def github_token(self) -> str:
        return self.data['github']['token']

    @property
    def repository(self) -> Optional[str]:
        return self.data['github'].get('repository')

    @property
    def users(self) -> List[str]:
        return self.data['users']

    @property
    def start_date(self) -> Optional[str]:
        return self.data.get('date_range', {}).get('start')

    @property
    def end_date(self) -> Optional[str]:
        return self.data.get('date_range', {}).get('end')

    @property
    def output_format(self) -> str:
        return self.data.get('output', {}).get('format', 'table')

    @property
    def show_details(self) -> bool:
        return self.data.get('output', {}).get('show_details', False)


class GitHubClient:
    """GitHub API client for fetching PR data."""

    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.base_url = 'https://api.github.com'

    def _make_request(self, url: str, params: Dict = None) -> Dict:
        """Make authenticated request to GitHub API."""
        try:
            response = self.session.get(url, params=params)

            if response.status_code == 401:
                raise GitHubAPIError("Invalid GitHub token. Check your configuration.")
            elif response.status_code == 403:
                if 'rate limit' in response.text.lower():
                    raise GitHubAPIError("GitHub API rate limit exceeded. Try again later.")
                raise GitHubAPIError(f"GitHub API forbidden: {response.text}")
            elif response.status_code != 200:
                raise GitHubAPIError(f"GitHub API error ({response.status_code}): {response.text}")

            return response.json()
        except requests.RequestException as e:
            raise GitHubAPIError(f"Network error: {e}")

    def _get_all_pages(self, url: str, params: Dict = None) -> List[Dict]:
        """Fetch all pages of results from GitHub API."""
        results = []
        params = params or {}
        params['per_page'] = 100
        page = 1

        while True:
            params['page'] = page
            response = self._make_request(url, params)

            if not response:
                break

            if isinstance(response, dict) and 'items' in response:
                items = response['items']
                results.extend(items)
                if len(items) < 100:
                    break
            elif isinstance(response, list):
                results.extend(response)
                if len(response) < 100:
                    break
            else:
                break

            page += 1

        return results

    def fetch_merged_prs(
        self,
        user: str,
        repository: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[PRData]:
        """Fetch merged PRs for a user within date range."""
        query_parts = [f"author:{user}", "is:pr", "is:merged"]

        if repository:
            query_parts.append(f"repo:{repository}")

        if start_date:
            query_parts.append(f"merged:>={start_date}")

        if end_date:
            query_parts.append(f"merged:<={end_date}")

        query = " ".join(query_parts)
        search_url = f"{self.base_url}/search/issues"

        print(f"  Fetching PRs for {user}...", end=" ", flush=True)
        prs = self._get_all_pages(search_url, {'q': query, 'sort': 'updated', 'order': 'desc'})

        pr_data_list = []
        for pr in prs:
            pr_number = pr['number']
            repo_full_name = pr['repository_url'].split('repos/')[-1]
            pr_url = f"{self.base_url}/repos/{repo_full_name}/pulls/{pr_number}"

            pr_details = self._make_request(pr_url)

            pr_data = PRData(
                number=pr_number,
                title=pr['title'],
                author=user,
                merged_at=pr_details.get('merged_at', ''),
                additions=pr_details.get('additions', 0),
                deletions=pr_details.get('deletions', 0),
                total_lines=pr_details.get('additions', 0) + pr_details.get('deletions', 0),
                url=pr['html_url']
            )
            pr_data_list.append(pr_data)

        print(f"✓ Found {len(pr_data_list)} merged PRs")
        return pr_data_list


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


def display_table(stats: List[UserStats], pr_data_list: List[PRData], show_details: bool):
    """Display statistics in table format."""
    if not stats:
        print("No data to display")
        return

    print("\n" + "=" * 80)
    print("PR STATISTICS SUMMARY")
    print("=" * 80)

    print(f"\n{'User':<20} {'Total PRs':<12} {'Avg Lines/PR':<15} {'Total Lines':<15}")
    print("-" * 80)

    for stat in stats:
        print(f"{stat.user:<20} {stat.total_prs:<12} {stat.avg_lines_per_pr:<15.1f} {stat.total_lines:<15,}")

    print("-" * 80)
    total_prs = sum(s.total_prs for s in stats)
    total_lines = sum(s.total_lines for s in stats)
    overall_avg = total_lines / total_prs if total_prs > 0 else 0
    print(f"{'TOTAL':<20} {total_prs:<12} {overall_avg:<15.1f} {total_lines:<15,}")
    print("=" * 80)

    if show_details:
        print("\nDETAILED PR LIST")
        print("=" * 80)
        for pr in sorted(pr_data_list, key=lambda x: x.merged_at, reverse=True):
            print(f"\n#{pr.number} - {pr.title}")
            print(f"  Author: {pr.author}")
            print(f"  Merged: {pr.merged_at}")
            print(f"  Lines: +{pr.additions} -{pr.deletions} (total: {pr.total_lines})")
            print(f"  URL: {pr.url}")


def display_json(stats: List[UserStats], pr_data_list: List[PRData]):
    """Display statistics in JSON format."""
    output = {
        'summary': [asdict(s) for s in stats],
        'total_prs': sum(s.total_prs for s in stats),
        'prs': [asdict(pr) for pr in pr_data_list]
    }
    print(json.dumps(output, indent=2))


def display_csv(stats: List[UserStats], pr_data_list: List[PRData]):
    """Display statistics in CSV format."""
    print("user,total_prs,avg_lines_per_pr,total_lines")
    for stat in stats:
        print(f"{stat.user},{stat.total_prs},{stat.avg_lines_per_pr},{stat.total_lines}")


def main():
    """Main entry point."""
    try:
        config = Config()
        print(f"✓ Configuration loaded successfully")
        print(f"  Repository: {config.repository or 'All accessible repos'}")
        print(f"  Users: {', '.join(config.users)}")
        print(f"  Date range: {config.start_date or 'All time'} to {config.end_date or 'Now'}")
        print(f"  Output format: {config.output_format}")
        print()

        client = GitHubClient(config.github_token)

        all_pr_data = []
        for user in config.users:
            pr_data = client.fetch_merged_prs(
                user=user,
                repository=config.repository,
                start_date=config.start_date,
                end_date=config.end_date
            )
            all_pr_data.extend(pr_data)

        print(f"\n✓ Fetched {len(all_pr_data)} total PRs")

        if not all_pr_data:
            print("\nNo PRs found matching the criteria")
            return

        stats = calculate_statistics(all_pr_data)

        if config.output_format == 'json':
            display_json(stats, all_pr_data)
        elif config.output_format == 'csv':
            display_csv(stats, all_pr_data)
        else:
            display_table(stats, all_pr_data, config.show_details)

    except ConfigError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except GitHubAPIError as e:
        print(f"GitHub API Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
