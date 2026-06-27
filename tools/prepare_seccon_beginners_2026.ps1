$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$eventDir = Join-Path $root "challenges\seccon-beginners-2026"
$categories = @("web", "crypto", "rev", "pwn", "misc", "forensics", "network", "programming")

New-Item -ItemType Directory -Force -Path $eventDir | Out-Null

foreach ($category in $categories) {
    $path = Join-Path $eventDir $category
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    New-Item -ItemType File -Force -Path (Join-Path $path ".gitkeep") | Out-Null
}

$readme = Join-Path $eventDir "README.md"
if (-not (Test-Path $readme)) {
    $content = @(
        "# SECCON Beginners CTF 2026"
        ""
        "- Schedule: 2026/6/13 14:00 JST - 2026/6/14 14:00 JST"
        "- Format: Jeopardy"
        "- Official: https://www.seccon.jp/15/seccon_beginners/ctf.html"
        ""
        "## Startup"
        ""
        "- [ ] Log in to the score server"
        "- [ ] Join/check official Discord announcements"
        "- [ ] List all challenges by category/difficulty"
        "- [ ] Start with beginner/easy web, crypto, rev, misc"
        "- [ ] Create per-challenge folders with ``python tools\new_challenge.py <category> <name>``"
        ""
        "## Live Board"
        ""
        "| Category | Challenge | Difficulty | Owner | Status | Notes |"
        "|---|---|---|---|---|---|"
        "| web | | | | | |"
        "| crypto | | | | | |"
        "| rev | | | | | |"
        "| pwn | | | | | |"
        "| misc | | | | | |"
        ""
        "## Useful Docs"
        ""
        "- ``docs/seccon-beginners-2026.md``"
        "- ``docs/ctf4b-2025-patterns.md``"
    )
    $content | Set-Content -Path $readme -Encoding UTF8
}

Write-Host "Prepared SECCON Beginners CTF 2026 workspace:"
Write-Host $eventDir
