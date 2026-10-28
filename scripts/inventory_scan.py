#!/usr/bin/env python3
"""Static half of an interface inventory: count the colors, type, spacing, radii, shadows,
buttons and inputs a codebase really uses, so the team sees "37 button styles" as data before
the screenshot session. Regex only, no parsers: every number is a candidate, not a decision.

Usage: inventory_scan.py ROOT [ROOT ...] [--out DIR] [--ignore GLOB ...] | --self-test
Writes DIR/scan.json and DIR/scan.md. Exits 0 after any scan, 2 on bad arguments.
"""
import argparse, bisect, colorsys, fnmatch, json, math, os, pathlib, re, sys, tempfile
from collections import defaultdict

EXTS = ('.css', '.scss', '.less', '.html', '.htm', '.jsx', '.tsx', '.vue', '.svelte', '.astro', '.ts')
IGNORE = ['node_modules', 'dist', 'build', '.git', 'coverage', 'storybook-static']
NAMED = set("""aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown
burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod
darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen
darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue
firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew
hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan
lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray
lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid
mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream
mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod palegreen
paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown
royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey snow
springgreen steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen""".split())
# key: (title, rough target). Targets are rules of thumb (beyond the book), not limits.
CATS = {
    'colors': ('Colors', '1 neutral ramp + 1-2 brand accents + status colors'),
    'font_family': ('Font families', '1-2 families (+ 1 mono)'),
    'font_size': ('Font sizes', 'type scale of 6-8 sizes'), 'font_weight': ('Font weights', '2-4 weights'),
    'line_height': ('Line heights', '2-3 (tight, body, loose)'),
    'spacing': ('Spacing (margin/padding/gap)', 'one spacing scale, 8-12 steps'),
    'border_radius': ('Border radii', '3-4 (none, small, medium, full)'),
    'box_shadow': ('Box shadows', '3-5 elevation levels'), 'z_index': ('z-index values', '5-8 named layers'),
    'durations': ('Transition/animation durations', '3-4 durations'), 'easings': ('Easings', '2-4 easings'),
    'breakpoints': ('Breakpoints (media/container queries)', '3-5 breakpoints'),
    'custom_properties': ('Existing variables (--*, $scss, @less)', 'map onto tokens; no target'),
    'buttons': ('Button-like patterns', '1 button component: a few variants x sizes'),
    'inputs': ('Input-like patterns', '1 component per control type'),
    'headings': ('Heading styles (h1-h6)', '6 levels mapped to the type scale')}
COLOR_RE = re.compile(r'#[0-9a-f]{3,8}(?![\w-])|(?:rgba?|hsla?|oklch|oklab|lab|lch|hwb|color)\([^()]*\)'
                      r'|(?<![\w.#$@-])[a-z]+(?![\w(-])')
NO_COLOR = {'font-family', 'font', 'content', 'grid-area', 'grid-template-areas', 'animation-name',
            'transition-property', 'will-change', 'list-style-type', 'counter-reset'}
GLOBAL_KW = {'inherit', 'initial', 'unset', 'revert', 'revert-layer'}
TOKEN_RE = re.compile(r'[^\s(]+(?:\([^)]*\))?')
UNITLESS = {'font-weight', 'line-height', 'z-index', 'opacity', 'flex', 'flex-grow', 'flex-shrink', 'order'}
DECL_RE = re.compile(r'(?<![\w$@-])(--[\w-]+|[$@][\w-]+|[a-zA-Z-]+)\s*:\s*([^;{}]+?)\s*(?=;|\}|$)')
RULE_RE = re.compile(r'([^{};]+)\{([^{}]*)')  # body = decls before any nested rule
TAG_RE = re.compile(r'(?<![\w$.])<([A-Za-z][\w:.-]*)(\s[^>]*)?>')
CLASS_RE = re.compile(r'(?<![\w-])(?:class|className|:class|class:list)\s*=\s*'
                      r'(?:"([^"]*)"|\'([^\']*)\'|\{\s*["\'`]([^"\'`]*)["\'`]\s*\})')
PROP_RE = re.compile(r'(?<![\w-])(variant|size|kind|color|appearance)\s*=\s*["\']([^"\']+)')

