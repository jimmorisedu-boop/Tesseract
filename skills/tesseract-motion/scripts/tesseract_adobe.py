"""Adobe Premiere Pro (FCP XML) and After Effects (ExtendScript JSX) export tools for Tesseract.

Converts Tesseract project editable JSON or .tsrct bundles into:
1. Final Cut Pro / Premiere XML (.xml) for native Premiere Pro timeline import.
2. Adobe After Effects ExtendScript (.jsx) for rebuilding compositions, layers, text, shapes, and transforms.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


def parse_project_json(json_path: Path) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def export_premiere_xml(doc: dict, output_path: Path, sequence_name: str = "Tesseract Sequence", fps: int = 25) -> Path:
    """Generate Final Cut Pro 7 / Premiere Pro XML (xmeml version 4)."""
    width = doc.get("dimensions", {}).get("width", 1920)
    height = doc.get("dimensions", {}).get("height", 1080)
    duration_sec = doc.get("duration", 10.0)
    total_frames = int(round(duration_sec * fps))

    comp = doc.get("composition", {})
    layers = comp.get("layers", [])

    xmeml = ET.Element("xmeml", version="4")
    seq = ET.SubElement(xmeml, "sequence")
    ET.SubElement(seq, "name").text = sequence_name
    ET.SubElement(seq, "duration").text = str(total_frames)

    rate = ET.SubElement(seq, "rate")
    ET.SubElement(rate, "timebase").text = str(fps)
    ET.SubElement(rate, "ntsc").text = "FALSE"

    media = ET.SubElement(seq, "media")
    video = ET.SubElement(media, "video")
    v_format = ET.SubElement(video, "format")
    sc = ET.SubElement(v_format, "samplecharacteristics")
    ET.SubElement(sc, "width").text = str(width)
    ET.SubElement(sc, "height").text = str(height)
    sc_rate = ET.SubElement(sc, "rate")
    ET.SubElement(sc_rate, "timebase").text = str(fps)
    ET.SubElement(sc_rate, "ntsc").text = "FALSE"

    # Separate video/visual and audio layers
    v_track = ET.SubElement(video, "track")
    audio = ET.SubElement(media, "audio")
    a_track = ET.SubElement(audio, "track")

    clip_id_counter = 1
    for layer in layers:
        l_type = layer.get("type", "")
        l_name = layer.get("name", f"Layer {clip_id_counter}")

        # Determine start and duration in frames
        start_ms = 0
        dur_ms = int(round(duration_sec * 1000))

        if "playback" in layer and isinstance(layer["playback"], dict):
            in_range = layer["playback"].get("inputRange", {})
            start_ms = in_range.get("start", 0)
            dur_ms = in_range.get("duration", dur_ms)
        elif "activeRange" in layer and isinstance(layer["activeRange"], dict):
            start_ms = layer["activeRange"].get("start", 0)
            dur_ms = layer["activeRange"].get("duration", dur_ms)

        start_frame = int(round((start_ms / 1000.0) * fps))
        dur_frames = int(round((dur_ms / 1000.0) * fps))
        end_frame = start_frame + dur_frames

        # Source Range
        src_start_ms = 0
        src_dur_ms = dur_ms
        if "sourceRange" in layer and isinstance(layer["sourceRange"], dict):
            src_start_ms = layer["sourceRange"].get("start", 0)
            src_dur_ms = layer["sourceRange"].get("duration", dur_ms)

        src_in_frame = int(round((src_start_ms / 1000.0) * fps))
        src_out_frame = src_in_frame + dur_frames

        if l_type in ("Video", "Image", "Rect", "Text"):
            clipitem = ET.SubElement(v_track, "clipitem", id=f"clipitem-{clip_id_counter}")
            ET.SubElement(clipitem, "name").text = l_name
            ET.SubElement(clipitem, "duration").text = str(total_frames)
            c_rate = ET.SubElement(clipitem, "rate")
            ET.SubElement(c_rate, "timebase").text = str(fps)
            ET.SubElement(c_rate, "ntsc").text = "FALSE"
            ET.SubElement(clipitem, "start").text = str(start_frame)
            ET.SubElement(clipitem, "end").text = str(end_frame)
            ET.SubElement(clipitem, "in").text = str(src_in_frame)
            ET.SubElement(clipitem, "out").text = str(src_out_frame)

            # Asset file info if available
            asset_id = ""
            if "source" in layer and isinstance(layer["source"], dict):
                asset_id = layer["source"].get("assetId", "")
            file_elem = ET.SubElement(clipitem, "file", id=f"file-{clip_id_counter}")
            ET.SubElement(file_elem, "name").text = asset_id or l_name
            f_rate = ET.SubElement(file_elem, "rate")
            ET.SubElement(f_rate, "timebase").text = str(fps)
            ET.SubElement(f_rate, "ntsc").text = "FALSE"

            clip_id_counter += 1

        elif l_type == "Audio":
            aclipitem = ET.SubElement(a_track, "clipitem", id=f"clipitem-{clip_id_counter}")
            ET.SubElement(aclipitem, "name").text = l_name
            ET.SubElement(aclipitem, "duration").text = str(total_frames)
            a_rate = ET.SubElement(aclipitem, "rate")
            ET.SubElement(a_rate, "timebase").text = str(fps)
            ET.SubElement(a_rate, "ntsc").text = "FALSE"
            ET.SubElement(aclipitem, "start").text = str(start_frame)
            ET.SubElement(aclipitem, "end").text = str(end_frame)
            ET.SubElement(aclipitem, "in").text = str(src_in_frame)
            ET.SubElement(aclipitem, "out").text = str(src_out_frame)

            clip_id_counter += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(xmeml)
    ET.indent(tree, space="  ")
    tree.write(str(output_path), encoding="utf-8", xml_declaration=True)
    return output_path


def export_aftereffects_jsx(doc: dict, output_path: Path, comp_name: str = "Tesseract Comp", fps: int = 25) -> Path:
    """Generate Adobe After Effects ExtendScript (.jsx) file to rebuild the composition."""
    width = doc.get("dimensions", {}).get("width", 1920)
    height = doc.get("dimensions", {}).get("height", 1080)
    duration_sec = doc.get("duration", 10.0)

    comp = doc.get("composition", {})
    layers = comp.get("layers", [])

    lines = [
        "// Adobe After Effects ExtendScript Generated by Tesseract",
        "// Automatically builds the composition, layers, text, shapes, and timing",
        "(function() {",
        '    app.beginUndoGroup("Import Tesseract Project");',
        "",
        f'    var comp = app.project.items.addComp("{comp_name}", {width}, {height}, 1.0, {duration_sec}, {fps});',
        "    if (!comp) {",
        '        alert("Failed to create After Effects composition.");',
        "        return;",
        "    }",
        "",
    ]

    # Layers in reverse so layer[0] is frontmost (topmost) in After Effects
    for idx, layer in enumerate(reversed(layers)):
        l_type = layer.get("type", "")
        l_name = layer.get("name", f"Layer_{idx}")

        start_ms = 0
        dur_ms = int(round(duration_sec * 1000))
        if "playback" in layer and isinstance(layer["playback"], dict):
            in_range = layer["playback"].get("inputRange", {})
            start_ms = in_range.get("start", 0)
            dur_ms = in_range.get("duration", dur_ms)
        elif "activeRange" in layer and isinstance(layer["activeRange"], dict):
            start_ms = layer["activeRange"].get("start", 0)
            dur_ms = layer["activeRange"].get("duration", dur_ms)

        in_sec = start_ms / 1000.0
        out_sec = (start_ms + dur_ms) / 1000.0

        transform = layer.get("transform", {})
        pos = transform.get("position", [width / 2, height / 2])
        scale = transform.get("scale", [100, 100])
        opacity = transform.get("opacity", 100)
        rotation = transform.get("rotation", 0)

        lines.append(f"    // --- Layer: {l_name} ({l_type}) ---")

        if l_type == "Text":
            src_text = layer.get("sourceText", {})
            text_val = src_text.get("text", "").replace('"', '\\"').replace("\n", "\\r")
            font_size = src_text.get("fontSize", 48)
            fill_col = src_text.get("fillColor", [1, 1, 1, 1])

            lines.extend([
                f'    var tLayer = comp.layers.addText("{text_val}");',
                f'    tLayer.name = "{l_name}";',
                f"    tLayer.startTime = {in_sec};",
                f"    tLayer.inPoint = {in_sec};",
                f"    tLayer.outPoint = {out_sec};",
                "    var textProp = tLayer.property('Source Text');",
                "    var textDoc = textProp.value;",
                f"    textDoc.fontSize = {font_size};",
                f"    textDoc.fillColor = [{fill_col[0]}, {fill_col[1]}, {fill_col[2]}];",
                "    textProp.setValue(textDoc);",
                f"    tLayer.property('Position').setValue([{pos[0]}, {pos[1]}]);",
                f"    tLayer.property('Scale').setValue([{scale[0]}, {scale[1]}]);",
                f"    tLayer.property('Opacity').setValue({opacity});",
                f"    tLayer.property('Rotation').setValue({rotation});",
                "",
            ])

        elif l_type == "Rect":
            rect_data = layer.get("rect", {})
            size = rect_data.get("size", [400, 200])
            fill_col = rect_data.get("fillColor", [0.2, 0.4, 0.8, 1.0])
            w, h = int(size[0]), int(size[1])

            lines.extend([
                f'    var sLayer = comp.layers.addSolid([{fill_col[0]}, {fill_col[1]}, {fill_col[2]}], "{l_name}", {w}, {h}, 1.0);',
                f"    sLayer.startTime = {in_sec};",
                f"    sLayer.inPoint = {in_sec};",
                f"    sLayer.outPoint = {out_sec};",
                f"    sLayer.property('Position').setValue([{pos[0]}, {pos[1]}]);",
                f"    sLayer.property('Scale').setValue([{scale[0]}, {scale[1]}]);",
                f"    sLayer.property('Opacity').setValue({opacity});",
                f"    sLayer.property('Rotation').setValue({rotation});",
                "",
            ])

        elif l_type in ("Video", "Image"):
            asset_id = ""
            if "source" in layer and isinstance(layer["source"], dict):
                asset_id = layer["source"].get("assetId", "")

            lines.extend([
                f'    // Placeholder Solid for media asset "{asset_id or l_name}"',
                f'    var mLayer = comp.layers.addSolid([0.15, 0.15, 0.18], "{l_name} [{asset_id}]", {width}, {height}, 1.0);',
                f"    mLayer.startTime = {in_sec};",
                f"    mLayer.inPoint = {in_sec};",
                f"    mLayer.outPoint = {out_sec};",
                f"    mLayer.property('Position').setValue([{pos[0]}, {pos[1]}]);",
                f"    mLayer.property('Scale').setValue([{scale[0]}, {scale[1]}]);",
                f"    mLayer.property('Opacity').setValue({opacity});",
                f"    mLayer.property('Rotation').setValue({rotation});",
                "",
            ])

    lines.extend([
        '    app.endUndoGroup();',
        f'    alert("Tesseract composition \'{comp_name}\' successfully imported into After Effects!");',
        "})();",
        "",
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return output_path


def export_adobe_bundle(project_or_json: str | Path, output_dir: str | Path, tsrct_cli: str | None = None) -> dict:
    """Generate both Premiere XML and After Effects JSX from a .tsrct project or editable JSON."""
    src = Path(project_or_json).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    json_path = src
    temp_json = None

    if src.suffix == ".tsrct":
        cli = tsrct_cli or os.path.expandvars(r"%LOCALAPPDATA%\Tesseract\bin\tsrct.cmd")
        temp_json = out / "tesseract_editable_temp.json"
        subprocess.run([cli, "project", "checkout", "-p", str(src), "-o", str(temp_json)], check=True)
        json_path = temp_json

    doc = parse_project_json(json_path)

    base_name = src.stem if src.suffix == ".tsrct" else "tesseract_project"
    xml_file = out / f"{base_name}_premiere.xml"
    jsx_file = out / f"{base_name}_aftereffects.jsx"

    export_premiere_xml(doc, xml_file, sequence_name=base_name)
    export_aftereffects_jsx(doc, jsx_file, comp_name=base_name)

    if temp_json and temp_json.exists():
        temp_json.unlink()

    return {
        "status": "success",
        "premiere_xml": str(xml_file),
        "aftereffects_jsx": str(jsx_file),
        "source": str(src),
    }


def main():
    parser = argparse.ArgumentParser(description="Export Tesseract project to Premiere Pro XML and After Effects JSX")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Premiere XML
    p_prem = subparsers.add_parser("premiere", help="Export to Premiere Pro XML (.xml)")
    p_prem.add_argument("--json", required=True, help="Path to project editable JSON")
    p_prem.add_argument("--output", required=True, help="Output .xml file path")
    p_prem.add_argument("--fps", type=int, default=25, help="Frame rate")

    # After Effects JSX
    p_ae = subparsers.add_parser("aftereffects", help="Export to After Effects JSX (.jsx)")
    p_ae.add_argument("--json", required=True, help="Path to project editable JSON")
    p_ae.add_argument("--output", required=True, help="Output .jsx script path")
    p_ae.add_argument("--fps", type=int, default=25, help="Frame rate")

    # All / Bundle
    p_all = subparsers.add_parser("bundle", help="Export complete Adobe bundle (Premiere XML + AE JSX)")
    p_all.add_argument("--input", required=True, help="Path to .tsrct or editable JSON")
    p_all.add_argument("--output-dir", required=True, help="Directory to save Adobe export files")

    args = parser.parse_args()

    if args.command == "premiere":
        doc = parse_project_json(Path(args.json))
        res = export_premiere_xml(doc, Path(args.output), fps=args.fps)
        print(f"Exported Premiere XML: {res}")
    elif args.command == "aftereffects":
        doc = parse_project_json(Path(args.json))
        res = export_aftereffects_jsx(doc, Path(args.output), fps=args.fps)
        print(f"Exported After Effects JSX: {res}")
    elif args.command == "bundle":
        res = export_adobe_bundle(args.input, args.output_dir)
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
