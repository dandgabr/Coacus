# Desktop extension practices

Coacus's [GNOME Shell extension skill](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/SKILL.md)
covers GJS extension code, GTK/libadwaita preferences, account coordination,
native popup themes, and package delivery. Its native API examples apply to GNOME;
revalidate them for another runtime. They do not establish KDE support.

## Choose a reference

| Task or symptom | Canonical reference |
|---|---|
| A control saves settings but the visible rows do not change; subscriptions leak after leaving a page. | [Native preferences lifecycle](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/native-preferences-lifecycle.md) |
| Saved accounts appear blocked after login; deletion races a delayed credential operation; a reporting API needs different authorization. | [Accounts and API reporting](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/accounts-and-api-reporting.md) |
| Popup dimensions, gutters, fonts, transparency, light/dark identity, or decoration performance need verification. | [Native layout and theme effects](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/native-layout-and-effects.md) |
| An update must preserve connectors/settings; a public rename affects packaging; installed and loaded versions differ. | [Verification and release](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/verification-and-release.md) |
| A native API name, property or test-harness behavior depends on the Shell runtime. | [Verified native API notes](../../knowledge/skills/engineering/practices/gnome-shell-extension-development/references/gnome-shell-50-notes.md) |

The references carry pinned source evidence and limits. The
[Elfvision consolidation report](../reports/2026-10-08-elfvision-learning-consolidation.md)
records how the lessons were transferred and evaluated. A historical replay is
evidence for its tested path; it does not replace validation of new implementation,
real provider authentication or physical display performance.

## Discovery surfaces

The [human catalog](../../catalog/INDEX.md) and
[machine catalog](../../catalog/catalog.json) index the skill entry. Linked
references provide depth on demand; they are not separate skills. Search or
resolve the canonical entry from the repository root:

```text
python3 scripts/coacus_skill_search.py search "session coordination"
python3 scripts/coacus_skill_search.py show gnome-shell-extension-development
```

Use [the skill-maintenance procedure](../extending.md#update-a-skill-and-its-references)
to change the sources and refresh their generated discovery surfaces.