def norm(v):
    v = {'white': '#fff', 'black': '#000'}.get(v.strip().lower(), v)
    v = re.sub(r'\s+', ' ', v.lower().replace('!important', '')).strip()
    v = re.sub(r'\s*,\s*', ', ', re.sub(r'\(\s+', '(', re.sub(r'\s+\)', ')', v)))
    v = re.sub(r'#([0-9a-f])([0-9a-f])([0-9a-f])([0-9a-f])?\b',
               lambda m: '#' + ''.join(c * 2 for c in m.groups() if c), v)
    v = re.sub(r'(?<![\w.])0(?:\.0+)?(?:px|rem|em|pt)\b', '0', v)
    return re.sub(r'(?<![\w.])\.(\d)', r'0.\1', v)

unit = lambda t: ((m.group(1) or 'unitless') if (m := re.fullmatch(r'-?[\d.]+([a-z%]*)', t))
                 else t.split('(')[0] if '(' in t else 'keyword')

def to_px(v):  # ponytail: assumes a 16px root for rem/em; good enough for "within 1px" hints
    m = re.fullmatch(r'(-?\d*\.?\d+)(px|rem|em)?', v)
    return None if not m else float(m.group(1)) * (16 if m.group(2) in ('rem', 'em') else 1)

def to_rgb(v):  # ponytail: hex/rgb/hsl only, alpha ignored; oklch/lab/named skip the distance check
    if re.fullmatch(r'#[0-9a-f]{6}([0-9a-f]{2})?', v):
        return tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
    m = re.fullmatch(r'(rgba?|hsla?)\(([^)]*)\)', v)
    if not m or len(nums := re.findall(r'-?\d*\.?\d+%?', m.group(2))[:3]) < 3:
        return None
    if m.group(1).startswith('rgb'):
        return tuple(float(n[:-1]) * 2.55 if n.endswith('%') else float(n) for n in nums)
    h, s, l = (float(n.rstrip('%')) for n in nums)
    return tuple(c * 255 for c in colorsys.hls_to_rgb(h / 360 % 1, l / 100, s / 100))

