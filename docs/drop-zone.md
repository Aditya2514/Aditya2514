# Drop Zone README

The profile uses a GitHub-dark base (`#0d1117`), panels (`#161b22`), amber
(`#e9b44c`), cyan (`#70c9cb`), off-white (`#e6edf3`) and secondary text (`#a8b3bf`).
Noesis uses a muted lavender accent (`#b6a7dc`).

## Rebuild

```sh
python3 scripts/build_catalog.py
python3 scripts/build_mission.py
python3 -m unittest discover -s tests -v
node --test tests/cinema-timeline.test.cjs
```

The offline build is deterministic. `build_mission.py --refresh` fetches recent
non-merge commits from the three featured public repositories, then updates the
feed and rotates a curated engineering decision. An API failure keeps the last
successful snapshot and its original timestamp. The existing six-hour workflow
runs the refresh. GitHub schedules and image caches can delay visible updates.

Edit featured art, chapter panels and colors in `scripts/mission_art.py`.
Edit feed generation and rotating decision cards in `scripts/build_mission.py`.
Edit other project metadata in `profile.json`. Preserve both generated marker
pairs in `README.md`: `MISSION-FEED` and `PROJECT-LOBBY`.

The hero embeds `assets/mission/operator.jpg` as an image data URI so its SVG is
self-contained. The JPEG is AI-generated background artwork; text, labels,
links and animation are maintained separately. The compressed JPEG is the
committed source asset; the build needs no image-generation service or package.

`picture` sources select mobile layouts and static hero variants for reduced
motion. Project SVGs also disable CSS animation for reduced motion. The hero's
operator is a still render with animated interface accents, not a video or
interactive 3D scene. Project sequences are illustrative, not production runs.

The README uses native links and details sections. Scripts execute only during
generation, never inside the README. Older cinematic assets remain available
to the existing cinema generator.

## Expanded cinematic edition

The profile now keeps its project lobby, build kit, match history and career
campaign visible. Large illustrated project stories replace the compact cards.
New JPEG source art is embedded into desktop/mobile SVGs. The image backgrounds
are still renders; animated overlays, step highlights, particles and border
traces supply the motion. The hero character itself is not a moving 3D model.

## Motion layers

Each painted scene (`operator.jpg`, `lexguard-art.jpg`, `pikina-art.jpg`, `noesis-art.jpg`) has its
effects drawn in the painting's own coordinates in `scripts/mission_art.py` (`operator_fx`,
`lexguard_fx`, `pikina_fx`, `noesis_fx`), so they stay aligned on the desktop and phone crops.
If a painting is replaced, re-check those coordinates.

The hero also carries game HUD pieces: a heading tape, a minimap with a closing zone, and a feed
of the latest commits from `data/mission-activity.json` (escaped and truncated before use).
`results.svg` is the match-result scene in the career section; edit its facts in `results()`.

Everything that moves has class `fx` and is hidden under `prefers-reduced-motion`; the hero also
has `-still` files that the README serves to people who ask for reduced motion.
