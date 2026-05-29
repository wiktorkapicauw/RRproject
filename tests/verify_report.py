"""Smoke test for the generated Quarto report.

Run after rendering the report inside the Docker image. Verifies that the
report is complete, free of Python errors, and contains no duplicated plots
(every embedded figure must appear exactly once).
"""

import hashlib
import re
import sys
from pathlib import Path

REPORT = Path("output/report.html")

REQUIRED_SECTIONS = [
    "Introduction",
    "Model Fitting",
    "Model Comparison",
    "Diagnostics",
    "Conditional Volatility",
    "Rolling Forecast",
    "Conclusions",
]

ERROR_MARKERS = ["Traceback (most recent call last)", "ModuleNotFoundError"]


def main() -> int:
    if not REPORT.exists():
        print(f"FAIL: {REPORT} was not generated")
        return 1

    html = REPORT.read_text(encoding="utf-8")

    if not html.rstrip().endswith("</html>"):
        print("FAIL: report is truncated (missing closing </html>)")
        return 1

    missing = [s for s in REQUIRED_SECTIONS if s not in html]
    if missing:
        print(f"FAIL: missing sections: {missing}")
        return 1

    for marker in ERROR_MARKERS:
        if marker in html:
            print(f"FAIL: report contains a Python error marker: {marker!r}")
            return 1

    blobs = re.findall(r"data:image/png;base64,([A-Za-z0-9+/=]+)", html)
    if len(blobs) < 5:
        print(f"FAIL: expected at least 5 plots, found {len(blobs)}")
        return 1

    hashes = [hashlib.sha256(b.encode()).hexdigest() for b in blobs]
    if len(hashes) != len(set(hashes)):
        print(
            f"FAIL: duplicate plots detected "
            f"({len(hashes)} images, {len(set(hashes))} unique)"
        )
        return 1

    print(
        f"PASS: report complete, all sections present, "
        f"{len(blobs)} plots and all unique."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
