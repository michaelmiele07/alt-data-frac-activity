#!/usr/bin/env python3
"""Download the FracFocus bulk disclosure export (public data).

Primary source: FracFocus Chemical Disclosure Registry bulk download.
Only DisclosureList_1.csv (one row per frack-job disclosure) is used;
the chemical-level Registry files are not extracted. Zip ~420 MB; not
committed to git.
"""
import pathlib
import subprocess

URL = "https://www.fracfocusdata.org/digitaldownload/FracFocusCSV.zip"
DATA = pathlib.Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
dest = DATA / "FracFocusCSV.zip"
subprocess.run(["curl", "-sL", "-o", str(dest), URL], check=True)
subprocess.run(["unzip", "-o", "-q", str(dest), "DisclosureList_1.csv",
                "readme csv.txt", "-d", str(DATA)], check=True)
print("done:", dest)
