#!/usr/bin/env python3
"""Validate DTCG 2025.10 design token files, optionally through a resolver document.

  validate_tokens.py tokens/primitives.brand-a.json tokens/semantic.json ...
      Merge the files in order (later tokens replace earlier ones) and validate the result.
  validate_tokens.py --resolver tokens/tokens.resolver.json
      Check the resolver, then validate every permutation it describes.
  validate_tokens.py --self-test

Checks: $value present, $type resolvable (own, alias target, or parent group), known types,
well-formed values per type (color objects, px|rem dimensions, ms|s durations, composites),
aliases resolve to tokens of the right type with no cycles, $deprecated strings name a
replacement as {token.path}. Prints a markdown report; exits 1 on any error.
"""
import argparse, itertools, json, re, sys
from pathlib import Path

ALIAS = re.compile(r"^\{([^{}]+)\}$")
num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
unit = lambda units: lambda v: isinstance(v, dict) and num(v.get("value")) and v.get("unit") in units
SPACES = {"srgb", "srgb-linear", "hsl", "hwb", "lab", "lch", "oklab", "oklch", "display-p3",
          "a98-rgb", "prophoto-rgb", "rec2020", "xyz-d65", "xyz-d50"}
WEIGHTS = {"thin", "hairline", "extra-light", "ultra-light", "light", "normal", "regular", "book", "medium",
           "semi-bold", "demi-bold", "bold", "extra-bold", "ultra-bold", "black", "heavy", "extra-black", "ultra-black"}
SIMPLE = {  # type: (predicate, rule shown on failure)
    "dimension": (unit(("px", "rem")), "must be {value: number, unit: px|rem}"),
    "duration": (unit(("ms", "s")), "must be {value: number, unit: ms|s}"),
    "number": (num, "must be a JSON number"),
    "fontFamily": (lambda v: isinstance(v, str) or (isinstance(v, list) and v and all(isinstance(x, str) for x in v)),
                   "must be a string or list of strings"),
    "fontWeight": (lambda v: (num(v) and 1 <= v <= 1000) or v in WEIGHTS, "must be 1-1000 or a named weight"),
    "cubicBezier": (lambda v: isinstance(v, list) and len(v) == 4 and all(map(num, v)) and 0 <= v[0] <= 1 and 0 <= v[2] <= 1,
                    "must be [x1, y1, x2, y2] with x in 0-1"),
    "strokeStyle": (lambda v: v in {"solid", "dashed", "dotted", "double", "groove", "ridge", "outset", "inset"}
                    or (isinstance(v, dict) and isinstance(v.get("dashArray"), list) and v.get("lineCap") in ("round", "butt", "square")),
                    "must be a style keyword or {dashArray, lineCap}"),
}
COMPOSITE = {
    "border": {"color": "color", "width": "dimension", "style": "strokeStyle"},
    "transition": {"duration": "duration", "delay": "duration", "timingFunction": "cubicBezier"},
    "shadow": {"color": "color", "offsetX": "dimension", "offsetY": "dimension", "blur": "dimension", "spread": "dimension"},
    "typography": {"fontFamily": "fontFamily", "fontSize": "dimension", "fontWeight": "fontWeight",
                   "letterSpacing": "dimension", "lineHeight": "number"},
    "gradient-stop": {"color": "color", "position": "number"},
}
TYPES = ({"color", "gradient"} | set(SIMPLE) | set(COMPOSITE)) - {"gradient-stop"}
GROUP_PROPS = {"$type", "$description", "$extensions", "$deprecated", "$schema"}
TOKEN_PROPS = {"$value", "$type", "$description", "$extensions", "$deprecated"}


def merge(into, frm):
    """Resolver merge: groups merge into fresh dicts; a token replaces (kept by identity for origins)."""
    for k, v in frm.items():
        if isinstance(v, dict) and "$value" not in v:
            if not (isinstance(into.get(k), dict) and "$value" not in into[k]):
                into[k] = {}
            merge(into[k], v)
        else:
            into[k] = v
    return into


