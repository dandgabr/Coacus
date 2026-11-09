#!/usr/bin/env python3
"""
scripts/sync_pencil_skills.py — Synchronize Coacus Canonical UI Styles to Pencil (pen.dev)

Performs deterministic, lossless adaptation of all 82 pure canonical UI styles
from knowledge/skills/domains/design/ui-style-* into ~/.pencil/skills/ui-style-*/,
purges obsolete hybrid directories, updates the central catalog, and verifies
structural integrity.

Author: Coacus Autonomous Pair Programming
Contract: ADR 0008, AGENTS.md (Python standard library only)
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

DEFAULT_COACUS_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COACUS_STYLES = DEFAULT_COACUS_ROOT / "knowledge" / "skills" / "domains" / "design"
DEFAULT_PENCIL_SKILLS = Path(os.path.expanduser("~/.pencil/skills"))
DEFAULT_BACKUP_DIR = Path(os.path.expanduser(f"~/.pencil/skill-backups/{date.today().isoformat()}-pre-sync"))

DEPRECATED_HYBRID_STYLES = [
    "ui-style-art-nouveau-arts-crafts",
    "ui-style-constructivism-propaganda",
    "ui-style-dungeon-synth-dark-fantasy",
    "ui-style-retro-computing-pixel",
    "ui-style-risograph-zine",
    "ui-style-vaporwave-synthwave",
    "ui-style-weirdcore-dreamcore",
]

PENCIL_CANVAS_GUIDELINES = """## Apply it on the Pencil canvas

- Start from the requested screen and preserve its information hierarchy; apply the aesthetic consistently to background, surfaces, typography, controls, icon treatment, and decorative layers.
- Use named frames, components, variables, and native properties. Translate gradients, shadows, blur, borders, texture, and shape cutouts into Pencil fills, strokes, effects, paths, or separate layers.
- Use fonts available in the document. If a defining typeface is unavailable, choose the closest readable visual substitute and note the substitution; do not assume the font was installed.
- Keep functional controls visually identifiable. Make decorative detail subordinate to labels, content, and interaction affordances.
- Do not output frontend implementation or frontend code for a canvas-only request. A Script node is appropriate only when repeated or parameterized geometry is materially easier to generate than to draw."""

STATE_FRAMES_NOTE = """- Treat hover, focus, pressed, loading, success, and error as visual states. Show them in separate labeled frames or component examples; do not claim a static canvas is playing the interaction.
- Include a reduced-motion alternative when the style uses flashing, continuous movement, rapid glitch, parallax, or other strong motion."""

ACCESSIBILITY_CANVAS_NOTE = """- Keep essential information readable without texture, animation, color, or decorative effects. Present focus and other important states explicitly in the canvas."""

RELATED_PENCIL_SKILLS = """## Related Pencil skills

- For choosing and browsing styles, consult `pencil-style-catalog`.
- For visual art direction, combine with `pencil-art-direction`.
- For general interface craft, use `better-ui` or `better-interface` alongside this style when useful."""


def parse_coacus_skill(path: Path) -> tuple[str, str, str, str]:
    """Parse Coacus SKILL.md into (slug, clean_title, canonical_desc, body)."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    slug = path.parent.name
    fm_match = re.match(r"^---\n(.*?)\n---\n+", content, re.DOTALL)
    fm_text = fm_match.group(1) if fm_match else ""
    body = content[fm_match.end():] if fm_match else content

    desc_match = re.search(r"^description:\s*\"?(.*?)\"?$", fm_text, re.MULTILINE)
    canonical_desc = desc_match.group(1).strip() if desc_match else ""

    title_match = re.search(r"^#\s+(?:UI\s+Style:\s*)?(.*)$", body, re.MULTILINE)
    raw_title = title_match.group(1).strip() if title_match else slug
    clean_title = re.sub(r"^[^\w\s]+\s*", "", raw_title).strip()

    return slug, clean_title, canonical_desc, body


