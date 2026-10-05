"""Tests for optional-skills/research/scarf-single-cell — an upstream-maintained catalog stub.

The stub vendors nothing: its metadata.hermes.upstream pointer makes
``hermes skills install official/research/scarf-single-cell`` pull the skill from
NygenAnalytics/scarf. These tests pin the pointer, the install redirect (GitHub mocked, no
network) and the two facts a reader needs before the fetch: which Scarf project it is and the
pinned install line.
"""

from pathlib import Path

from tools.skills_hub_models import SkillBundle
from tools.skills_hub_official import OptionalSkillSource

REPO = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO / "optional-skills" / "research" / "scarf-single-cell"
SKILL_MD = SKILL_DIR / "SKILL.md"
UPSTREAM = {"repo": "NygenAnalytics/scarf", "path": "skills/scarf-single-cell"}


def _source() -> OptionalSkillSource:
    source = OptionalSkillSource()
    source._optional_dir = REPO / "optional-skills"
    return source


def test_stub_points_at_the_maintained_skill_upstream():
    pointer = _source()._upstream_pointer_from_content(SKILL_MD.read_text(encoding="utf-8"))
    assert pointer == UPSTREAM


def test_stub_vendors_nothing_but_skill_md():
    assert sorted(p.name for p in SKILL_DIR.iterdir()) == ["SKILL.md"]


def test_install_redirects_to_upstream_and_relabels_as_official(monkeypatch):
    source = _source()
    fetched = []

    class _FakeGitHub:
        def fetch(self, identifier):
            fetched.append(identifier)
            return SkillBundle(
                name="scarf-single-cell",
                files={"SKILL.md": "---\nname: scarf-single-cell\ndescription: real\n---\nbody",
                       "scripts/inspect_store.py": "print('store')\n"},
                source="github",
                identifier=identifier,
                trust_level="community",
                metadata={"source_url": "https://github.com/NygenAnalytics/scarf"},
            )

    monkeypatch.setattr(source, "_get_github", lambda: _FakeGitHub())

    bundle = source.fetch("official/research/scarf-single-cell")

    assert fetched == ["NygenAnalytics/scarf/skills/scarf-single-cell"]
    assert bundle is not None
    assert bundle.identifier == "official/research/scarf-single-cell"
    assert bundle.source == "official"
    # Curated but third-party content: a dangerous scan verdict must still block.
    assert bundle.trust_level == "trusted"
    assert "scripts/inspect_store.py" in bundle.files
    assert (bundle.metadata["upstream_repo"], bundle.metadata["upstream_path"]) == (
        UPSTREAM["repo"], UPSTREAM["path"])


def test_stub_disambiguates_the_project_and_pins_the_install():
    text = SKILL_MD.read_text(encoding="utf-8")
    # awizemann/scarf (a macOS app for Hermes) also ships skills named scarf-*.
    assert "NygenAnalytics/scarf" in text
    # A bare `scarf[extra]` resolves to 0.32.x: installers skip the 1.0 pre-releases.
    assert 'pip install "scarf[extra]>=1.0.0rc17"' in text
    assert 'pip install "scarf[extra]"' not in text