def validate(sources):
    """sources: list of (label, dict). Returns ([(where, message)], token count)."""
    origin, tree, errs, toks, group_deps = {}, {}, [], {}, []

    def tag(d, label):
        if isinstance(d, dict):
            origin[id(d)] = label
            for x in d.values():
                tag(x, label)
    for label, doc in sources:
        tag(doc, label)
        merge(tree, doc)

    def walk(node, path, gtype):
        where = ".".join(path) or "(root)"
        gtype = node.get("$type", gtype)
        for k, v in node.items():
            if k.startswith("$") and k != "$root":
                if k not in GROUP_PROPS:  # includes $extends, which this tool does not expand
                    errs.append((where, f"unsupported group property {k}"))
                continue
            p = ".".join(path + (k,))
            if re.search(r"[{}.]", k):
                errs.append((p, "names must not contain { } or ."))
            if not isinstance(v, dict):
                errs.append((p, "expected a token or group object"))
            elif "$value" in v:
                toks[p] = (v, gtype, origin.get(id(v), "?"))
            elif "value" in v or ("$type" in v and all(x.startswith("$") for x in v)):
                errs.append((p, "token has no $value (DTCG keys start with $)"))
            else:
                walk(v, path + (k,), gtype)
        if isinstance(node.get("$deprecated"), str):
            group_deps.append((where, node["$deprecated"]))

    def follow(path):
        """Walk an alias chain. Returns (concrete token path, None) or (None, problem)."""
        seen = []
        while path in toks:
            if path in seen:
                return None, "alias chain loops: " + " -> ".join(seen + [path])
            seen.append(path)
            m = isinstance(toks[path][0]["$value"], str) and ALIAS.match(toks[path][0]["$value"])
            if not m:
                return path, None
            path = m[1]
        return None, f"alias {{{path}}} does not resolve to a token"

    def type_of(path):
        tok, gtype, _ = toks[path]
        if "$type" in tok:
            return tok["$type"]
        end = follow(path)[0]
        return gtype if end == path else end and type_of(end)

    def deprecated(text):
        refs = re.findall(r"\{([^{}]+)\}", text)
        return ([] if refs else ["$deprecated string must name a replacement as {token.path}"]) + [
            f"$deprecated replacement {{{r}}} does not resolve" for r in refs if r not in toks]

    def check(v, typ):
        if isinstance(v, str) and ALIAS.match(v):
            end, problem = follow(ALIAS.match(v)[1])
            t = end and type_of(end)
            return [problem] if problem else [] if t == typ else [f"alias {v} has type {t}, expected {typ}"]
        if isinstance(v, dict) and set(v) == {"$ref"}:
            return []  # JSON Pointer reference: left to the build tool
        if typ == "color":
            if not isinstance(v, dict):
                return [f"color {v!r} must be {{colorSpace, components, hex?}}; hex strings are invalid in 2025.10"]
            c = v.get("components")
            return [m for bad, m in (
                (v.get("colorSpace") not in SPACES, f"unknown colorSpace {v.get('colorSpace')!r}"),
                (not (isinstance(c, list) and len(c) == 3 and all(num(x) or x == "none" for x in c)), "components must be 3 numbers (or 'none')"),
                ("alpha" in v and not (num(v["alpha"]) and 0 <= v["alpha"] <= 1), "alpha must be a number from 0 to 1"),
                ("hex" in v and not re.fullmatch(r"#[0-9a-fA-F]{6}", str(v.get("hex"))), f"hex fallback {v.get('hex')!r} must be 6-digit #rrggbb"),
            ) if bad]
        if typ in SIMPLE:
            ok, rule = SIMPLE[typ]
            return [] if ok(v) else [f"{typ} {rule}, got {json.dumps(v)}"]
        if typ in ("gradient", "shadow") and isinstance(v, list):
            return [m for s in v for m in check(s, "gradient-stop" if typ == "gradient" else "shadow")]
        if typ in COMPOSITE and isinstance(v, dict):
            want = COMPOSITE[typ]
            extra = sorted(set(v) - set(want) - ({"inset"} if typ == "shadow" else set()))
            return ([f"{typ} is missing {k}" for k in want if k not in v] + [f"{typ} has unknown key {k}" for k in extra]
                    + [m for k, t in want.items() if k in v for m in check(v[k], t)])
        return [f"{typ} value has the wrong shape: {json.dumps(v)}"]

    walk(tree, (), None)
    errs += [(w, m) for w, text in group_deps for m in deprecated(text)]
    for path, (tok, _, src) in sorted(toks.items()):
        typ, extra = type_of(path), [k for k in tok if k not in TOKEN_PROPS]
        first = ((extra and f"unexpected keys {extra}; a token cannot also be a group") or follow(path)[1]
                 or (not typ and "no $type: set it on the token or a parent group")
                 or (typ not in TYPES and f"unknown $type {typ!r}"))
        msgs = [first] if first else check(tok["$value"], typ)
        if isinstance(tok.get("$deprecated"), str):
            msgs += deprecated(tok["$deprecated"])
        errs += [(f"{path} ({src})", m) for m in msgs]
    return errs, len(toks)


