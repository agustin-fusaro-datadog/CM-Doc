#!/usr/bin/env python3
"""
GitHub PR Statistics Tool - CLI Interface
Analyzes PR activity for specified users within a date range.
"""

import sys
import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from lib.analyzer import PRAnalyzer
from lib.github_client import GitHubAPIError


class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass


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
        if 'github' not in self.data:
            raise ConfigError("Missing 'github' section in config")

        github = self.data['github']
        if not github.get('token'):
            raise ConfigError(
                "Missing 'github.token' in config\n"
                "Generate a token at: https://github.com/settings/tokens"
            )

        if 'users' not in self.data or not self.data['users']:
            raise ConfigError("Missing 'users' list in config")

        if not isinstance(self.data['users'], list):
            raise ConfigError("'users' must be a list")

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


def display_table(result: Dict, show_details: bool):
    """Display statistics in table format."""
    summary = result['summary']
    prs = result['prs']

    if not summary:
        print("No data to display")
        return

    print("\n" + "=" * 80)
    print("PR STATISTICS SUMMARY")
    print("=" * 80)

    print(f"\n{'User':<20} {'Total PRs':<12} {'Avg Lines/PR':<15} {'Total Lines':<15}")
    print("-" * 80)

    for stat in summary:
        print(f"{stat['user']:<20} {stat['total_prs']:<12} {stat['avg_lines_per_pr']:<15.1f} {stat['total_lines']:<15,}")

    print("-" * 80)
    total_prs = result['total_prs']
    total_lines = sum(s['total_lines'] for s in summary)
    overall_avg = total_lines / total_prs if total_prs > 0 else 0
    print(f"{'TOTAL':<20} {total_prs:<12} {overall_avg:<15.1f} {total_lines:<15,}")
    print("=" * 80)

    if show_details:
        print("\nDETAILED PR LIST")
        print("=" * 80)
        sorted_prs = sorted(prs, key=lambda x: x['merged_at'], reverse=True)
        for pr in sorted_prs:
            print(f"\n#{pr['number']} - {pr['title']}")
            print(f"  Author: {pr['author']}")
            print(f"  Merged: {pr['merged_at']}")
            print(f"  Lines: +{pr['additions']} -{pr['deletions']} (total: {pr['total_lines']})")
            print(f"  URL: {pr['url']}")


def display_json(result: Dict):
    """Display statistics in JSON format."""
    print(json.dumps(result, indent=2))


def display_csv(result: Dict):
    """Display statistics in CSV format."""
    print("user,total_prs,avg_lines_per_pr,total_lines")
    for stat in result['summary']:
        print(f"{stat['user']},{stat['total_prs']},{stat['avg_lines_per_pr']},{stat['total_lines']}")


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

        analyzer = PRAnalyzer(config.github_token)

        result = analyzer.analyze(
            users=config.users,
            repository=config.repository,
            start_date=config.start_date,
            end_date=config.end_date,
            verbose=True
        )

        print(f"\n✓ Fetched {result['total_prs']} total PRs")

        if result['total_prs'] == 0:
            print("\nNo PRs found matching the criteria")
            return

        if config.output_format == 'json':
            display_json(result)
        elif config.output_format == 'csv':
            display_csv(result)
        else:
            display_table(result, config.show_details)

    except ConfigError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except GitHubAPIError as e:
        print(f"GitHub API Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
