import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "tesseract-video" / "scripts"))

import tesseract_media
import tesseract_sound
import tesseract_waveform
import tesseract_adobe


class AuditRemediationTests(unittest.TestCase):
    def test_version_consistency(self):
        """Verify version 0.3.1 is aligned across all manifests, player, and CI."""
        # 1. release-manifest.json
        manifest = json.loads((ROOT / "release-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "0.3.1")

        # 2. plugin.json
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], "0.3.1")

        # 3. player/app.js
        app_js = (ROOT / "player" / "app.js").read_text(encoding="utf-8")
        self.assertIn("runtime/0.3.1/web_api.js", app_js)
        self.assertNotIn("runtime/0.3.0/web_api.js", app_js)

        # 4. .github/workflows/player-pages.yml
        workflow = (ROOT / ".github" / "workflows" / "player-pages.yml").read_text(encoding="utf-8")
        self.assertIn("VERSION: 0.3.1", workflow)
        self.assertNotIn("VERSION: 0.3.0", workflow)

        # 5. cli-version.txt in all skills
        for cli_ver in ROOT.glob("skills/*/references/cli-version.txt"):
            self.assertEqual(cli_ver.read_text(encoding="utf-8").strip(), "0.3.1")

    def test_plugin_manifest_antigravity_compatibility(self):
        """Verify plugin.json complies with Antigravity Plugin specification."""
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["name"], "tesseract")
        self.assertEqual(plugin["displayName"], "Tesseract by Mirage")
        # logo must not have leading ./
        self.assertEqual(plugin["logo"], "assets/plugin-icon.svg")
        self.assertTrue((ROOT / plugin["logo"]).is_file(), f"Logo file does not exist: {plugin['logo']}")
        # exactly 3 suggestedPrompts recommended
        self.assertEqual(len(plugin.get("suggestedPrompts", [])), 3)

    def test_no_dead_gemini_extension_json(self):
        """Verify legacy/unsupported gemini-extension.json is removed."""
        self.assertFalse((ROOT / "gemini-extension.json").exists())

    def test_gitignore_exists_and_ignores_agents(self):
        """Verify root .gitignore exists and ignores local .agents/ workspace clutter."""
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".agents/", gitignore)
        self.assertIn("__pycache__/", gitignore)

    def test_no_os_link_in_scripts(self):
        """Verify os.link is replaced with os.replace in all script files."""
        for script in ROOT.glob("skills/*/scripts/*.py"):
            text = script.read_text(encoding="utf-8")
            self.assertNotIn("os.link(", text, f"Found os.link in {script}")

    def test_font_resolution(self):
        """Verify cross-platform font resolution finds a font on the system."""
        font = tesseract_waveform.find_diagnostic_font()
        self.assertIsNotNone(font, "A diagnostic font should be found on this system.")
        if sys.platform == "win32":
            self.assertIn(r"\:", font, "Windows drive letters must be escaped with \\: for FFmpeg.")

    def test_sound_cue_and_waveform_generation(self):
        """Test sound synthesis, save_cue, and waveform generation without errors."""
        with tempfile.TemporaryDirectory(prefix="tsrct-test-") as tmp:
            tmp_path = Path(tmp)
            wav_file = tmp_path / "cue.wav"
            png_file = tmp_path / "waveform.png"
            json_file = tmp_path / "waveform.json"

            # 1. Synthesize and save cue
            cue_result = tesseract_sound.save_cue("soft-tap", str(wav_file), duration_ms=100)
            self.assertTrue(wav_file.is_file())
            self.assertGreater(wav_file.stat().st_size, 0)
            self.assertEqual(cue_result["preset"], "soft-tap")

            # 2. Waveform generation
            wf_result = tesseract_waveform.waveform(
                str(wav_file), str(png_file), str(json_file), mode="speech"
            )
            self.assertTrue(png_file.is_file())
            self.assertTrue(json_file.is_file())
            self.assertEqual(wf_result["mode"], "speech")

    def test_adobe_premiere_and_aftereffects_export(self):
        """Test exporting Tesseract project to Premiere Pro XML and After Effects JSX."""
        with tempfile.TemporaryDirectory(prefix="tsrct-adobe-") as tmp:
            tmp_path = Path(tmp)
            xml_file = tmp_path / "seq.xml"
            jsx_file = tmp_path / "comp.jsx"

            dummy_doc = {
                "dimensions": {"width": 1920, "height": 1080},
                "duration": 5.0,
                "composition": {
                    "id": "main",
                    "layers": [
                        {
                            "type": "Video",
                            "name": "Host Footage",
                            "playback": {"inputRange": {"start": 0, "duration": 5000}},
                            "sourceRange": {"start": 1000, "duration": 5000},
                            "source": {"assetId": "host-1"},
                        },
                        {
                            "type": "Rect",
                            "name": "News Card",
                            "activeRange": {"start": 1500, "duration": 3000},
                            "rect": {"size": [700, 200], "fillColor": [1, 1, 1, 1]},
                            "transform": {"position": [680, 260], "scale": [100, 100]},
                        },
                        {
                            "type": "Text",
                            "name": "Headline",
                            "activeRange": {"start": 1500, "duration": 3000},
                            "sourceText": {"text": "Breaking News", "fontSize": 48},
                        },
                    ],
                },
            }

            # Export Premiere XML
            tesseract_adobe.export_premiere_xml(dummy_doc, xml_file, fps=25)
            self.assertTrue(xml_file.is_file())
            xml_content = xml_file.read_text(encoding="utf-8")
            self.assertIn("<xmeml", xml_content)
            self.assertIn("<sequence>", xml_content)
            self.assertIn("Host Footage", xml_content)

            # Export After Effects JSX
            tesseract_adobe.export_aftereffects_jsx(dummy_doc, jsx_file, fps=25)
            self.assertTrue(jsx_file.is_file())
            jsx_content = jsx_file.read_text(encoding="utf-8")
            self.assertIn("app.beginUndoGroup", jsx_content)
            self.assertIn("app.project.items.addComp", jsx_content)
            self.assertIn("addText", jsx_content)
            self.assertIn("Breaking News", jsx_content)


if __name__ == "__main__":
    unittest.main()