class Inventory:
    def __init__(self):
        self.data, self.files = defaultdict(dict), 0
    def add(self, cat, value, where, group=None):
        e = self.data[cat].setdefault(value, {'count': 0, 'examples': [], 'group': group})
        e['count'] += 1
        if len(e['examples']) < 3 and where not in e['examples']:
            e['examples'].append(where)
    def decl(self, prop, raw, where):
        prop, v = prop.strip(), norm(raw)
        if not v or v in GLOBAL_KW:
            return
        if prop.startswith(('--', '$', '@')):
            self.add('custom_properties', prop, where)
        if prop not in NO_COLOR:
            for c in COLOR_RE.findall(re.sub(r'url\([^)]*\)|var\([^)]*\)', '', v)):
                if c in NAMED or '(' in c or (c[0] == '#' and len(c) in (7, 9)):
                    self.add('colors', c, where)
        if prop == 'font':  # shorthand: [style weight] size[/line-height] family
            m = re.fullmatch(r'(?:(.*?)\s+)?(\d*\.?\d+[a-z%]+|(?:x*-)?(?:small|large)|medium)'
                             r'(?:\s*/\s*(\S+))?\s+(.+)', v)
            if m:
                weights = [('font-weight', w) for w in re.findall(r'\b(?:[1-9]00|bold|bolder|lighter)\b', m.group(1) or '')]
                for p, val in weights + list(zip(('font-size', 'line-height', 'font-family'), m.groups()[1:])):
                    val and self.decl(p, val, where)
        simple = {'font-family': 'font_family', 'font-size': 'font_size', 'font-weight': 'font_weight',
                  'line-height': 'line_height', 'z-index': 'z_index', 'box-shadow': 'box_shadow'}
        if prop in simple:
            self.add(simple[prop], v, where)
        elif re.fullmatch(r'(margin|padding)(-[a-z-]+)?|(row-|column-|grid-)?gap', prop):
            for t in TOKEN_RE.findall(v):
                self.add('spacing', t, where, unit(t))
        elif 'radius' in prop:
            for t in TOKEN_RE.findall(v.replace('/', ' ')):
                self.add('border_radius', t, where)
        elif prop.startswith(('transition', 'animation')):
            for d in re.findall(r'(?<![\w.-])\d*\.?\d+m?s\b', v):
                self.add('durations', d, where)
            for e in re.findall(r'ease(?:-in-out|-in|-out)?|linear(?:\([^)]*\))?|cubic-bezier\([^)]*\)|steps\([^)]*\)', v):
                self.add('easings', e, where)
    def css(self, text, base, loc):
        text = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m.group()), text, flags=re.S)
        for m in DECL_RE.finditer(text):
            self.decl(m.group(1), m.group(2), loc(base + m.start()))
        for m in re.finditer(r'@(media|container)([^{;]*)\{', text):
            for a, b in re.findall(r'(?:width|inline-size)\s*(?::|[<>]=?)\s*(\d*\.?\d+[a-z]+)'
                                   r'|(\d*\.?\d+[a-z]+)\s*[<>]=?\s*(?:width|inline-size)', m.group(2)):
                self.add('breakpoints', f'{norm(a or b)} (@{m.group(1)})', loc(base + m.start()), m.group(1))
        for m in RULE_RE.finditer(text):
            where = loc(base + m.start(1) + len(m.group(1)) - len(m.group(1).lstrip()))
            for part in m.group(1).split(','):
                compounds = [re.sub(r'::?[\w-]+(\([^)]*\))?', '', c) for c in re.split(r'[\s>+~]+', part.strip()) if c]
                for c in compounds:
                    if re.search(r'btn|button', c, re.I):
                        self.add('buttons', f'selector {c}', where, 'css')
                    elif re.search(r'input|(?<!set-)field(?!set)|form-control|select|textarea', c, re.I):
                        self.add('inputs', f'selector {c}', where, 'css')
                h = re.fullmatch(r'\.?(h[1-6])', compounds[-1]) if compounds else None
                if h:
                    sig = '; '.join(f'{p}: {norm(v)}' for p, v in DECL_RE.findall(m.group(2))
                                    if p.startswith(('font', 'line-height', 'letter-spacing', 'text-transform')))
                    if sig: self.add('headings', f'{h.group(1)} {{ {sig} }}', where, h.group(1))
    def markup(self, text, base, loc):
        for m in re.finditer(r'<style[^>]*>(.*?)</style>', text, re.S | re.I):
            self.css(m.group(1), base + m.start(1), loc)
        for m in re.finditer(r'\bstyle\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', text):
            self.css(m.group(1) or m.group(2) or '', base + m.start(), loc)
        for m in re.finditer(r'(?:\bcss|styled\.\w+|styled\([^)]*\)|createGlobalStyle|keyframes)\s*`([^`]*)`', text):
            self.css(m.group(1), base + m.start(1), loc)
        for m in re.finditer(r'style=\{\{(.*?)\}\}', text, re.S):
            for k in re.finditer(r'(\w+)\s*:\s*(?:([\'"])(.*?)\2|(-?\d*\.?\d+)(?![\w.]))', m.group(1)):
                prop, v = re.sub(r'([A-Z])', r'-\1', k.group(1)).lower(), k.group(3) or k.group(4)
                if k.group(4) and prop not in UNITLESS and float(v) != 0:
                    v += 'px'
                self.decl(prop, v, loc(base + m.start(1) + k.start()))
        for m in re.finditer(r'\b(fill|stroke|bgcolor|stop-color)\s*=\s*["\']([^"\']+)', text):
            self.decl(m.group(1), m.group(2), loc(base + m.start()))
        for m in TAG_RE.finditer(text):
            tag, attrs = m.group(1), m.group(2) or ''
            t, where = tag.lower(), loc(base + m.start())
            c = CLASS_RE.search(attrs)
            classes = sorted({x for x in (c and (c.group(1) or c.group(2) or c.group(3)) or '').split()
                              if re.fullmatch(r'[\w:/-]+', x)})
            typ = ty.group(1).lower() if (ty := re.search(r'(?<![\w-])type\s*=\s*["\']?([\w-]+)', attrs)) else ''
            key = f'<{tag}' + (f' type={typ}' if typ and 'button' not in t else '') + '>' \
                + (' .' + '.'.join(classes) if classes else '') \
                + ''.join(f' {p}={v}' for p, v in PROP_RE.findall(attrs))
            cls = ' '.join(classes)
            if ('button' in t or re.search(r'role\s*=\s*["\']button', attrs) or re.search(r'btn|button', cls, re.I)
                    or (t == 'input' and typ in ('submit', 'button', 'reset'))):
                self.add('buttons', key, where, 'markup')
            elif (re.search(r'input|select|textarea|field', t) and t != 'fieldset') \
                    or re.search(r'input|field|form-control', cls, re.I):
                self.add('inputs', key, where, 'markup')
    def scan_file(self, path):
        text = pathlib.Path(path).read_text(encoding='utf-8', errors='replace')
        nl = [m.start() for m in re.finditer('\n', text)]
        loc = lambda pos: f'{path}:{bisect.bisect_left(nl, pos) + 1}'
        if path.endswith('.ts') and '@Component' not in text:
            return
        if path.endswith(('.css', '.scss', '.less')):
            self.css(text, 0, loc)
        elif path.endswith('.ts'):  # Angular inline templates/styles only
            for m in re.finditer(r'template\s*:\s*`([^`]*)`', text):
                self.markup(m.group(1), m.start(1), loc)
            for m in re.finditer(r'styles?\s*:\s*(\[[^\]]*\]|`[^`]*`)', text):
                for s in re.finditer(r'`([^`]*)`', m.group(1)):
                    self.css(s.group(1), m.start(1) + s.start(1), loc)
        else:
            self.markup(text, 0, loc)
        self.files += 1