def adapt_style_content(slug: str, clean_title: str, canonical_desc: str, body: str) -> str:
    """Adapt canonical Coacus skill markdown for Pencil (.pen) canvas environment."""
    pencil_desc = (
        f"Applies the {clean_title} visual language to a Pencil canvas through palette, "
        "typography, geometry, surfaces, texture, and motion cues. Use when the user requests "
        "this aesthetic or compares visual directions."
    )

    output_lines = [
        "---",
        f"name: {slug}",
        f'description: "{pencil_desc}"',
        "---",
        "",
    ]

    lines = body.splitlines()
    in_integration = False
    canvas_injected = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Intercept and replace Cross-Skill Integration / Dialect Relations
        if re.match(r"^##\s+.*(?:Integration|Cross-Skill|Dialect)", line, re.IGNORECASE):
            in_integration = True
            output_lines.append(RELATED_PENCIL_SKILLS)
            i += 1
            while i < len(lines) and not re.match(r"^##\s+", lines[i]):
                i += 1
            continue

        # Intercept Interaction / Motion section
        if re.match(r"^##\s+.*(?:Interaction|Motion|Animation)", line, re.IGNORECASE):
            if not canvas_injected:
                output_lines.append(PENCIL_CANVAS_GUIDELINES)
                output_lines.append("")
                output_lines.append("---")
                output_lines.append("")
                canvas_injected = True

            output_lines.append(line)
            i += 1
            sec_body = []
            while i < len(lines) and not re.match(r"^##\s+", lines[i]):
                sec_body.append(lines[i])
                i += 1
            sec_text = "\n".join(sec_body).strip()
            if sec_text:
                output_lines.append(sec_text)
                output_lines.append("")
            output_lines.append(STATE_FRAMES_NOTE)
            output_lines.append("")
            continue

        # Intercept Accessibility section
        if re.match(r"^##\s+.*(?:Accessibility|WCAG)", line, re.IGNORECASE):
            output_lines.append(line)
            i += 1
            sec_body = []
            while i < len(lines) and not re.match(r"^##\s+", lines[i]):
                sec_body.append(lines[i])
                i += 1
            sec_text = "\n".join(sec_body).strip()
            if sec_text:
                output_lines.append(sec_text)
                output_lines.append("")
            output_lines.append(ACCESSIBILITY_CANVAS_NOTE)
            output_lines.append("")
            continue

        output_lines.append(line)
        i += 1

    if not canvas_injected:
        output_lines.append("")
        output_lines.append(PENCIL_CANVAS_GUIDELINES)
        output_lines.append("")

    if not in_integration:
        output_lines.append("")
        output_lines.append(RELATED_PENCIL_SKILLS)
        output_lines.append("")

    return "\n".join(output_lines)


def generate_pencil_catalog(styles_data: list[tuple[str, str, str]]) -> str:
    """Generate the full pencil-style-catalog/SKILL.md indexing all 82 styles."""
    total_count = len(styles_data)

    lines = [
        "---",
        "name: pencil-style-catalog",
        f'description: "Lists the {total_count} visual styles adapted for Pencil and helps identify which named style skill to select. Use when browsing, comparing, or choosing a style before designing."',
        "---",
        "",
        "# Pencil Visual Style Catalog",
        "",
        f"Use this catalog to browse and compare the {total_count} pure visual styles available in this Pencil collection. "
        "When applying a named style, select the matching `ui-style-*` skill from the Pencil skill menu as well; "
        "the catalog is an index, not a substitute for that style’s detailed instructions.",
        "",
        "## Canonical Styles Directory",
        "",
    ]

    for slug, clean_title, canonical_desc in sorted(styles_data, key=lambda x: x[0]):
        # Extract a short summary from canonical description
        summary = canonical_desc
        if summary.startswith("Provides the "):
            summary = summary[len("Provides the "):]
        elif summary.startswith("Applies the "):
            summary = summary[len("Applies the "):]
        if ":" in summary:
            summary = summary.split(":", 1)[1].strip()
        # Truncate summary nicely if too long
        if len(summary) > 130:
            cut = summary[:130].rsplit(" ", 1)[0]
            summary = cut + "..."
        if not summary.endswith("."):
            summary += "."

        lines.append(f"- `{slug}` — **{clean_title}.** {summary}")

    lines.extend([
        "",
        "## Selection Guidance",
        "",
        "- **Apply one dominant style per screen.** Mix styles only when the user explicitly requests a hybrid direction, and clearly name which visual elements stem from each direction.",
        "- **Preserve the product's information hierarchy.** Maintain recognizable, accessible controls even when executing highly expressive aesthetics.",
        "- **Fidelity on Canvas:** Translate tokens, gradients, and specular splits into native Pencil fills, strokes, and layer effects. Never emit frontend code for canvas-only tasks.",
        "- **State Coverage:** Model interactive states (hover, focus, pressed, disabled) as separate labeled frames alongside the main design.",
        "- **Reduced Motion:** Always design a static `reduced-motion` alternative frame for motion-heavy or flickering directions.",
        "- **Art Direction:** For end-to-end design guidance across typography, color, and composition, load `pencil-art-direction` alongside your chosen style.",
        "",
    ])

    return "\n".join(lines)


