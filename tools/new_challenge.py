from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "web",
    "pwn",
    "crypto",
    "rev",
    "forensics",
    "network",
    "programming",
    "misc",
}


def slugify(value: str) -> str:
    safe = []
    for char in value.strip().lower():
        if char.isalnum():
            safe.append(char)
        elif char in {" ", "-", "_"}:
            safe.append("-")
    slug = "".join(safe).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "challenge"


def create_challenge(category: str, name: str) -> Path:
    if category not in CATEGORIES:
        choices = ", ".join(sorted(CATEGORIES))
        raise ValueError(f"Unknown category '{category}'. Choose one of: {choices}")

    challenge_dir = ROOT / "challenges" / category / slugify(name)
    challenge_dir.mkdir(parents=True, exist_ok=False)

    shutil.copyfile(ROOT / "templates" / "challenge-notes.md", challenge_dir / "notes.md")
    shutil.copyfile(ROOT / "templates" / "writeup.md", challenge_dir / "writeup.md")
    (challenge_dir / "solve.py").write_text(
        "from __future__ import annotations\n\n\n"
        "def main() -> None:\n"
        "    pass\n\n\n"
        "if __name__ == \"__main__\":\n"
        "    main()\n",
        encoding="utf-8",
    )

    return challenge_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a CTF challenge workspace.")
    parser.add_argument("category", choices=sorted(CATEGORIES))
    parser.add_argument("name")
    args = parser.parse_args()

    challenge_dir = create_challenge(args.category, args.name)
    print(challenge_dir)


if __name__ == "__main__":
    main()