def near(values, conv, limit):  # ponytail: O(n^2) over distinct values; fine below a few thousand
    pts = [(v, p) for v in values if (p := conv(v)) is not None]
    out = []
    for i, (a, p) in enumerate(pts):
        for b, q in pts[i + 1:]:
            d = math.dist(p, q) if isinstance(p, tuple) else abs(p - q)
            if d <= limit:
                out.append({'a': a, 'b': b, 'distance': round(d, 2)})
    return sorted(out, key=lambda h: h['distance'])

def scan(roots, ignore):
    inv = Inventory()
    skip = lambda name, rel: any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch(rel, g) for g in ignore)
    for root in roots:  # a file root walks nothing and is scanned as itself
        paths = [root] if os.path.isfile(root) else []
        for d, dirs, files in os.walk(root):
            dirs[:] = sorted(x for x in dirs if not skip(x, os.path.relpath(os.path.join(d, x), root)))
            paths += [os.path.join(d, f) for f in sorted(files) if not skip(f, os.path.relpath(os.path.join(d, f), root))]
        for p in paths:
            if p.lower().endswith(EXTS):
                inv.scan_file(p)
    vals = {k: sorted(inv.data[k].items(), key=lambda kv: (-kv[1]['count'], kv[0])) for k in CATS}
    cats = {k: {'distinct': len(vs), 'total': sum(e['count'] for _, e in vs),
                'values': [dict(value=v, **e) for v, e in vs]} for k, vs in vals.items()}
    single = lambda k: [v for v in inv.data[k] if ' ' not in v]
    hints = {'colors (RGB distance <= 12)': near(inv.data['colors'], to_rgb, 12),
             'font sizes (within 1px, rem/em at 16px)': near(single('font_size'), to_px, 1),
             'border radii (within 1px)': near(single('border_radius'), to_px, 1)}
    return {'roots': roots, 'ignore': ignore, 'files_scanned': inv.files, 'categories': cats, 'hints': hints}

def markdown(r, top=15):
    cell = lambda s: str(s).replace('|', '\\|').replace('`', "'")
    out = ['# Interface inventory scan', '',
           f"Scanned {r['files_scanned']} files under {', '.join(f'`{x}`' for x in r['roots'])}; "
           f"ignored {', '.join(f'`{g}`' for g in r['ignore'])}.",
           'Static regex scan: counts are approximate and miss runtime styles, so pair it with the '
           'screenshot session. Rough targets are rules of thumb, not limits.', '',
           '## Summary', '', '| Category | Distinct values | Total occurrences | Rough target |', '|---|---|---|---|']
    out += [f"| {CATS[k][0]} | {c['distinct']} | {c['total']} | {CATS[k][1]} |" for k, c in r['categories'].items()]
    for k, c in [(k, c) for k, c in r['categories'].items() if c['values']]:
        out += ['', f'## {CATS[k][0]}', '',
                f"{c['distinct']} distinct, {c['total']} total. Top {min(top, c['distinct'])} shown; all in scan.json.", '',
                '| Value | Count | Examples |', '|---|---|---|']
        out += [f"| `{cell(e['value'])}`" + (f" ({e['group']})" if k == 'spacing' else '')
                + f" | {e['count']} | {cell(', '.join(e['examples']))} |" for e in c['values'][:top]]
    out += ['', '## Consolidation hints', '', 'Near-duplicates the working group may want to merge. '
            'Candidates, not decisions: a 1px difference can be deliberate.']
    for label, hs in r['hints'].items():
        out += ['', f'### {label}', '']
        def label(h):
            return 'same value, notation or alpha differs' if h['distance'] == 0 else 'distance %s' % h['distance']
        out += [f"- `{cell(h['a'])}` vs `{cell(h['b'])}` ({label(h)})" for h in hs[:30]] or ['- none found']
        out += [f'- ... {len(hs) - 30} more in scan.json'] * (len(hs) > 30)
    return '\n'.join(out) + '\n'

