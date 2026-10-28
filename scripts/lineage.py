#!/usr/bin/env python3
"""Build a pattern lineage map ("contains" / "used in") for a component library.

Scans .ts .tsx .js .jsx .svelte .vue .html files under a components root, finds
imports and component or custom-element usages, and prints lineage.md (default)
or lineage.json. Reads custom-elements.json when present to name elements.

A component is a folder directly under the root (or under a tier folder such as
atoms/, molecules/, 00-atoms/), or a single file sitting at that level.
Story, test and spec files are ignored so demos do not count as real usage.

Usage:
  python3 scripts/lineage.py [ROOT] [--consumers DIR ...] [--manifest FILE]
                             [--json] [--out DIR]
  python3 scripts/lineage.py --self-test
"""
import argparse, json, os, re, sys, tempfile

EXTS = {".ts", ".tsx", ".js", ".jsx", ".svelte", ".vue", ".html"}
SKIP_DIRS = {"node_modules", "dist", "build", ".git", "storybook-static", "coverage"}
TIERS = {"atoms", "molecules", "organisms", "templates", "pages"}
TOP_TIERS = {"templates", "pages"}  # expected to have no parents, never orphans
IMPORT_RE = re.compile(r"""(?:\bfrom|\bimport|\brequire)\s*\(?\s*['"]([^'"\n]+)['"]""")
TAG_RE = re.compile(r"<([A-Za-z][\w.-]*)")
DEMO_RE = re.compile(r"\.(stories|story|test|spec)\.")


def kebab(s):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s).replace("_", "-").lower()


def locate(parts):
    """Map path parts relative to the root to (component, tier)."""
    parts = [p for p in parts if p not in ("", ".")]
    tier = None
    if parts and re.sub(r"^\d+-", "", parts[0]).lower() in TIERS:
        tier = re.sub(r"^\d+-", "", parts.pop(0)).lower()
    if not parts:
        return None, tier
    name = parts[0].split(".")[0] if len(parts) == 1 else parts[0]
    return kebab(re.sub(r"^\d+-", "", name)), tier


def walk(top):
    for d, dirs, files in os.walk(top):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1] in EXTS and not DEMO_RE.search(f):
                yield os.path.join(d, f)


def find_manifest(root):
    d = os.path.abspath(root)
    while True:
        p = os.path.join(d, "custom-elements.json")
        if os.path.isfile(p):
            return p
        if os.path.dirname(d) == d:
            return None
        d = os.path.dirname(d)


