# Web UI Design for GitHub PR Statistics Tool

## Overview
Web interface for analyzing GitHub PR statistics with real-time data fetching and visualization.

## User Flow

1. **Landing Page**
   - Welcome message and brief description
   - Form to configure analysis
   - Link to GitHub token generation

2. **Configuration Form**
   - GitHub Token (password field with show/hide toggle)
   - Repository (optional text input with placeholder)
   - Users (textarea for multiple usernames, one per line)
   - Date Range (two date pickers: start and end)
   - Submit button

3. **Loading State**
   - Progress indicator while fetching data
   - Status messages (e.g., "Fetching PRs for user1...")
   - Cancel button

4. **Results Display**
   - Summary statistics table
   - Visual charts (bar chart comparing users)
   - Detailed PR list (expandable)
   - Export options (JSON, CSV)
   - "New Analysis" button

5. **Error Handling**
   - Clear error messages
   - Suggestions for fixes
   - Return to form with previous values

## Layout Structure

```
┌─────────────────────────────────────────────────┐
│ Header: "GitHub PR Statistics Tool"             │
├─────────────────────────────────────────────────┤
│                                                  │
│  Configuration Form                              │
│  ┌────────────────────────────────────────────┐ │
│  │ GitHub Token: [******************] 👁       │ │
│  │ Repository: [owner/repo] (optional)         │ │
│  │ Users:                                      │ │
│  │ ┌────────────────────────────────────────┐ │ │
│  │ │ user1                                   │ │ │
│  │ │ user2                                   │ │ │
│  │ └────────────────────────────────────────┘ │ │
│  │ Start Date: [📅 2025-01-01]                │ │
│  │ End Date:   [📅 2026-01-23]                │ │
│  │                                             │ │
│  │           [Analyze PRs]                     │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
├─────────────────────────────────────────────────┤
│ Results (shown after analysis)                   │
│                                                  │
│  Summary Statistics                              │
│  ┌────────────────────────────────────────────┐ │
│  │ User    Total PRs  Avg Lines  Total Lines  │ │
│  │ user1   15         245.3      3,680        │ │
│  │ user2   8          189.5      1,516        │ │
│  │ TOTAL   23         226.0      5,196        │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  Visual Comparison                               │
│  ┌────────────────────────────────────────────┐ │
│  │ [Bar Chart: PRs by User]                   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  [Show Detailed PR List] [Export JSON] [CSV]    │
│                                                  │
│           [New Analysis]                         │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Technical Specifications

### Frontend
- Single-page application (SPA)
- Responsive design (mobile-friendly)
- Modern, clean UI with good UX
- No heavy frameworks (vanilla JS or minimal library)

### Backend
- Flask lightweight web framework
- RESTful API endpoint: POST /api/analyze
- JSON request/response
- Error handling with HTTP status codes

### API Contract

**POST /api/analyze**

Request:
```json
{
  "token": "ghp_...",
  "repository": "owner/repo",  // optional
  "users": ["user1", "user2"],
  "start_date": "2025-01-01",  // optional
  "end_date": "2026-01-23"     // optional
}
```

Response (success):
```json
{
  "summary": [
    {
      "user": "user1",
      "total_prs": 15,
      "avg_lines_per_pr": 245.3,
      "total_lines": 3680
    }
  ],
  "prs": [
    {
      "number": 123,
      "title": "Fix bug",
      "author": "user1",
      "merged_at": "2025-01-15T10:30:00Z",
      "additions": 120,
      "deletions": 50,
      "total_lines": 170,
      "url": "https://github.com/..."
    }
  ]
}
```

Response (error):
```json
{
  "error": "Invalid GitHub token",
  "details": "Check your configuration"
}
```

## Design Principles

1. **Simplicity**: Clean, uncluttered interface
2. **Feedback**: Clear loading states and error messages
3. **Accessibility**: Proper labels, semantic HTML, keyboard navigation
4. **Performance**: Async operations, progressive loading
5. **Security**: Token never logged, HTTPS recommended for production

## Color Scheme
- Primary: #0366d6 (GitHub blue)
- Success: #28a745 (green)
- Error: #d73a49 (red)
- Background: #f6f8fa (light gray)
- Text: #24292e (dark gray)

## Next Steps
1. Set up Flask project structure
2. Refactor existing Python code for web use
3. Build API endpoint
4. Create HTML/CSS frontend
5. Add JavaScript interactivity
6. Integrate Chart.js for visualizations
