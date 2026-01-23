"""GitHub API client for fetching PR data."""

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass


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
        end_date: Optional[str] = None,
        verbose: bool = True
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

        if verbose:
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

        if verbose:
            print(f"✓ Found {len(pr_data_list)} merged PRs")

        return pr_data_list