def read_manifest(path, root, names):
    """Return {tag: component} for custom elements declared in the manifest."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    tags = {}
    for mod in data.get("modules", []):
        for decl in mod.get("declarations", []):
            tag = decl.get("tagName")
            if not tag:
                continue
            src = os.path.join(os.path.dirname(path), mod.get("path", ""))
            rel = os.path.relpath(src, root)
            comp = None if rel.startswith("..") else locate(rel.split(os.sep))[0]
            tags[tag] = comp if comp in names else match_tag(tag, names, {})
    return tags


def match_tag(tag, names, tags):
    if tag in tags:
        return tags[tag]
    t = kebab(tag)
    if "-" not in tag:  # PascalCase framework component: exact name only
        return t if tag[0].isupper() and t in names else None
    # ponytail: suffix match guesses the prefix (<ds-button> -> button); pass a manifest when it guesses wrong
    hits = [n for n in names if t == n or t.endswith("-" + n)]
    return max(hits, key=len) if hits else None


def resolve_import(spec, src_file, root, names):
    if spec.startswith("."):
        target = os.path.normpath(os.path.join(os.path.dirname(src_file), spec))
        rel = os.path.relpath(target, root)
        return None if rel.startswith("..") else locate(rel.split(os.sep))[0]
    # ponytail: aliases resolved only when the specifier names the root folder ($lib/components/x)
    segs = spec.split("/")
    base = os.path.basename(os.path.normpath(root))
    if base in segs[:-1]:
        name = locate(segs[segs.index(base) + 1:])[0]
        return name if name in names else None
    return None


def build(root, consumers=(), manifest=None):
    root = os.path.abspath(root)
    comps = {}
    for f in walk(root):
        name, tier = locate(os.path.relpath(f, root).split(os.sep))
        if name:
            c = comps.setdefault(name, {"tier": tier, "files": 0, "elements": [],
                                        "contains": set(), "used_in": set()})
            c["files"] += 1
    names = set(comps)
    manifest = manifest or find_manifest(root)
    tags = read_manifest(manifest, root, names) if manifest else {}
    for tag, comp in tags.items():
        if comp in comps:
            comps[comp]["elements"].append(tag)

    def scan(path, owner):
        # ponytail: regex over raw text, so commented-out code still counts; fine for a lineage overview
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        used = {resolve_import(s, path, root, names) for s in IMPORT_RE.findall(text)}
        used |= {match_tag(t, names, tags) for t in TAG_RE.findall(text)}
        for u in used - {None, owner}:
            comps[u]["used_in"].add(owner)
            if owner in comps:
                comps[owner]["contains"].add(u)

    for f in walk(root):
        scan(f, locate(os.path.relpath(f, root).split(os.sep))[0])
    for top in consumers:
        for f in walk(top):
            scan(f, "app:" + os.path.relpath(f))
    out = {}
    for n in sorted(comps):
        c = comps[n]
        out[n] = {"tier": c["tier"], "files": c["files"], "elements": sorted(c["elements"]),
                  "contains": sorted(c["contains"]), "used_in": sorted(c["used_in"]),
                  "orphan": not c["used_in"] and c["tier"] not in TOP_TIERS}
    return {"root": root, "manifest": manifest, "components": out}


def to_markdown(data):
    comps = data["components"]
    orphans = [n for n, c in comps.items() if c["orphan"]]
    lines = ["# Pattern lineage", "",
             f"Generated by `scripts/lineage.py` from `{os.path.relpath(data['root'])}`. "
             f"Components: {len(comps)}. Orphans: {len(orphans)}. Regenerate after every change; do not edit by hand.",
             "", "| Component | Tier | Contains | Used in | Flag |", "|---|---|---|---|---|"]
    for n, c in comps.items():
        lines.append(f"| [{n}](#{n}) | {c['tier'] or '-'} | {len(c['contains'])} | "
                     f"{len(c['used_in'])} | {'orphan' if c['orphan'] else ''} |")
    fmt = lambda xs: ", ".join(f"`{x}`" for x in xs) or "none"
    for n, c in comps.items():
        lines += ["", f"## {n}", ""]
        if c["elements"]:
            lines.append("- Element: " + ", ".join(f"`<{t}>`" for t in c["elements"]))
        lines.append(f"- Contains ({len(c['contains'])}): {fmt(c['contains'])}")
        lines.append(f"- Used in ({len(c['used_in'])}): {fmt(c['used_in'])}")
        if c["orphan"]:
            lines.append("- **Orphan:** nothing in the scanned code uses it. Confirm with product "
                         "teams, then deprecate or document why it stays.")
    return "\n".join(lines) + "\n"


def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        files = {
            "src/components/atoms/button/button.ts": "customElements.define('ds-button', class extends HTMLElement {});",
            "src/components/atoms/button/button.stories.ts": "import '../square/Square'; <ds-unused-badge>",
            "src/components/atoms/square/Square.tsx": "export const Square = () => <div/>;",
            "src/components/atoms/unused-badge/unused-badge.svelte": "<span><slot/></span>",
            "src/components/molecules/media-block/MediaBlock.tsx":
                "import { Square } from '../../atoms/square/Square';\nexport default () => <div><Square /><ds-button>Go</ds-button><button/></div>;",
            "src/components/organisms/media-block-list/media-block-list.vue":
                "<template><media-block v-for='x in xs'/></template>\n<script>import MediaBlock from '$lib/components/molecules/media-block';</script>",
            "src/components/templates/home/home.html": "<ds-media-block-list></ds-media-block-list>",
            "app/page.tsx": "export default () => <ds-button>Buy</ds-button>;",
            "custom-elements.json": json.dumps({"modules": [{"path": "src/components/atoms/button/button.ts",
                "declarations": [{"name": "DsButton", "tagName": "ds-button", "customElement": True}]}]}),
        }
        for rel, body in files.items():
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(body)
        cwd = os.getcwd()
        os.chdir(tmp)
        try:
            data = build("src/components", consumers=["app"])
        finally:
            os.chdir(cwd)
        c = data["components"]
        assert set(c) == {"button", "square", "unused-badge", "media-block", "media-block-list", "home"}, c
        assert c["media-block"]["contains"] == ["button", "square"], c["media-block"]
        assert c["media-block"]["used_in"] == ["media-block-list"], c["media-block"]
        assert c["media-block-list"]["used_in"] == ["home"], c["media-block-list"]
        assert c["button"]["used_in"] == ["app:app/page.tsx", "media-block"], c["button"]
        assert c["button"]["elements"] == ["ds-button"] and c["button"]["files"] == 1
        assert c["unused-badge"]["orphan"] and not c["home"]["orphan"] and not c["square"]["orphan"]
        assert c["home"]["tier"] == "templates" and c["square"]["tier"] == "atoms"
        md = to_markdown(data)
        assert "## media-block\n" in md and "**Orphan:**" in md
    print("lineage self-test passed: 6 components, contains/used-in, manifest, consumers, orphans")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("root", nargs="?", default="src/components", help="components root (default: src/components)")
    ap.add_argument("--consumers", action="append", default=[], metavar="DIR",
                    help="app folder whose files count as 'used in' (repeatable)")
    ap.add_argument("--manifest", help="custom-elements.json (default: nearest one above ROOT)")
    ap.add_argument("--json", action="store_true", help="print lineage.json instead of markdown")
    ap.add_argument("--out", metavar="DIR", help="write lineage.md and lineage.json into DIR")
    ap.add_argument("--self-test", action="store_true", help="run the built-in check and exit")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    for d in [a.root, *a.consumers]:
        if not os.path.isdir(d):
            sys.exit(f"error: not a directory: {d}")
    try:
        data = build(a.root, a.consumers, a.manifest)
    except (OSError, ValueError) as e:
        sys.exit(f"error: {e}")
    if not data["components"]:
        sys.exit(f"error: no components found under {a.root}")
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        with open(os.path.join(a.out, "lineage.md"), "w", encoding="utf-8") as fh:
            fh.write(to_markdown(data))
        with open(os.path.join(a.out, "lineage.json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        print(f"wrote {a.out}/lineage.md and {a.out}/lineage.json")
    else:
        print(json.dumps(data, indent=2) if a.json else to_markdown(data), end="")


if __name__ == "__main__":
    main()