def self_test():
    with tempfile.TemporaryDirectory() as d:
        files = {
            'a.css': '/* #000000 in a comment */\n.btn.primary:hover { color: #FFF; background: #ffffff; margin: 0px; }\n'
                     'h1 { font-size: 32px; font-weight: 700 }\n.card { font-size: 16px; border-radius: 4px; padding: 0 }\n'
                     '.note { font-size: 15px; border-radius: 5px; color: #fefefe; transition: opacity 200ms ease-in }\n'
                     ':root { --brand: rgb(255, 255, 255) }\n@media (min-width: 768px) { .card { font-size: 1rem } }\n',
            'b.html': '<button class="btn primary">A</button>\n<button class="primary btn">B</button>\n'
                      '<p style="color:#fff">x</p>\n<input type="email" class="field">\n<h1>t</h1>\n',
            'c.tsx': 'export const C = () => <Button variant="primary" style={{ fontSize: 16, color: \'white\' }} />;\n',
            'node_modules/x.css': '.x { color: #123456 }\n'}
        for name, body in files.items():
            os.makedirs(os.path.dirname(os.path.join(d, name)), exist_ok=True)
            pathlib.Path(d, name).write_text(body)
        r = scan([d], IGNORE)
        v = {k: {e['value']: e['count'] for e in c['values']} for k, c in r['categories'].items()}
        hc, hf, hr = ({(h['a'], h['b']) for h in hs} | {(h['b'], h['a']) for h in hs} for hs in r['hints'].values())
        assert r['files_scanned'] == 3, r['files_scanned']
        assert v['colors'] == {'#ffffff': 4, 'rgb(255, 255, 255)': 1, '#fefefe': 1}, v['colors']
        assert {('#ffffff', '#fefefe'), ('#ffffff', 'rgb(255, 255, 255)')} <= hc, hc
        assert v['font_size']['16px'] == 2 and {('15px', '16px'), ('1rem', '16px')} <= hf and ('4px', '5px') in hr
        assert v['spacing']['0'] == 2, v['spacing']
        assert v['buttons'] == {'<button> .btn.primary': 2, 'selector .btn.primary': 1, '<Button> variant=primary': 1}
        assert v['inputs']['<input type=email> .field'] == 1, v['inputs']
        assert v['headings']['h1 { font-size: 32px; font-weight: 700 }'] == 1, v['headings']
        assert v['custom_properties']['--brand'] == 1 and v['breakpoints']['768px (@media)'] == 1
        assert v['durations']['200ms'] == 1 and v['easings']['ease-in'] == 1
        assert '| Colors | 3 | 6 |' in markdown(r) and 'Consolidation hints' in markdown(r)
    print('self-test passed')

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('roots', nargs='*', help='directories or files to scan')
    ap.add_argument('--out', default='design-system/inventory', help='output dir (default: %(default)s)')
    ap.add_argument('--ignore', action='append', default=[], metavar='GLOB',
                    help='extra glob to skip (repeatable), added to: ' + ', '.join(IGNORE))
    ap.add_argument('--self-test', action='store_true', help='run the built-in check and exit')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.roots:
        ap.error('give at least one root path')
    if missing := [p for p in a.roots if not os.path.exists(p)]:
        ap.error('not found: ' + ', '.join(missing))
    r = scan(a.roots, IGNORE + a.ignore)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, 'scan.json'), 'w') as f:
        json.dump(r, f, indent=2)
    with open(os.path.join(a.out, 'scan.md'), 'w') as f:
        f.write(markdown(r))
    print(f"Scanned {r['files_scanned']} files. Wrote {a.out}/scan.json and {a.out}/scan.md")

if __name__ == '__main__':
    sys.exit(main())
