---
name: astronomical-data-integrity
description: >-
  Guides provenance and coordinate checks for observational astronomy data. Use when analyzing astronomical images, FITS files, sky coordinates, observation times or catalog matches.
---

# Astronomical data integrity

1. Record the dataset, instrument, calibration products, observation time, units and data release. Inspect the file structure and identify the science data and associated uncertainty or quality information before analysis.
2. Preserve the coordinate frame, epoch and time scale. Confirm reference metadata and units before transformations; distinguish a coordinate transformation from relabeling values.
3. For image positions, inspect the world-coordinate system, axis order, dimensionality and pixel-origin convention. Check representative pixel-to-world and inverse transformations against known positions and report missing or ambiguous metadata.
4. For catalog matching, record catalog releases, search radius, separation and matching rules. Report unmatched and ambiguous candidates; a nearest neighbor is not automatically a unique physical counterpart. Account for motion and observation epochs when relevant.
5. Preserve uncertainty, masks and calibration assumptions in derived products. A syntactically valid file or successful transform does not establish observational calibration or scientific validity.

See the official [world-coordinate documentation](https://docs.astropy.org/en/stable/wcs/) and [coordinate matching documentation](https://docs.astropy.org/en/stable/coordinates/matchsep.html) for the selected implementation. The workflow was informed by the [upstream astronomy skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/astropy/SKILL.md).
