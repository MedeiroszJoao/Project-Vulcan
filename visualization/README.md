# Interactive vehicle explorer

Open [index.html](index.html) in a recent desktop or mobile browser with WebGL enabled. The file loads Three.js r128 from a public CDN, so it requires internet access. No build step, tracking script, user account or backend is required.

## Features

- Select, hide or isolate individual vehicle assemblies.
- Switch between 0, 2, 4 and 6 solid rocket boosters and two fairing sizes.
- Explode the assembly and inspect the illustrative interiors.
- Drag to rotate, scroll to zoom, toggle wireframe or automatic rotation.
- Inspect per-component notes distinguishing public exterior dimensions from modeled details.

## Accuracy boundary

The viewer is a **procedural illustration, not dimensionally certified CAD**. Public envelope dimensions guide overall proportions, but detailed nozzle profiles, stringers, pipes, separation interfaces, avionics fittings and payload geometry are not based on manufacturing drawings or measured vehicle hardware. The shown generic payload is **not** the Amazon Leo spacecraft. No fluid, structural, thermal or reliability solver is connected to the 3D mesh.

The original numerical decision analysis lives separately in \`src/\` and \`forecast/\`. Do not interpret model color or geometry as measured risk. In the prospective decision model, the LV-01 scenario assumes VC6L and six boosters; changing the viewer configuration does not rerun the statistical experiment.

## Source and licensing

External dimensional references: ULA Vulcan Launch Systems User's Guide and published GEM 63XL information from Northrop Grumman. The original Project Vulcan source is MIT licensed; third-party data and brands retain their own terms. Three.js is MIT licensed and fetched via CDN.

See [scientific limitations](../docs/SCIENTIFIC_LIMITATIONS.md) and [third-party notices](../THIRD_PARTY_NOTICES.md).
