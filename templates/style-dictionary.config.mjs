// Token build: DTCG 2025.10 sources -> CSS custom properties + JSON, via Style Dictionary 5.x.
// Copy to design-system/style-dictionary.config.mjs, then run: node design-system/style-dictionary.config.mjs
// Needs: npm i -D style-dictionary@^5
//
// Style Dictionary does not read resolver documents yet, so this script reads tokens/tokens.resolver.json
// itself, builds one Style Dictionary instance per permutation it needs, and diffs them into CSS
// blocks. The resolver stays the single source of truth for which files make a theme.
// When Style Dictionary ships resolver support, replace resolve() with it and keep the CSS writer.
//
// Output (dist/tokens/ next to this file):
//   tokens.css           layer order, semantic + component tiers, scheme/contrast/density/forced-colors blocks
//   <brand>.css          that brand's primitives, scoped to [data-brand="<brand>"] (default brand also on :root)
//   <brand>.<scheme>.json resolved values for non-CSS consumers (hex colors)
// Replace: PREFIX, LAYERS, FORCED_KEY (<org>), and LIGHT_DARK_FALLBACK per your browser policy.

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import StyleDictionary from 'style-dictionary';

const ROOT = dirname(fileURLToPath(import.meta.url));
const TOKENS = join(ROOT, 'tokens');
const OUT = join(ROOT, 'dist/tokens');
const PREFIX = ''; // e.g. 'ds' -> --ds-color-surface-default. Use one when the app ships other CSS.
const LAYERS = '@layer reset, tokens, base, components, utilities;';
const FORCED_KEY = 'com.<org>.forcedColors'; // $extensions key holding a CSS system color
// light-dark() is Baseline Newly Available (2024-05). Keep the fallback until your policy allows it.
const LIGHT_DARK_FALLBACK = true;
const SCOPE = ':where(:root, [data-brand])'; // re-declared under every brand scope so var() re-resolves
const SUPPORTS = '(color: light-dark(#fff, #000))';
// How each non-default modifier context reaches CSS. Brand and scheme are handled separately below.
const CSS_CONTEXTS = {
  contrast: { more: (e) => at('@media (prefers-contrast: more)', rule(SCOPE, e, '    ')) },
  density: {
    // Markup hook: data-density="compact" on any element. Works in every browser and nests by inheritance.
    // CSS hook: `--density: compact` in a stylesheet; container style queries are Baseline Newly
    // Available (2026-05), so this is a progressive enhancement. It styles descendants, not the element.
    compact: (e) => `${at('@container style(--density: compact)', rule(':where(*)', e, '    '))}\n${rule(':where([data-density="compact"])', e)}`,
  },
};

const resolver = JSON.parse(await readFile(join(TOKENS, 'tokens.resolver.json'), 'utf8'));
const mods = resolver.modifiers;

// ponytail: minimal resolver (file $refs relative to tokens/, #/sets/ pointers, inline tokens).
// No remote URLs, no #/ pointers into files. Replace with Style Dictionary's own once it exists.
async function load(list) {
  const out = [];
  for (const src of list) {
    if (src.$ref?.startsWith('#/sets/')) out.push(...(await load(resolver.sets[src.$ref.slice(7)].sources)));
    else if (src.$ref) out.push(JSON.parse(await readFile(join(TOKENS, src.$ref), 'utf8')));
    else out.push(src);
  }
  return out;
}
const isGroup = (v) => v && typeof v === 'object' && !Array.isArray(v) && !('$value' in v);
// Groups merge; a token declared again replaces the earlier one (resolver spec: last occurrence wins).
function merge(into, from) {
  for (const [k, v] of Object.entries(from)) into[k] = isGroup(v) && isGroup(into[k]) ? merge(into[k], v) : structuredClone(v);
  return into;
}
async function resolve(input) {
  const tree = {};
  for (const { $ref } of resolver.resolutionOrder) {
    const [, kind, name] = $ref.split('/');
    const list = kind === 'sets' ? resolver.sets[name].sources : mods[name].contexts[input[name] ?? mods[name].default];
    for (const src of await load(list)) merge(tree, src);
  }
  delete tree.$schema;
  delete tree.$description;
  return tree;
}

const cssTransforms = StyleDictionary.hooks.transformGroups.css.map((t) => (t === 'color/css' ? 'color/oklch' : t));
async function build(input) {
  const sd = new StyleDictionary({
    tokens: await resolve(input),
    usesDtcg: true, // DTCG mode: $value/$type/$description, color objects, {alias} syntax
    log: { verbosity: 'silent' },
    platforms: {
      css: { transforms: cssTransforms, prefix: PREFIX || undefined },
      json: { transformGroup: 'js', buildPath: `${OUT}/`, files: [{ destination: `${input.brand}.${input.scheme}.json`, format: 'json/nested' }] },
    },
  });
  const { allTokens } = await sd.getPlatformTokens('css');
  const byPath = new Map(allTokens.map((t) => [t.path.join('.'), t]));
  // A pure alias becomes var(--target) so the cascade, not the build, decides the final value.
  const ref = (v) => {
    const m = typeof v === 'string' && v.match(/^\{([^{}]+)\}$/);
    return m && `var(--${byPath.get(m[1]).name})`;
  };
  const css = (t) => {
    const v = t.original.$value;
    if (ref(v)) return ref(v);
    // Typography built from aliases: compose `font` from var()s so a [data-brand] scope re-resolves it.
    // The `font` shorthand cannot carry letter-spacing; components read that from its own token.
    const parts = t.$type === 'typography' && [v.fontWeight, v.fontSize, v.lineHeight, v.fontFamily].map(ref);
    if (parts && parts.every(Boolean)) return `${parts[0]} ${parts[1]}/${parts[2]} ${parts[3]}`;
    return t.$value;
  };
  // Breakpoints cannot be used in @media through custom properties; they stay in JSON only.
  const tokens = allTokens.filter((t) => t.path[0] !== 'breakpoint').map((t) => ({ t, css: css(t), key: JSON.stringify(t.$value) }));
  return { sd, tokens: new Map(tokens.map((x) => [x.t.name, x])) };
}

