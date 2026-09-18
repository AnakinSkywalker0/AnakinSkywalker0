"""Rewrite the "Recently" block in README.md from the GitHub public event feed.

Keeps the section quiet on purpose: one line per event, newest first, no badges.
Run by .github/workflows/activity.yml; safe to run locally (unauthenticated
requests work, they are just rate limited).
"""

import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

USER = os.environ.get("PROFILE_USER", "AnakinSkywalker0")
README = pathlib.Path(__file__).resolve().parents[2] / "README.md"
START, END = "<!-- ACTIVITY:START -->", "<!-- ACTIVITY:END -->"
LIMIT = 5


def fetch_events():
    req = urllib.request.Request(
        "https://api.github.com/users/%s/events/public?per_page=100" % USER,
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def describe(event):
    """Return a one-line description, or None for event types we don't show."""
    kind = event["type"]
    payload = event.get("payload", {})

    if kind == "PushEvent":
        # The public feed omits commit counts, so report the branch instead.
        branch = (payload.get("ref") or "").rsplit("/", 1)[-1]
        return "pushed to `%s`" % branch if branch else "pushed"
    if kind == "CreateEvent":
        ref_type = payload.get("ref_type")
        if ref_type == "repository":
            return "started it"
        if ref_type == "tag":
            return "tagged `%s`" % payload.get("ref")
        if ref_type == "branch":
            return "opened branch `%s`" % payload.get("ref")
        return None
    if kind == "PublicEvent":
        return "made it public"
    if kind == "ReleaseEvent" and payload.get("action") == "published":
        return "released %s" % payload.get("release", {}).get("tag_name", "a version")
    if kind == "PullRequestEvent":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        if action == "closed" and pr.get("merged"):
            action = "merged"
        elif action not in ("opened", "reopened"):
            return None
        return "%s PR #%s — %s" % (action, pr.get("number"), pr.get("title", "").strip())
    if kind == "IssuesEvent" and payload.get("action") in ("opened", "closed"):
        issue = payload.get("issue", {})
        return "%s issue #%s — %s" % (
            payload["action"], issue.get("number"), issue.get("title", "").strip())
    if kind == "WatchEvent":
        return "starred it"
    if kind == "ForkEvent":
        return "forked it"
    return None


def render(events):
    lines, seen = [], set()
    for event in events:
        text = describe(event)
        if not text:
            continue
        repo = event["repo"]["name"]
        # One line per repo+action so a burst of pushes doesn't fill the section.
        key = (repo, text.split(" ")[0])
        if key in seen:
            continue
        seen.add(key)
        day = event["created_at"][:10]
        lines.append("`%s` · [%s](https://github.com/%s) — %s" % (day, repo, repo, text))
        if len(lines) == LIMIT:
            break
    if not lines:
        return "_Nothing public lately — most of the work lives in private repos._"
    # Explicit breaks — plain newlines collapse into one paragraph on GitHub.
    return "<br>\n".join(lines) + "\n"


def main():
    try:
        events = fetch_events()
    except (urllib.error.URLError, TimeoutError) as exc:
        print("could not reach the GitHub API: %s" % exc, file=sys.stderr)
        return 1

    body = render(events)
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        print("markers %s / %s not found in README.md" % (START, END), file=sys.stderr)
        return 1

    updated = pattern.sub("%s\n%s\n%s" % (START, body.rstrip("\n"), END), text)
    if updated == text:
        print("no change")
        return 0
    README.write_text(updated, encoding="utf-8")
    print("updated:\n" + body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