def do_backup(pencil_dir: Path, backup_dir: Path, dry_run: bool = False) -> None:
    """Create a recursive backup of ~/.pencil/skills/."""
    print(f"📦 Backing up {pencil_dir} -> {backup_dir}...")
    if backup_dir.exists():
        print(f"ℹ️ Backup directory already exists: {backup_dir} (preserving existing snapshot)")
        return

    if dry_run:
        print(f"[DRY-RUN] Would copy {pencil_dir} to {backup_dir}")
        return

    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(pencil_dir, backup_dir)
    item_count = len(list(backup_dir.glob("*")))
    print(f"✅ Backup created successfully with {item_count} items.")


def do_purge_deprecated(pencil_dir: Path, dry_run: bool = False) -> list[str]:
    """Purge the 7 deprecated hybrid directories from ~/.pencil/skills/."""
    purged = []
    for dep in DEPRECATED_HYBRID_STYLES:
        target = pencil_dir / dep
        if target.exists() and target.is_dir():
            print(f"🗑️ Purging deprecated hybrid style: {dep}")
            if not dry_run:
                shutil.rmtree(target)
            purged.append(dep)
        else:
            print(f"ℹ️ Deprecated hybrid not present (already removed): {dep}")
    return purged


def do_sync(coacus_styles_dir: Path, pencil_dir: Path, dry_run: bool = False) -> list[tuple[str, str, str]]:
    """Synchronize all 82 canonical UI styles from Coacus to Pencil."""
    coacus_style_dirs = sorted([
        d for d in coacus_styles_dir.glob("ui-style-*")
        if d.is_dir() and (d / "SKILL.md").is_file()
    ])

    print(f"🔄 Found {len(coacus_style_dirs)} canonical UI styles in {coacus_styles_dir}")
    synced_data = []

    for s_dir in coacus_style_dirs:
        coacus_file = s_dir / "SKILL.md"
        slug, clean_title, canonical_desc, body = parse_coacus_skill(coacus_file)
        synced_data.append((slug, clean_title, canonical_desc))

        pencil_style_dir = pencil_dir / slug
        pencil_style_file = pencil_style_dir / "SKILL.md"

        adapted_content = adapt_style_content(slug, clean_title, canonical_desc, body)

        if dry_run:
            print(f"[DRY-RUN] Would write {pencil_style_file} ({len(adapted_content)} bytes)")
        else:
            pencil_style_dir.mkdir(parents=True, exist_ok=True)
            with open(pencil_style_file, "w", encoding="utf-8") as f:
                f.write(adapted_content)

    print(f"✅ Succeeded adapting {len(synced_data)} UI styles.")

    # Generate and write pencil-style-catalog
    catalog_content = generate_pencil_catalog(synced_data)
    catalog_dir = pencil_dir / "pencil-style-catalog"
    catalog_file = catalog_dir / "SKILL.md"

    if dry_run:
        print(f"[DRY-RUN] Would write catalog {catalog_file} ({len(catalog_content)} bytes)")
    else:
        catalog_dir.mkdir(parents=True, exist_ok=True)
        with open(catalog_file, "w", encoding="utf-8") as f:
            f.write(catalog_content)
        print(f"✅ Updated {catalog_file} with {len(synced_data)} styles.")

    return synced_data


