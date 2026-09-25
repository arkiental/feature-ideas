#!/usr/bin/env python3
"""Create and verify a deterministic, minimal skill installation ZIP.

Run: python scripts/package.py [--root PATH] [--output PATH]
No third-party dependencies; Python 3.10 or newer.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import zipfile

VERSION = "1.0.0"
MEMBERS = (
    ("feature-ideas/LICENSE", "LICENSE"),
    ("feature-ideas/SKILL.md", "skills/feature-ideas/SKILL.md"),
    ("feature-ideas/agents/openai.yaml", "skills/feature-ideas/agents/openai.yaml"),
)


def source_bytes(root: Path) -> dict[str, bytes]:
    """Normalize text newlines so Windows and POSIX checkouts produce the same ZIP."""
    result = {}
    for member, relative in MEMBERS:
        source = root / relative
        content = source.read_text(encoding="utf-8")
        if not content.strip():
            raise ValueError(f"Cannot package an empty file: {relative}")
        result[member] = content.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return result


def verify_archive(archive: Path, expected: dict[str, bytes]) -> None:
    with zipfile.ZipFile(archive) as package:
        if package.namelist() != list(expected):
            raise ValueError("Package has unexpected, missing, duplicated, or out-of-order members")
        if package.testzip() is not None:
            raise ValueError("Package integrity verification failed")
        for member, content in expected.items():
            info = package.getinfo(member)
            if info.date_time != (1980, 1, 1, 0, 0, 0):
                raise ValueError(f"Package timestamp is not deterministic: {member}")
            if package.read(member) != content:
                raise ValueError(f"Package content mismatch: {member}")


def build(root: Path, output: Path | None = None, version: str = VERSION) -> Path:
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?", version):
        raise ValueError("Version must be a semantic version such as 1.0.0")
    root = root.resolve()
    output = output.resolve() if output else root / "dist"
    expected = source_bytes(root)  # Read before creating output, so missing input leaves no archive.
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"feature-ideas-{version}.zip"
    temporary = archive.with_suffix(".zip.tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as package:
            for member, content in expected.items():
                info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_STORED
                package.writestr(info, content)
        verify_archive(temporary, expected)
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n", encoding="utf-8", newline="\n")
    return archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root")
    parser.add_argument("--output", type=Path, help="output directory (default: ROOT/dist)")
    parser.add_argument("--version", default=VERSION, help=f"release version (default: {VERSION})")
    args = parser.parse_args()
    try:
        archive = build(args.root, args.output, args.version)
    except (OSError, UnicodeError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Packaging failed: {exc}\n")
    print(f"Created and verified {archive.name} ({archive.stat().st_size:,} bytes)")
    print(f"Output: {archive.parent}")
    print("SHA256SUMS contains the archive checksum. ZIP includes only the skill, agent metadata, and MIT license.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
