#!/usr/bin/env python3
"""Search GitHub repositories and return architecture-research metadata as JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


API = "https://api.github.com/search/repositories"


def request_json(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "architecture-open-source-research",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def normalize(item: dict) -> dict:
    license_info = item.get("license") or {}
    return {
        "repository": item["full_name"],
        "url": item["html_url"],
        "description": item.get("description"),
        "stars": item.get("stargazers_count", 0),
        "forks": item.get("forks_count", 0),
        "language": item.get("language"),
        "license": license_info.get("spdx_id") or license_info.get("name"),
        "archived": item.get("archived", False),
        "default_branch": item.get("default_branch"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "pushed_at": item.get("pushed_at"),
        "topics": item.get("topics", []),
        "open_issues": item.get("open_issues_count", 0),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="GitHub repository-search query")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results, 1-100")
    parser.add_argument("--sort", choices=["stars", "forks", "help-wanted-issues", "updated"], default="stars")
    parser.add_argument("--order", choices=["asc", "desc"], default="desc")
    args = parser.parse_args()
    limit = min(max(args.limit, 1), 100)
    query = urllib.parse.urlencode({"q": args.query, "sort": args.sort, "order": args.order, "per_page": limit})
    try:
        payload = request_json(f"{API}?{query}")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": f"GitHub API returned {error.code}", "details": body}, ensure_ascii=False), file=sys.stderr)
        return 1
    except urllib.error.URLError as error:
        print(json.dumps({"error": "GitHub API request failed", "details": str(error.reason)}, ensure_ascii=False), file=sys.stderr)
        return 1

    output = {
        "query": args.query,
        "total_count": payload.get("total_count", 0),
        "results": [normalize(item) for item in payload.get("items", [])],
        "verification_required": [
            "Inspect the repository README, source, tests, releases, and issue activity before recommending it.",
            "Check the actual LICENSE file and dependency licenses before reuse.",
            "Do not infer production suitability from stars or this metadata alone.",
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