def do_verify(coacus_styles_dir: Path, pencil_dir: Path) -> bool:
    """Verify integrity of all 82 styles in Pencil."""
    print(f"\n🔍 Verifying Pencil skills in {pencil_dir}...")
    errors: list[str] = []

    # 1. Check deprecated styles
    for dep in DEPRECATED_HYBRID_STYLES:
        if (pencil_dir / dep).exists():
            errors.append(f"Deprecated hybrid style still present: {dep}")

    # 2. Check canonical styles presence
    coacus_slugs = sorted([
        d.name for d in coacus_styles_dir.glob("ui-style-*")
        if d.is_dir() and (d / "SKILL.md").is_file()
    ])
    pencil_slugs = sorted([
        d.name for d in pencil_dir.glob("ui-style-*")
        if d.is_dir() and (d / "SKILL.md").is_file()
    ])

    if len(pencil_slugs) != len(coacus_slugs):
        errors.append(
            f"Style count mismatch: expected {len(coacus_slugs)} styles, found {len(pencil_slugs)} in Pencil."
        )

    for slug in coacus_slugs:
        s_file = pencil_dir / slug / "SKILL.md"
        if not s_file.exists():
            errors.append(f"Missing canonical style in Pencil: {slug}")
            continue

        with open(s_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Check frontmatter
        if not text.startswith("---"):
            errors.append(f"Style {slug} missing YAML frontmatter")
        if f"name: {slug}" not in text:
            errors.append(f"Style {slug} frontmatter name mismatch")
        if "description:" not in text:
            errors.append(f"Style {slug} frontmatter description missing")

        # Check mandatory Pencil sections
        if "## Apply it on the Pencil canvas" not in text:
            errors.append(f"Style {slug} missing 'Apply it on the Pencil canvas' section")
        if "## Related Pencil skills" not in text:
            errors.append(f"Style {slug} missing 'Related Pencil skills' section")

    # 3. Check catalog
    catalog_file = pencil_dir / "pencil-style-catalog" / "SKILL.md"
    if not catalog_file.exists():
        errors.append("pencil-style-catalog/SKILL.md does not exist")
    else:
        with open(catalog_file, "r", encoding="utf-8") as f:
            cat_text = f.read()
        for slug in coacus_slugs:
            if f"- `{slug}`" not in cat_text:
                errors.append(f"Catalog missing entry for `{slug}`")

    if errors:
        print(f"❌ Verification FAILED with {len(errors)} errors:")
        for err in errors[:20]:
            print(f"   - {err}")
        if len(errors) > 20:
            print(f"   ... and {len(errors) - 20} more errors.")
        return False

    print(f"🎉 Verification PASSED: exactly {len(pencil_slugs)} styles verified, 0 deprecated hybrids, catalog synchronized!")
    return True


def main() -> int:
    """Parse CLI arguments and dispatch the Coacus-to-Pencil style synchronization pipeline."""
    parser = argparse.ArgumentParser(description="Synchronize Coacus Canonical UI Styles to Pencil (pen.dev)")
    parser.add_argument("--pencil-dir", type=Path, default=DEFAULT_PENCIL_SKILLS, help="Target Pencil skills directory")
    parser.add_argument("--coacus-dir", type=Path, default=DEFAULT_COACUS_STYLES, help="Source Coacus design styles directory")
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR, help="Backup destination directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run without writing changes")
    parser.add_argument("--verify-only", action="store_true", help="Only verify existing installation")

    args = parser.parse_args()

    pencil_dir: Path = args.pencil_dir
    coacus_dir: Path = args.coacus_dir
    backup_dir: Path = args.backup_dir
    dry_run: bool = args.dry_run

    if args.verify_only:
        success = do_verify(coacus_dir, pencil_dir)
        return 0 if success else 1

    print("================================================================================")
    print("🚀 COACUS -> PENCIL (pen.dev) STYLE DOMAIN SYNCHRONIZATION")
    print(f"   Source directory: {coacus_dir}")
    print(f"   Target directory: {pencil_dir}")
    print(f"   Backup directory: {backup_dir}")
    print(f"   Dry-run mode: {dry_run}")
    print("================================================================================")

    # 1. Backup
    do_backup(pencil_dir, backup_dir, dry_run=dry_run)

    # 2. Purge deprecated hybrids
    do_purge_deprecated(pencil_dir, dry_run=dry_run)

    # 3. Sync all canonical styles and catalog
    do_sync(coacus_dir, pencil_dir, dry_run=dry_run)

    # 4. Verify
    if not dry_run:
        verified = do_verify(coacus_dir, pencil_dir)
        if not verified:
            return 1

    print("\n✅ Synchronization process completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
