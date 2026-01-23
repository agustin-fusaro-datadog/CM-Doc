#!/usr/bin/env python3
"""
Flask web application for GitHub PR Statistics Tool.
"""

from flask import Flask, render_template, request, jsonify
import sys

from lib.analyzer import PRAnalyzer
from lib.github_client import GitHubAPIError

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze GitHub PR statistics."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        token = data.get('token', '').strip()
        if not token:
            return jsonify({'error': 'GitHub token is required'}), 400

        users = data.get('users', [])
        if not users or not isinstance(users, list):
            return jsonify({'error': 'Users list is required'}), 400

        # Filter out empty usernames
        users = [u.strip() for u in users if u.strip()]
        if not users:
            return jsonify({'error': 'At least one valid username is required'}), 400

        # Optional parameters
        repository = data.get('repository', '').strip() or None
        start_date = data.get('start_date', '').strip() or None
        end_date = data.get('end_date', '').strip() or None

        # Perform analysis
        analyzer = PRAnalyzer(token)
        result = analyzer.analyze(
            users=users,
            repository=repository,
            start_date=start_date,
            end_date=end_date,
            verbose=False
        )

        return jsonify(result), 200

    except GitHubAPIError as e:
        return jsonify({
            'error': 'GitHub API error',
            'details': str(e)
        }), 400

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    print("Starting GitHub PR Statistics Web UI...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