const decl = (entries, pad) => entries.map(([n, v]) => `${pad}--${n}: ${v};`).join('\n');
const rule = (sel, entries, pad = '  ') => `${pad}${sel} {\n${decl(entries, pad + '  ')}\n${pad}}`;
const at = (cond, inner, pad = '  ') => `${pad}${cond} {\n${inner}\n${pad}}`;
// Tokens whose resolved value differs from the base build, written in the variant's own (aliased) form.
const diff = (base, variant) => [...variant.tokens].filter(([n, x]) => base.tokens.get(n)?.key !== x.key).map(([n, x]) => [n, x.css]);

// Token paths declared in a list of sources (used to tell a brand's primitives from the shared tiers).
const pathsIn = async (list) => {
  const paths = new Set();
  const walk = (node, path) => Object.entries(node).forEach(([k, v]) => {
    if (k.startsWith('$') || !v || typeof v !== 'object') return;
    '$value' in v ? paths.add([...path, k].join('.')) : walk(v, [...path, k]);
  });
  for (const src of await load(list)) walk(src, []);
  return paths;
};

const defaults = Object.fromEntries(Object.entries(mods).map(([k, m]) => [k, m.default]));
await mkdir(OUT, { recursive: true });

// 1. Per brand: primitives CSS, plus resolved JSON per scheme.
for (const brand of Object.keys(mods.brand.contexts)) {
  const own = await pathsIn(mods.brand.contexts[brand]);
  for (const scheme of Object.keys(mods.scheme.contexts)) await (await build({ ...defaults, brand, scheme })).sd.buildPlatform('json');
  const { tokens } = await build({ ...defaults, brand });
  const body = [...tokens.values()].filter((x) => own.has(x.t.path.join('.'))).map((x) => [x.t.name, x.css]);
  const selector = brand === mods.brand.default ? `:root,\n  [data-brand="${brand}"]` : `[data-brand="${brand}"]`;
  await writeFile(join(OUT, `${brand}.css`), `/* Generated. Do not edit. Primitives for ${brand}. */\n@layer tokens {\n${rule(selector, body)}\n}\n`);
}

// 2. Shared tokens.css: semantic + component tiers and every theming axis. Brand-independent because
//    semantic and component tokens only alias, so their CSS is var(--primitive) for any brand.
const base = await build(defaults);
const primitives = await pathsIn(mods.brand.contexts[mods.brand.default]);
const shared = [...base.tokens.values()].filter((x) => !primitives.has(x.t.path.join('.')));
const dark = await build({ ...defaults, scheme: 'dark' });
const darkDelta = diff(base, dark);
const lightDark = (x) => {
  const d = dark.tokens.get(x.t.name).css;
  return d === x.css ? x.css : `light-dark(${x.css}, ${d})`;
};

const parts = [
  '  :root {\n    color-scheme: light dark;\n  }',
  '  [data-theme="light"] {\n    color-scheme: light;\n  }',
  '  [data-theme="dark"] {\n    color-scheme: dark;\n  }',
  rule(SCOPE, shared.map((x) => [x.t.name, LIGHT_DARK_FALLBACK ? x.css : lightDark(x)])),
];
if (LIGHT_DARK_FALLBACK) {
  const ld = shared.filter((x) => lightDark(x) !== x.css).map((x) => [x.t.name, lightDark(x)]);
  parts.push(at(`@supports ${SUPPORTS}`, rule(SCOPE, ld, '    ')));
  parts.push(at(`@supports not ${SUPPORTS}`, [
    at('@media (prefers-color-scheme: dark)', rule(SCOPE, darkDelta, '      '), '    '),
    rule('[data-theme="dark"]', darkDelta, '    '),
    rule('[data-theme="light"]', darkDelta.map(([n]) => [n, base.tokens.get(n).css]), '    '),
  ].join('\n')));
}
for (const [axis, contexts] of Object.entries(CSS_CONTEXTS)) {
  for (const [ctx, toCss] of Object.entries(contexts)) {
    const delta = diff(base, await build({ ...defaults, [axis]: ctx }));
    if (delta.length) parts.push(toCss(delta));
  }
}
const forced = shared.filter((x) => x.t.$extensions?.[FORCED_KEY]).map((x) => [x.t.name, x.t.$extensions[FORCED_KEY]]);
if (forced.length) parts.push(at('@media (forced-colors: active)', rule(SCOPE, forced, '    ')));

await writeFile(join(OUT, 'tokens.css'), `/* Generated. Do not edit. Load before any other stylesheet. */\n${LAYERS}\n\n@layer tokens {\n${parts.join('\n\n')}\n}\n`);
console.log(`Built tokens.css and ${Object.keys(mods.brand.contexts).length} brand files into ${OUT}`);
