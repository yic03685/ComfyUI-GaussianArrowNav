# SPDX-License-Identifier: GPL-3.0-or-later
"""
ComfyUI-GaussianArrowNav

A drop-in alternative to GeometryPack's "Preview Gaussian" node whose viewer
adds arrow-key navigation (zoom / orbit / tilt) on top of the usual mouse
controls. The Python side is intentionally a thin path-resolver — identical in
behaviour to GeomPackPreviewGaussian — so it accepts the same inputs and can be
wired into the same workflows. All the navigation logic lives in the frontend
(web/viewer_gaussian_arrownav.html).
"""

import logging
import os

log = logging.getLogger("gaussianarrownav")

try:
    import folder_paths
    COMFYUI_OUTPUT_FOLDER = folder_paths.get_output_directory()
except (ImportError, AttributeError):
    COMFYUI_OUTPUT_FOLDER = None


class PreviewGaussianArrowNav:
    """Preview a Gaussian Splatting PLY with an arrow-key navigable viewer."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ply_path": ("STRING", {"forceInput": True}),
            },
            "optional": {
                # Same custom socket types as GeometryPack's camera nodes, so a
                # GeomPack EXTRINSICS/INTRINSICS output can drive the initial view.
                "extrinsics": ("EXTRINSICS",),
                "intrinsics": ("INTRINSICS",),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "preview"
    OUTPUT_NODE = True
    CATEGORY = "geompack/visualization"

    def preview(self, ply_path: str, extrinsics=None, intrinsics=None):
        """Resolve the PLY path and hand metadata to the frontend widget."""
        if not ply_path:
            log.info("No PLY path provided")
            return {"ui": {"error": ["No PLY path provided"]}}

        if not os.path.exists(ply_path):
            log.info("PLY file not found: %s", ply_path)
            return {"ui": {"error": [f"File not found: {ply_path}"]}}

        filename = os.path.basename(ply_path)

        # Prefer a path relative to the ComfyUI output dir when possible.
        if COMFYUI_OUTPUT_FOLDER and ply_path.startswith(COMFYUI_OUTPUT_FOLDER):
            relative_path = os.path.relpath(ply_path, COMFYUI_OUTPUT_FOLDER)
        else:
            relative_path = filename

        file_size_mb = os.path.getsize(ply_path) / (1024 * 1024)
        log.info("Loading PLY: %s (%.2f MB)", filename, file_size_mb)

        ui_data = {
            "ply_file": [relative_path],
            "filename": [filename],
            "file_size_mb": [round(file_size_mb, 2)],
        }
        if extrinsics is not None:
            ui_data["extrinsics"] = [extrinsics]
        if intrinsics is not None:
            ui_data["intrinsics"] = [intrinsics]

        return {"ui": ui_data}


NODE_CLASS_MAPPINGS = {
    "PreviewGaussianArrowNav": PreviewGaussianArrowNav,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewGaussianArrowNav": "Preview Gaussian (Arrow Nav)",
}