def resolver_permutations(doc, load):
    """Check a resolver doc; load(ref) -> dict or None. Returns (errors, warnings, [(label, sources)])."""
    errs, warns = [], []
    sets, mods, order = doc.get("sets", {}), doc.get("modifiers", {}), doc.get("resolutionOrder")
    if doc.get("version") != "2025.10":
        errs.append(("resolver", 'version must be "2025.10"'))
    for name, s in sets.items():
        if not isinstance(s.get("sources"), list):
            errs.append((f"sets.{name}", "set needs a sources array"))
    for name, m in mods.items():
        if len(m.get("contexts") or {}) < 2:
            errs.append((f"modifiers.{name}", f"modifier needs 2 or more contexts, has {len(m.get('contexts') or {})}"))
        if "default" in m and m["default"] not in (m.get("contexts") or {}):
            errs.append((f"modifiers.{name}", f"default {m['default']!r} is not a context"))
    if not isinstance(order, list):
        return errs + [("resolver", "resolutionOrder array is required")], warns, []

    def sources(lst, where, in_set):
        out = []
        for s in lst:
            ref = s.get("$ref") if isinstance(s, dict) else None
            if ref is None:
                out.append((f"resolver:{where}", s))
            elif ref.startswith("#/resolutionOrder") or (in_set and ref.startswith("#/modifiers/")):
                errs.append((where, f"{ref} may not be referenced here"))
            elif ref.startswith("#/sets/"):
                if ref[7:] in sets:
                    out += sources(sets[ref[7:]].get("sources", []), f"sets.{ref[7:]}", True)
                else:
                    errs.append((where, f"{ref} does not exist"))
            elif load(ref) is None:
                out.append(None)
                warns.append((where, f"{ref} not found (permutations using it are skipped)"))
            else:
                out.append((ref, load(ref)))
        return out

    steps = []  # per resolutionOrder item: alternatives of (label, sources)
    for i, item in enumerate(order):
        ref = item.get("$ref")
        kind, _, name = ref[2:].partition("/") if ref else (str(item.get("type")) + "s", "", item.get("name"))
        body = item if not ref else {"sets": sets, "modifiers": mods}.get(kind, {}).get(name)
        if body is None or (not ref and not (name and kind in ("sets", "modifiers"))):
            errs.append((f"resolutionOrder[{i}]", f"{ref} does not exist" if ref else "inline item needs name and type"))
        elif kind == "sets":
            steps.append([("", sources(body.get("sources", []), f"sets.{name}", True))])
        else:
            steps.append([(f"{name}={c}", sources(lst, f"modifiers.{name}.{c}", False)) for c, lst in body.get("contexts", {}).items()])
    perms = [(", ".join(lbl for lbl, _ in combo if lbl) or "default", [s for _, lst in combo for s in lst])
             for combo in itertools.product(*steps)]
    return errs, warns, perms


def run_resolver(doc, load):
    errs, warns, perms = resolver_permutations(doc, load)
    seen, ntok, skipped = set(), 0, 0
    for label, srcs in perms:
        if None in srcs:
            skipped += 1
            continue
        perr, n = validate(srcs)
        ntok = max(ntok, n)
        errs += [(w, f"{m} [in {label}]") for w, m in perr if (w, m) not in seen and not seen.add((w, m))]
    return errs, warns, ntok, len(perms), skipped


