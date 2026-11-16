#!/usr/bin/env python3
"""Prepare a release of stresing_python.

Sets the version in pyproject.toml, turns "Unreleased" in CHANGELOG.md into the new
version section, creates the commit "chore: release version x.y.z" and the tag x.y.z.
Nothing is pushed: check the result, then push commit and tag together, which starts
the release workflow on GitHub.

Usage:
    python scripts/prepare_release.py 4.25.0
    python scripts/prepare_release.py 4.25.0 --dry-run      # only show what would change
    python scripts/prepare_release.py 9.9.10 --any-branch   # test on a branch other than master
"""

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(\.post\d+)?$")
UNRELEASED_PATTERN = re.compile(r"^##\s+\[?unreleased\]?\s*$", re.IGNORECASE)
REPO = Path(__file__).resolve().parent.parent


def git(*args, check=True):
    """Run a git command in the repository and return its output."""
    result = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def read_lines(path):
    """Read a text file, return its lines and the line ending it uses (\\r\\n or \\n)."""
    text = path.read_text(encoding="utf-8", newline="")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text.splitlines(), newline


def write_lines(path, lines, newline):
    path.write_text(newline.join(lines) + newline, encoding="utf-8", newline="")


def heading_level(line):
    """Number of leading '#' of a Markdown heading, 0 for other lines."""
    match = re.match(r"^(#+)\s", line)
    return len(match.group(1)) if match else 0


def drop_empty_headings(lines):
    """Remove blank lines and headings without entries below them (before the next heading of the same or higher level)."""
    lines = [line for line in lines if line.strip()]
    kept = []
    for i, line in enumerate(lines):
        level = heading_level(line)
        if level == 0:
            kept.append(line)
            continue
        for following in lines[i + 1:]:
            following_level = heading_level(following)
            if following_level == 0:
                kept.append(line)
                break
            if following_level <= level:
                break
    return kept


def update_changelog(lines, version, date):
    """Turn "Unreleased" into "## <version> - <date>" and add a new empty "Unreleased" above it."""
    if any(re.match(rf"^##\s+\[?{re.escape(version)}\]?(\s|$)", line) for line in lines):
        sys.exit(f"CHANGELOG.md already contains a section for {version}")

    start = next((i for i, line in enumerate(lines) if UNRELEASED_PATTERN.match(line)), None)
    if start is None:
        sys.exit('CHANGELOG.md has no "## Unreleased" section')
    end = next((i for i in range(start + 1, len(lines)) if heading_level(lines[i]) == 2), len(lines))

    unreleased = lines[start + 1:end]
    entries = drop_empty_headings(unreleased)
    if not any(heading_level(line) == 0 for line in entries):
        sys.exit('"Unreleased" in CHANGELOG.md has no entries, nothing to release')

    # the new "Unreleased" gets the same (empty) headings as before
    template = [line for line in unreleased if heading_level(line) > 0]
    new_section = [lines[start], *template, "", "", f"## {version} - {date}", *entries, ""]
    return lines[:start] + new_section + lines[end:]


def update_pyproject(lines, version):
    pattern = re.compile(r'^version\s*=\s*"[^"]*"')
    matches = [i for i, line in enumerate(lines) if pattern.match(line)]
    if len(matches) != 1:
        sys.exit(f"Expected exactly one 'version = \"...\"' line in pyproject.toml, found {len(matches)}")
    lines = list(lines)
    lines[matches[0]] = f'version = "{version}"'
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("version", help="new version, e.g. 4.25.0 or 4.25.0.post1")
    parser.add_argument("--dry-run", action="store_true", help="only show the changes, do not write, commit or tag")
    parser.add_argument("--any-branch", action="store_true", help="allow a branch other than master (for tests)")
    args = parser.parse_args()
    version = args.version

    # 1. Checks
    if not VERSION_PATTERN.match(version):
        sys.exit(f"Invalid version '{version}', expected x.y.z or x.y.z.postN")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != "master" and not args.any_branch:
        sys.exit(f"You are on '{branch}', releases are made from master (use --any-branch for tests)")
    if git("status", "--porcelain"):
        sys.exit("Working tree is not clean, commit or stash your changes first")
    git("fetch", "origin", "--tags")
    if git("rev-parse", "-q", "--verify", f"refs/tags/{version}", check=False):
        sys.exit(f"Tag {version} already exists")
    behind = git("rev-list", "--count", f"HEAD..origin/{branch}", check=False)
    if behind not in ("", "0"):
        sys.exit(f"'{branch}' is {behind} commit(s) behind origin/{branch}, pull first")

    # 2. Changes
    changelog_path = REPO / "CHANGELOG.md"
    pyproject_path = REPO / "pyproject.toml"
    changelog, changelog_newline = read_lines(changelog_path)
    pyproject, pyproject_newline = read_lines(pyproject_path)
    new_changelog = update_changelog(changelog, version, datetime.date.today().isoformat())
    new_pyproject = update_pyproject(pyproject, version)

    if args.dry_run:
        start = next(i for i, line in enumerate(new_changelog) if line.startswith(f"## {version} "))
        end = next((i for i in range(start + 1, len(new_changelog)) if heading_level(new_changelog[i]) == 2), len(new_changelog))
        print(f"pyproject.toml: version = \"{version}\"")
        print("CHANGELOG.md:")
        print("\n".join(new_changelog[start:end]))
        print("\nDry run, nothing changed.")
        return

    write_lines(changelog_path, new_changelog, changelog_newline)
    write_lines(pyproject_path, new_pyproject, pyproject_newline)

    # 3. Commit and tag (local only)
    git("add", "CHANGELOG.md", "pyproject.toml")
    git("commit", "-m", f"chore: release version {version}")
    git("tag", version)

    print(git("show", "--stat", "HEAD"))
    print(f"\nCreated commit and tag {version}. Check them, then push both together:")
    print(f"    git push origin {branch} {version}")
    print("To undo before pushing:")
    print(f"    git tag -d {version}")
    print("    git reset --hard HEAD~1")


if __name__ == "__main__":
    main()