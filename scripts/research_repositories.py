#!/usr/bin/env python3
"""Search public GitHub and Gitee repositories for architecture research as JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


GITHUB_API = "https://api.github.com/search/repositories"
GITEE_API = "https://gitee.com/api/v5/search/repositories"


def request_json(url: str, source: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "architecture-open-source-research",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if source == "github" and token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def normalize_github(item: dict) -> dict:
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


def normalize_gitee(item: dict) -> dict:
    license_info = item.get("license") or {}
    return {
        "repository": item.get("full_name") or item.get("path_with_namespace") or item.get("name"),
        "url": item.get("html_url") or item.get("url"),
        "description": item.get("description"),
        "stars": item.get("stargazers_count", 0),
        "forks": item.get("forks_count", 0),
        "language": item.get("language"),
        "license": license_info.get("spdx_id") if isinstance(license_info, dict) else license_info,
        "archived": item.get("archived", False),
        "default_branch": item.get("default_branch"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "pushed_at": item.get("pushed_at"),
        "topics": item.get("topics", []),
        "open_issues": item.get("open_issues_count", 0),
    }


def search(source: str, args: argparse.Namespace, limit: int) -> dict:
    if source == "github":
        query = urllib.parse.urlencode({"q": args.query, "sort": args.sort, "order": args.order, "per_page": limit})
        payload = request_json(f"{GITHUB_API}?{query}", source)
        return {"source": source, "total_count": payload.get("total_count", 0), "results": [normalize_github(item) for item in payload.get("items", [])]}
    query = urllib.parse.urlencode({"q": args.query, "sort": "stars", "order": args.order, "per_page": limit})
    payload = request_json(f"{GITEE_API}?{query}", source)
    items = payload if isinstance(payload, list) else payload.get("items", [])
    return {"source": source, "total_count": len(items), "results": [normalize_gitee(item) for item in items]}


def readable_error(source: str, error: Exception) -> dict:
    if isinstance(error, urllib.error.HTTPError):
        detail = f"HTTP {error.code}"
        if error.code in (401, 403, 429):
            next_step = "可能是认证或速率限制。稍后重试；GitHub 可设置 GITHUB_TOKEN 提高公开 API 限额。"
        else:
            next_step = "确认查询词后重试；也可以改用另一个来源或在官方仓库页面人工检索。"
    elif isinstance(error, urllib.error.URLError):
        detail = str(error.reason)
        next_step = "检查网络或代理；使用 --source gitee，或改为阅读官方仓库页面和包注册表。"
    else:
        detail = str(error)
        next_step = "检查参数后重试；不要把本次检索失败解释为没有可用项目。"
    return {"source": source, "error": f"无法查询{source}：{detail}", "next_step": next_step}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="GitHub repository-search query")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results, 1-100")
    parser.add_argument("--sort", choices=["stars", "forks", "help-wanted-issues", "updated"], default="stars")
    parser.add_argument("--order", choices=["asc", "desc"], default="desc")
    parser.add_argument("--source", choices=["auto", "github", "gitee"], default="auto", help="Repository source; auto falls back from GitHub to Gitee")
    args = parser.parse_args()
    limit = min(max(args.limit, 1), 100)
    sources = [args.source] if args.source != "auto" else ["github", "gitee"]
    errors = []
    for source in sources:
        try:
            result = search(source, args, limit)
            output = {
                "query": args.query,
                **result,
                "fallback_used": source != sources[0],
                "failed_sources": errors,
                "verification_required": [
                    "在推荐前检查 README、源码、测试、发布和 issue 活动。",
                    "在复用前检查实际 LICENSE 文件和依赖许可证。",
                    "不要仅根据 star 数或这份元数据判断生产可用性。",
                ],
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return 0
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as error:
            errors.append(readable_error(source, error))

    output = {
        "query": args.query,
        "error": "所有已选公开仓库来源均不可用，本次未得到候选结果。",
        "failed_sources": errors,
        "next_step": "人工检查官方仓库、包注册表或在网络恢复后重试；记录信息缺口，不要据此下技术结论。",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
