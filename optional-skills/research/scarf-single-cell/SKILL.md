---
name: scarf-single-cell
description: Out-of-core single-cell RNA-seq analysis with Scarf.
version: 0.4.0
author: Gautam Ahuja (Gautam8387), Nygen Analytics
license: BSD-3-Clause
platforms: [linux, macos]
metadata:
  hermes:
    tags: [bioinformatics, single-cell, scrna-seq, genomics, zarr, out-of-core, biology, science]
    category: research
    related_skills: [bioinformatics]
    upstream:
      repo: NygenAnalytics/scarf
      path: skills/scarf-single-cell
---

# Scarf Single-Cell (upstream-maintained)

> **Catalog stub.** This entry is maintained upstream at
> [NygenAnalytics/scarf](https://github.com/NygenAnalytics/scarf): the project
> ships the skill directory (`skills/scarf-single-cell/`) with ten reference
> modules and a read-only store inspector (`scripts/inspect_store.py`). `hermes
> skills install official/research/scarf-single-cell` pulls the current tree
> live from that repo (quarantined and scanned like any hub install) — this
> directory holds only the catalog metadata, so the vendored copy can never go
> stale.

Scarf is a Python library for single-cell RNA-seq analysis at million-cell
scale. Counts live in Zarr stores on local disk or object storage (S3, GCS,
Hugging Face); Scarf streams them in bounded blocks under an explicit memory
budget and records every computation as an immutable, content-addressed
artifact with lineage. The skill covers opening, converting and mounting
stores, QC with removal audits, HVG/PCA/neighbour graphs, Leiden/Paris
clustering, UMAP, markers and cautious annotation, batch correction,
donor-level comparisons, headless plotting, provenance and export. It does not
cover `scarf.agent`.

Not to be confused with `awizemann/scarf`, an unrelated macOS app for Hermes
that also ships skills named `scarf-*`.

## Prerequisites

- Python 3.12+ and Scarf 1.0.0rc17 or newer, installed into the environment
  the `terminal` tool runs Python from:
  `pip install "scarf[extra]>=1.0.0rc17"`. Keep the version floor: installers
  skip pre-releases, so a bare `scarf[extra]` resolves to the 0.32 series,
  whose API the skill does not describe. Add `scarf[cytebase]` and network
  access for Cytebase datasets.
- Set the per-process budget before importing Scarf, since the defaults claim
  all detected RAM and every CPU: `SCARF_MEM_BUDGET=8G SCARF_WORKERS=8`.
- Installs pull 12 files (~180 KB) from GitHub; the fetch is pinned to one tree
  SHA, recorded in the bundle metadata.

Full documentation: https://scarf.readthedocs.io/en/latest/
