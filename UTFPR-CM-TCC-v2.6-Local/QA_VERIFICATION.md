# Verification and support matrix

The following tests were performed on Linux with Python 3.13 and pdfLaTeX from **TeX Live 2025/dev/Debian**. They are *not* evidence of exact TeX Live 2026 parity on UTFPR Overleaf.

- Python syntax: `python -m compileall -q scripts tests` — passed.
- Cross-platform-standard-library unit suite: `python -m unittest discover -s tests -v` — 5 tests passed.
- Native complete compilation (both language variants): `pdflatex`, `bibtex8 -8`, `makeindex` when needed, repeated `pdflatex` — passed; auxiliary files converged by pass 4.
- Acronym list: generated from used entries; unused definitions were not forcibly listed — confirmed in text extracted from the generated PDFs.
- Custom project CLI: `make compile PROJECT=... MAIN=...` — successful for a small standalone test project.
- Docker argument flow: verified using a *fake Docker CLI* invoking the installed local TeX tools. This exercises command construction, source mounting, log export, and the build phases; **it is not a real Docker-daemon/image run**.

## Not validated in this environment

- Actual Docker Desktop installation, Docker Hub image download, and Docker Engine execution.
- OS-specific prerequisite installations or GUI onboarding on Windows or macOS.
- Exact TeX Live 2026 packages used by UTFPR-hosted Overleaf.
- A warning-free build: legacy upstream LaTeX package warnings and some sample-layout warnings remain (see `build/logs/default/report.json` after compiling).

The build intentionally retains full logs and refuses to report success if any compilation command returns an error. Check the PDF visually when changing tables, illustrations, and glossary settings.
