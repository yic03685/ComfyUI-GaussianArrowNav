# ComfyUI-GaussianArrowNav

A Gaussian Splatting preview node for ComfyUI with **arrow-key navigation**.

It is a self-contained alternative to the **Preview Gaussian** node from
[ComfyUI-GeometryPack](https://github.com/PozzettiAndrea/ComfyUI-GeometryPack):
same inputs, same gsplat.js viewer, but the viewer adds keyboard controls on
top of the usual mouse controls.

## Node

**Preview Gaussian (Arrow Nav)** — `geompack/visualization`

| Input | Type | Notes |
|-------|------|-------|
| `ply_path` | `STRING` (forced input) | Path to a Gaussian Splatting `.ply` |
| `extrinsics` *(optional)* | `EXTRINSICS` | 4×4 camera pose for the initial view |
| `intrinsics` *(optional)* | `INTRINSICS` | 3×3 intrinsics for FOV / aspect ratio |

The `EXTRINSICS` / `INTRINSICS` socket types match GeometryPack's camera nodes,
so you can wire those outputs straight in. GeometryPack does **not** need to be
installed for the node itself to work — it ships its own viewer and gsplat bundle.

## Controls

| Key | Action |
|-----|--------|
| ↑ / ↓ | Zoom in / out |
| ← / → | Orbit horizontally |
| PageUp / PageDown | Tilt up / down (vertical orbit) |
| Shift + ↑ / ↓ | Tilt up / down (alias) |
| Mouse wheel | Zoom (still works) |
| Left-drag / right-drag | Orbit / pan (still works) |

Hover the viewer (or click it) so it has keyboard focus; arrow keys then drive
the splat instead of the ComfyUI graph. Focus is released when the pointer
leaves, so the keys go back to ComfyUI.

## How it works

The navigation is implemented **without** reimplementing any orbit math. Each
held key is translated, once per animation frame, into the exact `wheel` /
mouse-drag events that gsplat's `OrbitControls` already handles — so dampening,
zoom clamping and feel are identical to using the mouse. See the commented block
at the bottom of [`web/viewer_gaussian_arrownav.html`](web/viewer_gaussian_arrownav.html).

The viewer (`viewer_gaussian_arrownav.html`) and `web/js/gsplat-bundle.js` are
vendored copies from the `comfy-3d-viewers` package so this node does not depend
on GeometryPack's startup file-copy step (which would otherwise overwrite them).

## Install

Copy this folder into `ComfyUI/custom_nodes/` and restart ComfyUI.

## Credits & license

This is **not** a fork. It is an independent package that adapts and vendors
GPL-3.0 code from two upstream projects:

- [`comfy-3d-viewers`](https://pypi.org/project/comfy-3d-viewers/) — the bundled
  `web/viewer_gaussian_arrownav.html` and `web/js/gsplat-bundle.js` are modified
  copies of that package's `viewer_gaussian.html` and `gsplat-bundle.js`.
- [ComfyUI-GeometryPack](https://github.com/PozzettiAndrea/ComfyUI-GeometryPack)
  — `web/js/gaussian_arrow_preview.js` is adapted from its Gaussian preview widget.

`gsplat-bundle.js` itself bundles [gsplat.js](https://github.com/huggingface/gsplat.js) (MIT).

Licensed under **GPL-3.0-or-later** (see [LICENSE](LICENSE)) to comply with the
upstream license.
