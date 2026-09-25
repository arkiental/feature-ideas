#!/usr/bin/env python3
"""Validate the skill, examples, and repository links without network access.

Run from anywhere: python scripts/validate.py [--root PATH]
Development dependencies: PyYAML and Pillow (see requirements-dev.txt).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

try:
    import yaml
    from PIL import Image, UnidentifiedImageError
except ImportError as exc:
    raise SystemExit("Missing development dependency. Run: python -m pip install -r requirements-dev.txt") from exc

SKILL_PATH = Path("skills/feature-ideas")
EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", ".pytest_cache"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".mjs", ".cjs", ".js", ".toml", ".txt", ".svg"}
# Ignore API routes and generic installation examples; flag host-specific filesystem roots.
LOCAL_PATH = re.compile(r"(?i)(?:(?<![a-z0-9])[a-z]:[\\/](?!path(?:[\\/]|\b))[^\s<>\"']+|/(?:Users|home|root|tmp|workspace|mnt|private/var|var/folders)/[^\s<>\"']+)")
INLINE_LINK = re.compile(r"(!?)\[([^\]\n]*)\]\(\s*(<[^>\n]+>|(?:\\.|[^\s)])+)(?:\s+[\"'][^\n]*?[\"'])?\s*\)")
REFERENCE_DEF = re.compile(r"^ {0,3}\[([^\]]+)\]:\s*(<[^>\n]+>|\S+)", re.MULTILINE)
REFERENCE_LINK = re.compile(r"(!?)\[([^\]\n]+)\]\[([^\]\n]*)\]")


def visible_markdown(source: str) -> str:
    """Exclude fenced and inline code, where link-looking text is illustrative."""
    lines = []
    fence = None
    for line in source.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append("")
        elif fence is None:
            lines.append(re.sub(r"(`+).*?\1", "", line))
        else:
            lines.append("")
    return "\n".join(lines)


def markdown_links(source: str):
    """Yield (is_image, accessible_label, target) for inline/reference links."""
    visible = visible_markdown(source)
    refs = {label.casefold(): target for label, target in REFERENCE_DEF.findall(visible)}
    for match in INLINE_LINK.finditer(visible):
        yield bool(match[1]), match[2], match[3].strip("<>")
    for match in REFERENCE_LINK.finditer(visible):
        reference = (match[3] or match[2]).casefold()
        yield bool(match[1]), match[2], refs.get(reference, f"__missing_reference__/{reference}").strip("<>")


def local_target(root: Path, owner: Path, target: str) -> Path | None:
    """Resolve repository links; raise ValueError for absolute or escaping paths."""
    target = re.sub(r"\\([ ()])", r"\1", target)
    if target.startswith(("#", "//")):
        return None
    if re.match(r"^[A-Za-z]:[\\/]", target):
        raise ValueError("absolute machine-local link")
    parsed = urlsplit(target)
    if parsed.scheme:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith(("/", "\\")):
        raise ValueError("absolute local link; use a relative repository path")
    resolved = (owner.parent / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("link escapes the repository")
    return resolved


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_skill(root: Path) -> list[str]:
    errors = []
    path = root / SKILL_PATH / "SKILL.md"
    try:
        source = path.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", source, re.DOTALL)
        if not frontmatter:
            return [f"{SKILL_PATH}/SKILL.md: missing YAML frontmatter"]
        data = yaml.safe_load(frontmatter[1])
        if not isinstance(data, dict):
            return [f"{SKILL_PATH}/SKILL.md: frontmatter must be a mapping"]
        if data.get("name") != "feature-ideas":
            errors.append("SKILL.md: name must be feature-ideas")
        description = data.get("description")
        if not isinstance(description, str) or not 20 <= len(description.strip()) <= 1024:
            errors.append("SKILL.md: description must contain 20–1024 characters")
        if data.get("license") != "MIT":
            errors.append("SKILL.md: license must match the repository's MIT license")
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"SKILL.md: cannot read valid frontmatter ({exc})")
    path = root / SKILL_PATH / "agents/openai.yaml"
    try:
        data = read_yaml(path)
        interface = data.get("interface") if isinstance(data, dict) else None
        if not isinstance(interface, dict):
            errors.append("agents/openai.yaml: interface must be a mapping")
        else:
            if not isinstance(interface.get("display_name"), str) or not interface["display_name"].strip():
                errors.append("agents/openai.yaml: display_name must be nonempty")
            short = interface.get("short_description")
            if not isinstance(short, str) or not 25 <= len(short) <= 64:
                errors.append("agents/openai.yaml: short_description must contain 25–64 characters")
            prompt = interface.get("default_prompt")
            if not isinstance(prompt, str) or not 20 <= len(prompt) <= 1000:
                errors.append("agents/openai.yaml: default_prompt must contain 20–1000 characters")
            elif "$feature-ideas" not in prompt:
                errors.append("agents/openai.yaml: default_prompt must invoke $feature-ideas")
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"agents/openai.yaml: cannot read valid YAML ({exc})")
    return errors


def validate_markdown(root: Path, path: Path) -> list[str]:
    errors = []
    for is_image, label, target in markdown_links(path.read_text(encoding="utf-8")):
        if is_image and not label.strip():
            errors.append(f"{path.relative_to(root)}: image has no descriptive alt text ({target})")
        try:
            resolved = local_target(root, path, target)
            if resolved is not None and not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken relative link: {target}")
        except ValueError as exc:
            errors.append(f"{path.relative_to(root)}: {exc}: {target}")
    return errors


def validate_svg(path: Path) -> list[str]:
    errors = []
    if path.stat().st_size > 2_000_000:
        errors.append(f"{path.name}: SVG exceeds the 2 MB source size limit")
        return errors
    try:
        source = path.read_text(encoding="utf-8")
        if re.search(r"<!DOCTYPE|<!ENTITY", source, re.IGNORECASE):
            return [f"{path.name}: SVG must not declare external entities or a doctype"]
        svg = ET.fromstring(source)
        if svg.tag.split("}")[-1] != "svg":
            errors.append(f"{path.name}: document root is not svg")
        for element in svg.iter():
            tag = element.tag.split("}")[-1].casefold()
            if tag in {"script", "foreignobject"}:
                errors.append(f"{path.name}: unsafe SVG element {tag}")
            for key, value in element.attrib.items():
                attribute = key.split("}")[-1].casefold()
                if attribute.startswith("on"):
                    errors.append(f"{path.name}: SVG event handler {attribute} is forbidden")
                if attribute == "href" and value and not value.startswith("#"):
                    errors.append(f"{path.name}: SVG external href is forbidden")
        if re.search(r"@import|url\(\s*[\"']?(?!#)[^\s)\"']", source, re.IGNORECASE):
            errors.append(f"{path.name}: SVG external CSS resource is forbidden")
    except (OSError, UnicodeError, ET.ParseError) as exc:
        errors.append(f"{path.name}: invalid SVG ({exc})")
    return errors


def validate_png(path: Path) -> list[str]:
    try:
        with Image.open(path) as image:
            if image.format != "PNG":
                return [f"{path.name}: illustration must be PNG"]
            if image.width < 800 or image.height < 450:
                return [f"{path.name}: illustration must be at least 800 × 450 pixels"]
            image.verify()
        with Image.open(path) as image:
            image.load()  # Decode as well as verifying the container.
    except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        return [f"{path.name}: cannot decode illustration ({exc})"]
    return []


def manifest_path(root: Path, value) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("manifest path must be a nonempty string")
    resolved = local_target(root, root / "manifest-owner", value)
    if resolved is None:
        raise ValueError("manifest paths must be local, relative repository paths")
    if not resolved.is_file():
        raise ValueError(f"manifest file does not exist: {value}")
    return resolved


def validate_examples(root: Path) -> list[str]:
    errors = []
    try:
        manifest = json.loads((root / "examples/manifest.json").read_text(encoding="utf-8"))
        if not isinstance(manifest, list) or not manifest:
            return ["examples/manifest.json: expected a nonempty array of examples"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"examples/manifest.json: cannot read manifest ({exc})"]
    identifiers = set()
    for entry in manifest:
        if not isinstance(entry, dict):
            errors.append("examples/manifest.json: each example must be an object")
            continue
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            errors.append("examples/manifest.json: each id must use lowercase words separated by hyphens")
            continue
        if identifier in identifiers:
            errors.append(f"{identifier}: duplicate example ID")
        identifiers.add(identifier)
        try:
            readme = manifest_path(root, entry.get("readme"))
            listed = entry.get("images")
            if not isinstance(listed, list) or not 5 <= len(listed) <= 10:
                errors.append(f"{identifier}: each example must list 5–10 feature images")
                continue
            paths = [manifest_path(root, value) for value in listed]
            if len(set(paths)) != len(paths):
                errors.append(f"{identifier}: illustration paths must be distinct")
            if len({hashlib.sha256(path.read_bytes()).digest() for path in paths}) != len(paths):
                errors.append(f"{identifier}: illustration files must contain distinct images")
            image_links = {}
            for is_image, label, target in markdown_links(readme.read_text(encoding="utf-8")):
                if is_image:
                    resolved = local_target(root, readme, target)
                    if resolved:
                        image_links[resolved] = label.strip()
            for path in paths:
                errors.extend(validate_png(path))
                if not image_links.get(path):
                    errors.append(f"{identifier}: image must be embedded in its README with alt text: {path.relative_to(root)}")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{identifier}: {exc}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = validate_skill(root)
    errors.extend(validate_examples(root))
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in EXCLUDED for part in path.relative_to(root).parts):
            continue
        try:
            if path.suffix.lower() in TEXT_SUFFIXES:
                source = path.read_text(encoding="utf-8")
                for line_number, line in enumerate(source.splitlines(), 1):
                    if LOCAL_PATH.search(line):
                        errors.append(f"{path.relative_to(root)}:{line_number}: machine-local path must not be published")
            if path.suffix.lower() == ".md":
                errors.extend(validate_markdown(root, path))
            if path.suffix.lower() == ".svg":
                errors.extend(validate_svg(path))
            if ".github" in path.relative_to(root).parts and path.suffix.lower() in {".yml", ".yaml"}:
                # Parse only: PyYAML's YAML 1.1 mode maps the GitHub key `on` to True.
                # Do not reject valid workflow structure because of that interpretation.
                data = read_yaml(path)
                if not isinstance(data, dict):
                    errors.append(f"{path.relative_to(root)}: GitHub YAML must contain a mapping")
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root (defaults to this script's repository)")
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print(f"Validation failed: {len(errors)} issue(s).", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("Validation passed: skill metadata, GitHub YAML, example images, SVG safety, and local Markdown links.")
    print("Visual quality and behavioral claims still require human review; this check does not run proposed features.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