def report(title, errs, warns, ntok, perms=None, skipped=0):
    out = [f"# Token validation: {title}", "", f"- Tokens checked: {ntok}"]
    if perms is not None:
        out.append(f"- Permutations: {perms} ({skipped} skipped for missing files)")
    for head, items in (("Errors", errs), ("Warnings", warns)):
        if items:
            out += ["", f"## {head} ({len(items)})", ""] + [f"- `{w}`: {m}" for w, m in items]
    return "\n".join(out + ["", f"**Result: {'FAIL' if errs else 'PASS'}**"])


def self_test():
    prim = {"color": {"$type": "color", "n": {"0": {"$value": {"colorSpace": "oklch", "components": [1, 0, 0], "hex": "#ffffff"}}}},
            "space": {"$type": "dimension", "2": {"$value": {"value": 0.5, "unit": "rem"}}}}
    sem = {"color": {"$type": "color", "bg": {"$value": "{color.n.0}"},
                     "old": {"$value": "{color.bg}", "$deprecated": "Use {color.bg} instead."}},
           "type": {"$type": "typography", "body": {"$value": {"fontFamily": "x", "fontSize": "{space.2}", "fontWeight": 400,
                                                                "letterSpacing": {"value": 0, "unit": "px"}, "lineHeight": 1.5}}}}
    errs, n = validate([("p", prim), ("s", sem)])
    assert not errs and n == 5, errs
    bad = {"c": {"$type": "color", "hexstr": {"$value": "#ff0000"}, "space": {"$value": {"colorSpace": "rgb", "components": [1, 0]}},
                 "hex": {"$value": {"colorSpace": "srgb", "components": [1, 0, 0], "hex": "#f00"}},
                 "a": {"$value": "{c.b}"}, "b": {"$value": "{c.a}"}, "miss": {"$value": "{c.nope}"},
                 "dep": {"$value": "{c.hex}", "$deprecated": "old"}, "both": {"$value": "{c.hex}", "child": {"$value": 1}}},
           "d": {"em": {"$type": "dimension", "$value": {"value": 1, "unit": "em"}}, "untyped": {"$value": 3},
                 "weird": {"$type": "size", "$value": 1}, "wrong": {"$type": "dimension", "$value": "{c.hex}"},
                 "legacy": {"value": 1, "type": "number"}}}
    msgs = " | ".join(m for _, m in validate([("bad", bad)])[0])
    for want in ("hex strings are invalid", "unknown colorSpace", "components must be 3", "6-digit", "loops",
                 "does not resolve", "name a replacement", "cannot also be a group", "unit: px|rem", "no $type",
                 "unknown $type", "has type color, expected dimension", "has no $value"):
        assert want in msgs, f"missing check: {want}\n{msgs}"
    res = {"version": "2025.10", "sets": {"base": {"sources": [{"$ref": "p.json"}, {"$ref": "s.json"}]}},
           "modifiers": {"scheme": {"contexts": {"light": [], "dark": [{"color": {"bg": {"$value": "{color.n.0}"}}}]}, "default": "light"},
                         "solo": {"contexts": {"only": []}}},
           "resolutionOrder": [{"$ref": "#/sets/base"}, {"$ref": "#/modifiers/scheme"}, {"$ref": "#/sets/ghost"}]}
    errs, _, _, perms, _ = run_resolver(res, {"p.json": prim, "s.json": sem}.get)
    msgs = " | ".join(m for _, m in errs)
    assert perms == 2 and "2 or more contexts" in msgs and "#/sets/ghost does not exist" in msgs, msgs
    print("self-test passed: valid set clean; 13 token checks and 2 resolver checks fire")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", type=Path, help="DTCG token files, merged in the given order")
    ap.add_argument("--resolver", type=Path, help="resolver document; validates every permutation")
    ap.add_argument("--self-test", action="store_true", help="run the built-in check and exit")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.resolver:
        load = lambda ref: json.loads((a.resolver.parent / ref).read_text()) if (a.resolver.parent / ref).is_file() else None
        errs, warns, ntok, perms, skipped = run_resolver(json.loads(a.resolver.read_text()), load)
        print(report(str(a.resolver), errs, warns, ntok, perms, skipped))
    elif a.files:
        errs, ntok = validate([(str(f), json.loads(f.read_text())) for f in a.files])
        print(report(", ".join(map(str, a.files)), errs, [], ntok))
    else:
        ap.error("give token files or --resolver")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
