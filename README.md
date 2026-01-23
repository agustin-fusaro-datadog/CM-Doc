# GitHub PR Statistics Tool

Analyzes pull request activity for specified GitHub users within a configurable date range.

## Features

- Fetch merged PRs for multiple users
- Filter by date range and repository
- Calculate statistics:
  - Total merged PRs per user
  - Average lines of code per PR
  - Total lines changed
- Multiple output formats: table, JSON, CSV
- Optional detailed PR listing

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create configuration file:

```bash
cp config.example.yaml config.yaml
```

3. Edit `config.yaml` with your settings:
   - Add your GitHub personal access token
   - List users to analyze
   - Set date range
   - Configure output preferences

## Configuration

### GitHub Token

Generate a personal access token at: https://github.com/settings/tokens

Required scopes: `repo` (for private repositories) or `public_repo` (for public only)

### Example Configuration

```yaml
github:
  token: "ghp_your_token_here"
  repository: "datadog/dd-source"

users:
  - "gondyb"
  - "user2"

date_range:
  start: "2025-01-01"
  end: "2026-01-23"

output:
  format: "table"
  show_details: false
```

### Configuration Options

**github.token** (required): Your GitHub personal access token

**github.repository** (optional): Repository to analyze in format `owner/repo`. Leave empty to search across all accessible repos.

**users** (required): List of GitHub usernames to analyze

**date_range.start** (optional): Start date in YYYY-MM-DD format. Leave empty for all time.

**date_range.end** (optional): End date in YYYY-MM-DD format. Leave empty for present.

**output.format**: Output format - `table` (default), `json`, or `csv`

**output.show_details**: Include detailed PR list (only for table format)

## Usage

Run the tool:

```bash
python3 pr_stats.py
```

### Example Output (Table Format)

```
✓ Configuration loaded successfully
  Repository: datadog/dd-source
  Users: gondyb, user2
  Date range: 2025-01-01 to 2026-01-23
  Output format: table

  Fetching PRs for gondyb... ✓ Found 15 merged PRs
  Fetching PRs for user2... ✓ Found 8 merged PRs

✓ Fetched 23 total PRs

================================================================================
PR STATISTICS SUMMARY
================================================================================

User                 Total PRs    Avg Lines/PR    Total Lines
--------------------------------------------------------------------------------
gondyb               15           245.3           3,680
user2                8            189.5           1,516
--------------------------------------------------------------------------------
TOTAL                23           226.0           5,196
================================================================================
```

### JSON Output

```bash
# Set format to "json" in config.yaml or:
python3 pr_stats.py > output.json
```

### CSV Output

```bash
# Set format to "csv" in config.yaml or:
python3 pr_stats.py > output.csv
```

## Error Handling

The tool handles common errors gracefully:

- **Invalid token**: Clear error message with link to generate token
- **Rate limit exceeded**: Notifies to try again later
- **Network errors**: Reports connection issues
- **Invalid configuration**: Validates format and required fields

## Troubleshooting

**"GitHub API rate limit exceeded"**
- GitHub API has rate limits (5000 requests/hour for authenticated users)
- Wait an hour or reduce the number of users/date range

**"Invalid GitHub token"**
- Verify your token in config.yaml
- Ensure token has correct scopes (`repo` or `public_repo`)
- Generate new token at: https://github.com/settings/tokens

**"No PRs found"**
- Check that users have merged PRs in the specified date range
- Verify repository name format: `owner/repo`
- Ensure users have access to the repository

## License

MIT
